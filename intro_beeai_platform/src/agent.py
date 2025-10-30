# Copyright 2025 © BeeAI a Series of LF Projects, LLC
# SPDX-License-Identifier: Apache-2.0

# BeeAI Platform demo based on the Intro to BeeAI Framework Workshop 🐝
#
# 🎯 Scenario: The Field Marketing Lead has asked you to help prepare their team for conference season. You create a Conference Prep Agent that uses 3 tools: web search to collect relevant news and search for up to date information, Wikipedia to provide company history and details, and the team's internal notes and artifacts.

# System
import asyncio
from datetime import date
import logging
import json
import os
import sys
from typing import Annotated

# Third party
from beeai_sdk.a2a.extensions import (
    AgentDetailContributor,
    AgentDetailTool,
    CitationExtensionServer,
    CitationExtensionSpec,
)
from a2a.types import AgentCapabilities, AgentSkill
from a2a.utils.message import get_message_text
from dotenv import load_dotenv
# from openinference.instrumentation.beeai import BeeAIInstrumentor

# BeeAI Framework imports
from beeai_framework.utils.strings import to_json_serializable
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.agents.requirement.events import RequirementAgentSuccessEvent
from beeai_framework.agents.requirement.requirements.conditional import ConditionalRequirement
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.backend.document_loader import DocumentLoader
from beeai_framework.backend.embedding import EmbeddingModel
from beeai_framework.backend.text_splitter import TextSplitter
from beeai_framework.backend.vector_store import VectorStore
from beeai_framework.emitter import EventMeta
from beeai_framework.memory import SummarizeMemory
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool, tool
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.search.retrieval import VectorStoreSearchTool
from beeai_framework.tools.search.wikipedia import WikipediaTool, WikipediaToolInput
from beeai_framework.tools.think import ThinkTool

# BeeAI SDK imports
from beeai_sdk.a2a.extensions import TrajectoryExtensionServer, TrajectoryExtensionSpec
from beeai_sdk.a2a.extensions import Citation
from beeai_sdk.a2a.types import AgentMessage

from a2a.types import (
    Message,
)

from beeai_sdk.server import Server
from beeai_sdk.server.context import RunContext

import beeai_sdk.a2a.extensions
from beeai_sdk.a2a.extensions.ui.form import (
    DateField,
    TextField,
    FileField,
    CheckboxField,
    MultiSelectField,
    OptionItem,
    FormExtensionServer,
    FormExtensionSpec,
    FormRender,
)

# Constants
AGENT_NAME = "Conference Prep Agent"

# Read .env and set environment variables
load_dotenv()


#  ## 1️⃣ LLM Providers: Choose Your AI Engine

# BeeAI Framework supports 10+ LLM providers including Ollama, Groq, OpenAI, Watsonx.ai, and more, giving you flexibility to choose local or hosted models based on your needs. In this workshop we'll be working Ollama, so you will be running the model locally. You can find the documentation on how to connect to other providers [here](https://framework.beeai.dev/modules/backend).
# Change the `PROVIDER_ID` and `MODEL_ID` in your .env file. If you select a provider that requires an API key, please replace the placeholder with your `api_key`.
# Try several models to see how your agent performs. Note that you may need to modify the system prompt for each model, as they all have their own system prompt best practice.

PROVIDER_ID = os.getenv("PROVIDER_ID")
MODEL_ID = os.getenv("MODEL_ID")
MODEL_NAME = ":".join([PROVIDER_ID, MODEL_ID]) if PROVIDER_ID and MODEL_ID else None

# Load the chat model
llm = ChatModel.from_name(MODEL_NAME, ChatModelParameters(temperature=1))

# Load the embedding model
# TODO: this should be configurable in the .env too
embedding_model = EmbeddingModel.from_name("ollama:nomic-embed-text")

logging.getLogger("opentelemetry.exporter.otlp.proto.http._log_exporter").setLevel(
    logging.CRITICAL
)
logging.getLogger("opentelemetry.exporter.otlp.proto.http.metric_exporter").setLevel(
    logging.CRITICAL
)

