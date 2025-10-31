import asyncio
import json
import os
import logging
from pathlib import Path
from pprint import pprint
from typing import Any, Optional, List, Literal, Dict
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter
from beeai_framework.errors import FrameworkError
from beeai_framework.tools import Tool, ToolRunOptions, JSONToolOutput
from beeai_framework.tools.errors import ToolInputValidationError
from beeai_framework.tools.mcp import MCPTool
from beeai_framework import context
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# =============================================================================
# SETUP AND CONFIGURATION
# =============================================================================
# Set up working directory and environment for the MCP server to run properly
# print(f"Current working directory: {os.getcwd()}")
script_dir = Path(__file__).parent
# print(f"Script directory: {script_dir}")

# Change to script directory
os.chdir(script_dir)
# print(f"Changed to: {os.getcwd()}")

# =============================================================================
# SETTINGS AND CONFIGURATION MODELS
# =============================================================================
# Configuration class to handle API keys and environment variables

class Settings(BaseSettings):
    TAVILY_API_KEY: str = Field(alias='TAVILY_API_KEY')
    model_config = SettingsConfigDict(env_file='../.env', extra='ignore')


# =============================================================================
# SEARCH RESULT PARSING UTILITIES
# =============================================================================
# Helper functions to transform raw Tavily API responses into structured data

def parse_search_results(text_content: str, query: str) -> Dict[str, Any]:
    """Parse Tavily text results into structured format"""
    results = []
    
    # Split by "Title:" to get individual results
    title_sections = text_content.split("Title:")
    
    for section in title_sections[1:]:  # Skip first empty section
        lines = section.strip().split('\\n')
        title = lines[0].strip() if lines else ""
        
        url = ""
        content = ""
        
        for i, line in enumerate(lines):
            if line.startswith("URL:"):
                url = line.replace("URL:", "").strip()
            elif line.startswith("Content:"):
                content_lines = lines[i:]
                content = " ".join(line.replace("Content:", "").strip() 
                                for line in content_lines if line.strip())
                break
        
        if title and url:
            results.append({
                "title": title,
                "url": url,
                "content": content.strip(),
                "score": 1.0 - (len(results) * 0.1)
            })
    
    return {
        "query": query,
        "results": results,
        "total_results": len(results)
    }


# =============================================================================
# MAIN SEARCH CLIENT CLASS
# =============================================================================
# Core class that manages the MCP connection and handles search operations

class TavilySearch:
    """Tavily search client with persistent MCP session"""
    
    def __init__(self):
        self.settings = Settings()
        self.session = None
        self.search_tool = None
        self.server_params = StdioServerParameters(
            command="npx",
            args=["-y", "tavily-mcp@latest"],
            env={"TAVILY_API_KEY": self.settings.TAVILY_API_KEY}
        )
        self._context_manager = None
    
    async def __aenter__(self):
        """Start MCP server and initialize session"""
        self._context_manager = stdio_client(self.server_params)
        read, write = await self._context_manager.__aenter__()
        
        self.session = ClientSession(read, write)
        await self.session.__aenter__()
        await self.session.initialize()
        
        # Get search tool once
        tools = await MCPTool.from_client(self.session)
        self.search_tool = next((tool for tool in tools if "tavily-search" in tool.name), None)
        
        if not self.search_tool:
            raise ValueError("Tavily search tool not found")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up session and server"""
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
        if self._context_manager:
            await self._context_manager.__aexit__(exc_type, exc_val, exc_tb)
    
    async def search(
        self,
        # What is the main input that the model needs to provide? Hint: Look down in the search arguments dictionary and see what's missing.
        # [UNCOMMENT AND INSERT YOUR CODE HERE]
        max_results: int = 5,
        search_depth: str = "basic",
        include_domains: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Perform search using existing session"""
        if not self.session or not self.search_tool:
            raise RuntimeError("TavilySearch not initialized. Use 'async with TavilySearch():'")
        
        try:
            # Prepare search arguments
            arguments = {
                "query": query,
                "max_results": max_results,
                "search_depth": search_depth,
                "include_images": False,
                "topic": "general",
                "include_raw_content": False
            }
            
            if include_domains:
                arguments["include_domains"] = include_domains
            
            # Add any additional parameters
            arguments.update(kwargs)
            
            # Execute search
            result = await self.search_tool.run(arguments)
            
            # Extract text content from JSONToolOutput
            result_str = str(result)
            
            # Try to parse the nested JSON structure
            try:
                import ast
                try:
                    result_data = ast.literal_eval(result_str)
                except:
                    result_data = [{"type": "text", "text": result_str}]
                
                # Extract the text field which contains another JSON string
                if isinstance(result_data, list) and len(result_data) > 0:
                    first_item = result_data[0]
                    if isinstance(first_item, dict) and "text" in first_item:
                        nested_text = first_item["text"]
                        
                        # Parse the nested JSON to get the actual search results
                        nested_data = json.loads(nested_text)
                        if isinstance(nested_data, list) and len(nested_data) > 0:
                            nested_item = nested_data[0]
                            if isinstance(nested_item, dict) and "text" in nested_item:
                                text_content = nested_item["text"]
                            else:
                                text_content = nested_text
                        else:
                            text_content = nested_text
                    else:
                        text_content = str(result)
                else:
                    text_content = str(result)
                    
            except Exception as parse_error:
                text_content = str(result)
            
            # Parse and return structured results
            return parse_search_results(text_content, query)

        except ToolInputValidationError as tive:
            return {"error": tive.explain()}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}


