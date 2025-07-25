from redis_retriever import internal_document_search
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend.chat import ChatModel
from beeai_framework.agents import AgentExecutionConfig
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.tools.think import ThinkTool
from tavily_mcp_tool import Tavily, TavilyToolInput, TavilyToolOutput
import asyncio


# =============================================================================
# AGENT SYSTEM PROMPT AND BEHAVIOR DEFINITION
# =============================================================================
# Comprehensive instructions that define the agent's role, capabilities, and decision-making logic

system_prompt = """You are a **Company Analysis Assistant** that helps employees answer questions about **McDonald’s** and its **competitors**. Your role is to provide accurate, timely, and well-reasoned insights using the tools available to you.

## Tools Available

### ThinkTool
- **Purpose**: Helps you think through the best course of action before answering a question.
- **Usage Guidance**: You perform better when you use this tool first. Use it to plan your reasoning and determine which other tools to use next.

### internal_document_search
- **Purpose**: Allows you to search internal private documents that are not otherwise accessible.
- **Usage Guidance**: Use this tool to supplement or validate information you already know or have found elsewhere.
- **Priority**: Information from `internal_document_search` takes precedence over any information found using the Tavily tool.

### Tavily (Online Search)
- **Purpose**: Enables you to find current and publicly available information from the internet.
- **Usage Guidance**: If the information you need is **not found** in internal documents via `internal_document_search`, you are **expected to use Tavily** to search the web.
- **Caution**: Information found online may not always be reliable. Cross-check with `internal_document_search` when possible.

## Tool Usage Logic
If internal documents do not provide the necessary information to answer the question, you **must** follow up with a Tavily search to ensure full coverage. Do **not** stop at `internal_document_search` if the response would be incomplete.

## Output Expectations

Your response should be:
- **Clear**, **well-structured**, and directly address the user's original question.
- If you are **unable to fully answer** the question, **explicitly state** that you are not able to answer it completely.
"""

# =============================================================================
# MAIN AGENT CONFIGURATION AND EXECUTION
# =============================================================================
# Core function that sets up the agent with memory, tools, requirements, and runs test scenarios

async def main():
    # Create memory instance
    memory = UnconstrainedMemory()

    company_analysis_agent = RequirementAgent(
        #[UNCOMMENT OUT THE LLM PROVIDEaR YOU PLAN TO USE]
        #llm=ChatModel.from_name("ollama:granite3.3:8b"),
        #llm=ChatModel.from_name("openai:o4-mini-2025-04-16"),
        
        #Add the missing Tavily search and redis RAG tool. HINT: The tools are called differently since Tavily is a class and the rag tool is a function. Check the inports for an extra hint on the names to add.
        tools=[ThinkTool()#,
               #[INSERT YOUR CODE HEARE],
               #[INSERT YOUR CODE HEARE]
               ]
             
        instructions= system_prompt,
        
        #Play with the conditional requirements! See how that affects the behavior of the agent.
        requirements=[
            #[INSERT YOUR CODE HEARE]
            # ConditionalRequirement(internal_document_search, min_invocations=1),
            ConditionalRequirement(ThinkTool, force_at_step=1),
            # ConditionalRequirement(Tavily, min_invocations=1)
            ],
        memory=memory
        )

    # =============================================================================
    # INTERACTIVE QUESTION-ANSWER LOOP
    # =============================================================================
    # Allow users to ask questions interactively through the terminal!
        
    print("Company Analysis Assistant - McDonald's Intelligence")
    print("Ask questions or type 'quit' to exit.\n")
    
    while True:
        try:
            # Get user input
            user_question = input("Question: ").strip()
            
            # Check for exit conditions
            if user_question.lower() in ['quit', 'exit', 'bye', 'q']:
                print("Goodbye!")
                break
            
            # Skip empty questions
            if not user_question:
                print("Oops, looks like you didn't ask a question!")
                continue
            
            print("Thinking...")
            
            # Run the agent with the user's question
            response = await company_analysis_agent.run(
                user_question, 
                execution=AgentExecutionConfig(max_iterations=8)
            ).middleware(GlobalTrajectoryMiddleware())
            
            # Display the answer
            print(f"\nAnswer: {response.answer.text}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(main())