# ## Setup Observability: See what is happening under the hood
# To run beeai platform with phoenex enabled (review the license and) start it like this:
#     beeai platform start --set phoenix.enabled=true
EventMeta.model_fields["context"].exclude = True  # Temp fix?
# BeeAIInstrumentor().instrument()


# Create the A2A Server
server = Server()


# Set up the input form
task = TextField(type="text", id="task", label="Task", required=True, col_span=2, placeholder="Enter your request here")
company_name = TextField(type="text", id="company_name", label="Company name", col_span=1, placeholder="optional")
event_date = DateField(type="date", id="event_date", label="Event date", col_span=1)
event = TextField(type="text", id="event", label="Event", col_span=1)

style = MultiSelectField(
    type="multiselect",
    id="style",
    label="Style",
    required=True,
    col_span=1,
    options=[
        OptionItem(id="detailed", label="detailed"),
        OptionItem(id="summary", label="summary"),
        OptionItem(id="list", label="list"),
    ],
    default_value=["summary"],
)

form_render = FormRender(
    id="conference_prep_form",
    title="How can I help you prepare for your upcoming conference?",
    columns=2,
    fields=[task, company_name, style, event, event_date],
)
form_extension_spec = FormExtensionSpec(form_render)

# ## 4️⃣ Tools: Enabling LLMs to Take Action
# 
# What Are Tools?
# Tools are external capabilities that extend your agent beyond just generating text. They can be API calls, code, or even calls to other AI models. They can allow agents to:
# 
# - Access real-time data (internet search, API calls to live data)
# - Perform calculations (using code generation tools)
# - Interact with APIs (databases, web services)
# - Process files (call functions that read, modify, or write files)
# - Interact with `MCP Servers`
# 
# The BeeAI framework provides [built in tools](https://framework.beeai.dev/modules/tools#built-in-tools) for common tool types, but also provides the ability to create [custom tools](https://framework.beeai.dev/modules/tools#creating-custom-tools).

# ### Adding Framework Provided Tools

# The **Think tool** encourages a Re-Act pattern where the agent reasons and plans before calling a tool.
think_tool = ThinkTool()

# The **DuckDuckGoSearchTool** is a Web Search tool that provides relevant data from the internet to the LLM
search_tool = DuckDuckGoSearchTool()

# ### Adding Custom Tools

# There are 2 ways to provide custom tools to your agent. For simple tools you can use the `@tool` decorator above the function. For more complex tools, you can extend the `Tool Class` and customize things such as the run time and tool execution.  
# We will create a simple custom tool with the `@tool` decorator. Our tool must have a doc string, so that the agent understands when and how it should use that tool. The tool name will defualt to the function name.
# To learn more about advanced tool customization, take a look at this section in the [documentation](https://framework.beeai.dev/modules/tools#advanced-custom-tool).


@tool
async def wikipedia_tool(task: str) -> str:
    """
    Search factual and historical information, including biography, history, politics, geography, society, culture,
    science, technology, people, animal species, mathematics, and other subjects.

    Args:
        task: The topic or question to search for on Wikipedia.

    Returns:
        The information found via searching Wikipedia.
    """
    full_text = False
    language = "en"
    tool = WikipediaTool(language=language)
    response = await tool.run(input=WikipediaToolInput(query=task, full_text=full_text))
    return response.get_text_content()


# ## 5️⃣ Creating a RAG (Retrieval Augmented Generation) Tool to Search Internal Documents

# `RAG` (Retrieval-Augmented Generation) is “search + write”: you ask a question, the system retrieves the most relevant snippets from an indexed knowledge base (via embeddings) and the model composes an answer grounded in those snippets.
# 
# **We created synthetic (made-up) documents to simulate a company knowledge base:**
# - Security checklists
# - Call notes
# - Artifacts
# 
# We made sets of these for Spotify, Siemens, and Moderna.
# 
# **Important:** This is demonstration-only data and does not reflect real information about those companies.