# =============================================================================
# FRAMEWORK INTEGRATION MODELS
# =============================================================================
# Pydantic models that define the tool's input/output schema for the framework

class TavilyToolInput(BaseModel):
    query: str = Field(..., description="The query that will be searched for on the internet.")
    max_results: Literal[5] = Field(5, description="Fixed number of search results.")
    search_depth: Literal["basic"] = Field("basic", description="Fixed search depth.")
    include_domains: Optional[List[str]] = Field(None, description="Optional list of domains to constrain the search.")
    time_range: Literal[
        'day', 'week', 'month', 'year', 'd', 'w', 'm', 'y'] = Field("year", description="Time range to use for search")
    country: Literal["united states"] = Field("united states", description="Country to use for search")


class ParsedResult(BaseModel):
    title: str
    url: str
    content: str
    score: float


class TavilyToolOutput(BaseModel):
    query: str
    results: List[ParsedResult]
    total_results: int

# =============================================================================
# MAIN FRAMEWORK TOOL IMPLEMENTATION
# =============================================================================
# The primary tool class that implements the framework's Tool interface


class Tavily(Tool[TavilyToolInput, ToolRunOptions, JSONToolOutput[TavilyToolOutput]]):
    name = "TavilyTool"
    # Enter your description of the Tavily tool that is akin to "Search the internet for current information that you might not already know".
    # description = "[UNCOMMENT AND INSERT YOUR CODE HERE]"
    input_schema = TavilyToolInput

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        super().__init__(options)
        self.logger = logging.getLogger(__name__)

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "tavily", "search"],
            creator=self,
        )

    async def _run(
        self, 
        input: TavilyToolInput, 
        options: ToolRunOptions | None, 
        context: RunContext
    ) -> JSONToolOutput[TavilyToolOutput]:
        """Execute the Tavily search and return structured results"""
        
        try:
            print("Run Tavily tool search...")
            # Create and use TavilySearch with async context manager
            async with TavilySearch() as tavily:
                search_results = await tavily.search(**input.__dict__)
            print("Run Tavily tool search...")

            # Check for errors in search results
            if "error" in search_results:
                raise ToolInputValidationError(f"Search failed: {search_results['error']}")

            print(f"Tavily tool search returned {search_results.get('total_results')} results.")

            # Convert to our output format
            parsed_results = []
            for result in search_results.get("results", []):
                parsed_results.append(ParsedResult(
                    title=result["title"],
                    url=result["url"],
                    content=result["content"],
                    score=result["score"]
                ))
            
            output = TavilyToolOutput(
                query=search_results["query"],
                results=parsed_results,
                total_results=search_results["total_results"]
            )
            
            return JSONToolOutput(output.model_dump())
            
        except Exception as e:
            # Log the error and re-raise as a framework error
            self.logger.error(f"Tavily search failed: {str(e)}")
            raise FrameworkError(f"Failed to perform search: {str(e)}") from e


# =============================================================================
# TESTING AND DEMONSTRATION
# =============================================================================
# Test function to verify the tool works correctly

async def test_tavily_tool():
    """Test function for the Tavily tool"""
    
    # Initialize the tool
    tavily_tool = Tavily()
    
    # Create input
    search_input = TavilyToolInput(
        query="Python async programming",
        include_domains=["github.com", "stackoverflow.com"]
    )
    
    try:
        # Run the tool (within async context)
        print("Run Tavily tool search...")
        results = await tavily_tool._run(search_input, None, context)
        print("Search completed successfully!")
        print("Results:")
        pprint(results.to_json_safe())
    except Exception as e:
        print(f"Error running search: {e}")

if __name__ == "__main__":
    asyncio.run(test_tavily_tool())