# The BeeAI Framework has built in abstractions to make RAG simple to implement. Read more about it [here](https://framework.beeai.dev/modules/rag).

# First, we must pull an embedding model which converts text into numerical vectors so we can compare meanings and retrieve the most relevant snippets. The original document is:
# 1. preprocessed (cleaned + broken into chunks)
# 2. ran through the embedding algorithm
# 3. stored in the vector database
# 


async def get_vector_store():
    # ### *❗* Exercise: Internal documents
    # Take a look at the internal documents, so you know what type of questions to ask your agent
    #
    # Load the document using the `DocumentLoader` and split the document into chunks using the `text_splitter`.
    loader = DocumentLoader.from_name(
        name="langchain:UnstructuredMarkdownLoader", file_path="rag_conference_prep_agent.txt"
    )
    try:
        documents = await loader.load()
    except Exception as e:
        print(f"Failed to load documents: {e}")
        raise
    # Split documents into chunks
    text_splitter = TextSplitter.from_name(
        name="langchain:RecursiveCharacterTextSplitter", chunk_size=1000, chunk_overlap=200
    )
    documents = await text_splitter.split_documents(documents)
    print(f"Loaded {len(documents)} document chunks")

    # Create the `TemporalVectorStore`, which means this vector store also tracks time.
    # Create vector store and add documents
    vector_store = VectorStore.from_name(name="beeai:TemporalVectorStore", embedding_model=embedding_model)
    await vector_store.add_documents(documents=documents)
    print("Vector store populated with documents")
    return vector_store


# ## 6️⃣ Conditional Requirements: Guiding Agent Behavior
# 

def extract_citations(output) -> list[Citation]:
    """Extract citations from markdown-style links and return cleaned text."""

    citations = []

    try:
        for o in output:
            output = o
            url = output.get("url")
            title = output.get("title")
            description = output.get("description")

            if url and title and description:
                citations.append(Citation(url=url, title=title, description=description, start_index=-1, end_index=-1))
    except Exception:
        pass

    return citations


# ##  7️⃣ Assemble Your Reliable BeeAI Agent

# This is the part we've been working towards! Let's assemble the agent with all the parts we created.

# Add the server decorator with the agent detail + capabilities as required by A2A
agent_detail_extension_spec = beeai_sdk.a2a.extensions.AgentDetailExtensionSpec(
    params=beeai_sdk.a2a.extensions.AgentDetail(
        interaction_mode="multi-turn",
        tools=[
            AgentDetailTool(
                name="Wikipedia Search",
                description="Fetches summaries and information from Wikipedia articles.",
            ),
            AgentDetailTool(
                name="Web Search (DuckDuckGo)",
                description="Retrieves real-time search results from the web.",
            ),
            AgentDetailTool(
                name="Custom Internal Document Search",
                description="Searches internal documents leveraging BeeAI VectorStoreSearchTool.",
            ),
        ],
        framework="BeeAI",
        programming_language="Python",
        author=AgentDetailContributor(name="BeeAI contributors"),
        license="Apache 2.0",
    )
)


@server.agent(
    name=AGENT_NAME,
    capabilities=AgentCapabilities(
        streaming=True,
        push_notifications=True,
        state_transition_history=False,
        extensions=[
            *form_extension_spec.to_agent_card_extensions(),
            *agent_detail_extension_spec.to_agent_card_extensions(),
        ],
    ),
)
# Create the function for the BeeAI Agent
async def agent(
    input: Message,
    trajectory: Annotated[TrajectoryExtensionServer, TrajectoryExtensionSpec()],
    citation: Annotated[CitationExtensionServer, CitationExtensionSpec()],
    form: Annotated[
        FormExtensionServer,
        form_extension_spec,
    ],
):
    """
    Conference Prep Agent intelligently combines multiple information sources to provide comprehensive conference preparation materials.

    The agent will integrate three powerful tools:

    * Web Search – Collect relevant news and up-to-date information about attendees, speakers, and industry trends
    * Wikipedia Tool – Provide company history and background details on organizations and key people
    * Internal Knowledge Base – Access the team's internal notes and artifacts for context-specific information
    """


    # yield trajectory.trajectory_metadata(title="Setup", content="Using SummarizeMemory()")
    # memory = SummarizeMemory(llm)
    from beeai_framework.memory import SlidingMemory, SlidingMemoryConfig

    yield trajectory.trajectory_metadata(title="Setup", content="Using sliding memory... ")
    memory = SlidingMemory(SlidingMemoryConfig(
        size=3,
        handlers={"removal_selector": lambda messages: messages[0]}  # Remove the oldest message
    ))

    yield trajectory.trajectory_metadata(title="Setup", content="Loading internal documents in vector store... ")

    # Create the `internal_document_search` tool! Because the `VectorStoreSearchTool` is a built in tool wrapper, we don't need to use the `@tool` decorator or extend the custom `Tool class`.
    # Create the vector store search tool
    internal_document_search = VectorStoreSearchTool(vector_store=await get_vector_store())

    yield trajectory.trajectory_metadata(title="Setup", content="Processing form input... ")
    try:
        # Form
        parsed_form = form.parse_form_response(message=input)
        values = parsed_form.model_dump(exclude_none=True)["values"]
        styles = values.get("style", {"value": ["summary"]})["value"]
        style = styles[0] if styles else "summary"
        task = str(values)
    except Exception:
        # Message from CLI
        task = get_message_text(input)
        style = "summary"

    yield trajectory.trajectory_metadata(title="Setup", content=f"Setting style: {style}... ")

    todays_date = date.today().strftime("%B %d, %Y")
    instruct_prompt = f"""You help field marketing teams prep for conferences by answering questions on companies that they need to prepare to talk to. You produce quick and actionable briefs, doing your best to anwer the user's question.

    Today's date is {todays_date}.

    Tools:
    - ThinkTool: Helps you plan and reason before you act. Use this tool when you need to think.
    - DuckDuckGoSearchTool: Use this tool to collect current information on agendas, speakers, news, competitor moves. Include title + date + link to the resources you find in your answer. Do not use this tool for internal notes or artifacts.
    - wikipedia_tool: Use this tool to get company/org history (not for breaking news). Only look up company names as the input.
    - internal_document_search: past meetings, playbooks, artifacts. If you use information from this in your response, label it as as [Internal]. Always use this tool when internal notes or content is references.

    Basic Rules:
    - Be concise and practical. Requested style for final output is: {style}.
    - Favor recent info (agenda/news ≤30 days; exec changes/funding ≤180 days); flag older items.
    - If you don't know, say so. Don't make things up.
    """

    # What Are Conditional Requirements?
    # [Conditional requirements](https://framework.beeai.dev/experimental/requirement-agent#conditional-requirement) ensure your agents are reliable by controlling when and how tools are used. They're like business rules for agent behavior. You can make them as strict (esentially writing a static workflow) or flexible (no rules! LLM decides) as you'd like.
    #
    # The rules that you enforce may seem simple in the BeeAI framework, but in other frameworks they require ~5X the amount of code. Check out this [blog](https://beeai.dev/blog/reliable-ai-agents) where we built the same agent in BeeAI and other agent framework LangGraph.

    # These conditional requirements enforce the following in only 3 lines of code:
    # 1. The agent must call the think tool as the first tool call. It is not allowed to call it consecutive times in a row.
    # 2. The wikipedia_tool can only be called after the think tool, but not consecutively. It has a relative priority of 10.
    # 3. The DuckDuckGo Internet search tool can also only be called after the Think tool, it is allowed to be called up to 3 times, it must be invoked at least once, and it has a relative priority of 15.
    # 4. The internal_document_search tool can only be called after the think tool, it is allowed to be called multiple times in a row, it must be called at least once, and it has a relative priority of 20.
    #
    #

    yield trajectory.trajectory_metadata(title="Setup", content="Defining tool usage requirements for agent... ")
    requirement_1 = ConditionalRequirement(ThinkTool, consecutive_allowed=False, force_at_step=1)
    requirement_2 = ConditionalRequirement(wikipedia_tool, only_after=ThinkTool, consecutive_allowed=True,
                                           priority=10, )
    requirement_3 = ConditionalRequirement(DuckDuckGoSearchTool, only_after=ThinkTool, consecutive_allowed=True,
                                           min_invocations=1, max_invocations=3, priority=15, )
    requirement_4 = ConditionalRequirement(internal_document_search, only_after=ThinkTool, consecutive_allowed=True,
                                           min_invocations=1, priority=20, )

    requirement_agent = RequirementAgent(
        llm=llm,
        instructions=instruct_prompt,
        memory=memory,
        tools=[ThinkTool(), DuckDuckGoSearchTool(), wikipedia_tool, internal_document_search],
        requirements=[
            requirement_1,
            requirement_2,
            requirement_3,
            requirement_4
        ],
        # Log intermediate steps to the console
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
    )

    final_answer = None

    yield trajectory.trajectory_metadata(title="Execution", content=f"Running agent with task: {task}")
    citations = []
    async for event, meta in requirement_agent.run(task, max_retries_per_step=3, total_max_retries=15):

        if not isinstance(event, RequirementAgentSuccessEvent):
            continue

        last_step = event.state.steps[-1] if event.state.steps else None
        if last_step and last_step.tool is not None:

            output = to_json_serializable(last_step.output)
            citations.extend(extract_citations(output))

            yield trajectory.trajectory_metadata(
                title=last_step.tool.name,
                content=json.dumps(
                    {
                        "input": last_step.input,
                        "output": output,
                        "error": to_json_serializable(last_step.error),
                    }
                )
            )

        if event.state.answer is not None:
            final_answer = event.state.answer

    if final_answer:
        text = final_answer.text
        if citations:
            # Add separator because we will cite them all at the end instead of inline
            # because these are just searched docs and not annotated inline references.
            text = text + "\n\n---\n\n### Search sources:  "
        message = AgentMessage(
            text=text,
            metadata=(citation.citation_metadata(citations=citations) if citations else None),
        )
        yield message


async def cli_agent(question: str):
    """Run an async agent with a question, await and return the result"""

    async for x in agent(AgentMessage(text=question),
                         trajectory=TrajectoryExtensionServer(TrajectoryExtensionSpec()),
                         citation=CitationExtensionServer(CitationExtensionSpec()),
                         form=FormExtensionServer(form_extension_spec)):
        print("AGENT RESPONSE: ", x)


def serve():
    """Start a server that runs the agent"""
    PORT = os.environ.get("PORT")
    if PORT is None:
        server.run(
            configure_telemetry=True,
            # context_store=PlatformContextStore(),
        )  # Default port is 10000
    else:
        # Assign configured port
        # Note: 0=auto-assign but that is not supported for BeeAI Platform registration
        server.run(
            port=int(PORT),
            configure_telemetry=True,
            # context_store=PlatformContextStore(),
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"RUNNING '{AGENT_NAME}' CLI:")
        asyncio.run(cli_agent(sys.argv[1]))
    else:
        print(f"SERVING '{AGENT_NAME}'")
        serve()

# ### *❗* Exercise: Test Your Agent
# Remember that your agent is meant to prep the field marketing team for upcoming conferences and has a limited set of "internal documents". Make up your own question or ask one of the sample ones below!
#
# **Sample Questions:**
# - Brief me for a Shopify event at the conference. Give me an overview of the company, some recent news about them, and anything important I need to know from our internal notes.
#
# - I'm planning on meeting the Moderna rep at the next conference. Give me a one pager and remind me where we left off on previous discussions.
#
# - Build a security talking sheet for Siemens Energy. How does their strategy compare to their competitors'?

