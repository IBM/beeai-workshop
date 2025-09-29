# Copyright 2025 © BeeAI a Series of LF Projects, LLC
# SPDX-License-Identifier: Apache-2.0

# # Welcome to the BeeAI Framework Workshop 🐝
#
# 🎯 Scenario: The Field Marketing Lead has asked you to help prepare their team for conference season. You create a Conference Prep Agent that uses 3 tools: web search to collect relevant news and search for up to date information, Wikipedia to provide company history and details, and the team's internal notes and artifacts.

# 📚 What You'll Learn
# 
# - BeeAI Platform -
# - BeeAI Framework - see the notebook first and then use this for platform auto-registration
# - A2A - BeeAI SDK makes it easy to work with A2A
# - Forms - BeeAI Platform makes it easy to create input forms for the UI

# ...
# - System Prompts - The foundation of agent behavior
# - RequirementAgent - BeeAI's powerful agent implementation that provides control over agent behavior
# - LLM Providers - Local and hosted model options
# - Memory Systems - Maintaining conversation context
# - Tools Integration - Extending agent capabilities
# - Conditional Requirements - Enforcing business logic and rules
# - Observability - Monitoring and debugging agents

# ## 🔧 Setup
# First, let's install the BeeAI Framework and set up our environment.
# 
# - setting up the observability so we can capture and log the actions our agent takes
# - getting the "internal documents"


# System
import asyncio
from datetime import date
import logging
import os
import sys
from typing import Annotated

# Third party
from a2a.types import AgentCapabilities
from a2a.utils.message import get_message_text
from dotenv import load_dotenv
from openinference.instrumentation.beeai import BeeAIInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from openinference.semconv.resource import ResourceAttributes

# BeeAI Framework imports
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
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
from beeai_sdk.a2a.extensions import AgentDetail, AgentDetailExtensionSpec
from beeai_sdk.a2a.extensions import ui
from beeai_sdk.a2a.types import Message, AgentMessage
from beeai_sdk.server import Server
from beeai_sdk.server.context import RunContext
from beeai_sdk.server.store.platform_context_store import PlatformContextStore

# Constants
AGENT_NAME = "Conference planner"

# Read .env and set environment variables
load_dotenv()

# Logging

## Hide some noise
logging.getLogger("opentelemetry.exporter.otlp.proto.http").setLevel(logging.CRITICAL)
logging.getLogger("opentelemetry.exporter.otlp.proto.http._log_exporter").setLevel(
    logging.CRITICAL
)
logging.getLogger("opentelemetry.exporter.otlp.proto.http.metric_exporter").setLevel(
    logging.CRITICAL
)
logger = logging.getLogger(__name__)

#  ## 1️⃣ LLM Providers: Choose Your AI Engine

# BeeAI Framework supports 10+ LLM providers including Ollama, Groq, OpenAI, Watsonx.ai, and more, giving you flexibility to choose local or hosted models based on your needs. In this workshop we'll be working Ollama, so you will be running the model locally. You can find the documentation on how to connect to other providers [here](https://framework.beeai.dev/modules/backend).
# ### *❗* Exercise: Select your Language Model Provider
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

# Create the A2A Server
server = Server()

# Set up the input form
query = ui.form.TextField(type="text", id="query", label="query", required=True, col_span=2)
customer_name = ui.form.TextField(type="text", id="customer_name", label="Customer name", col_span=1)
account_id = ui.form.TextField(type="text", id="account_id", label="Account ID", col_span=1)
product = ui.form.TextField(type="text", id="product", label="Product", col_span=2)
incident_date = ui.form.DateField(type="date", id="incident_date", label="Incident date", col_span=1)

severity = ui.form.MultiSelectField(
    type="multiselect",
    id="severity",
    label="Severity",
    required=False,
    col_span=1,
    options=[
        ui.form.OptionItem(id="critical", label="critical"),
        ui.form.OptionItem(id="high", label="high"),
        ui.form.OptionItem(id="medium", label="medium"),
        ui.form.OptionItem(id="low", label="low"),
    ],
    default_value=["medium"],
)

sentiment = ui.form.MultiSelectField(
    type="multiselect",
    id="sentiment",
    label="Sentiment",
    required=False,
    col_span=1,
    options=[
        ui.form.OptionItem(id="negative", label="negative"),
        ui.form.OptionItem(id="neutral", label="neutral"),
        ui.form.OptionItem(id="positive", label="positive"),
    ],
    default_value=["neutral"],
)

category = ui.form.MultiSelectField(
    type="multiselect",
    id="category",
    label="Category",
    required=False,
    col_span=2,
    options=[
        ui.form.OptionItem(id="billing", label="billing"),
        ui.form.OptionItem(id="technical", label="technical"),
        ui.form.OptionItem(id="complaint", label="complaint"),
        ui.form.OptionItem(id="account", label="account"),
        ui.form.OptionItem(id="feedback", label="feedback"),
        ui.form.OptionItem(id="other", label="other"),
    ],
)
notes = ui.form.FileField(type="file", id="notes", label="Upload notes", accept=["text/*"], required=False, col_span=2)

form_render = ui.form.FormRender(
    id="ticket_form",
    title="Question",
    columns=2,
    fields=[
        query,
        category,
        customer_name, account_id,
        severity, sentiment,
        product, incident_date
    ],
)
form_extension_spec = ui.form.FormExtensionSpec(form_render)


# ## 2️⃣ Understanding System Prompts: The Agent's Foundation

# What is a System Prompt?
# A system prompt is the foundational instruction that defines your agent's identity, role, and behavior. Think of it as the agent's "job description" and "training manual" rolled into one. Each model responds differently to the same system prompt, so experimentation is necessary.
# 
# Some key components of a strong system prompt:
# 
# - Identity: Who is the agent?
# - Role: What is their function?
# - Context: What environment are they operating in?
# - Rules: What constraints and guidelines must they follow?
# - Knowledge: What domain-specific information do they need?

# ###*❗* Exercise: Customize Your System Prompt
# Try modifying the system prompt. Customize the "basic rules" section to add your own. Note that changes to the system prompt will affect the performance of the model. Creating a great `System Prompt` is an art, not a science.

todays_date = date.today().strftime("%B %d, %Y")
instruct_prompt = f"""You help field marketing teams prep for conferences by answering questions on companies that they need to prepare to talk to. You produce quick and actionable briefs, doing your best to anwer the user's question.

Today's date is {todays_date}.

Tools:
- ThinkTool: Helps you plan and reason before you act. Use this tool when you need to think.
- DuckDuckGoSearchTool: Use this tool to collect current information on agendas, speakers, news, competitor moves. Include title + date + link to the resources you find in your answer. Do not use this tool for internal notes or artifacts.
- wikipedia_tool: Use this tool to get company/org history (not for breaking news). Only look up company names as the input.
- internal_document_search: past meetings, playbooks, artifacts. If you use information from this in yoour response, label it as as [Internal]. Always use this tool when internal notes or content is references.

Basic Rules:
- Be concise and practical.
- Favor recent info (agenda/news ≤30 days; exec changes/funding ≤180 days); flag older items.
- If you don't know, say so. Don't make things up.
"""


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
async def wikipedia_tool(query: str) -> str:
    """
    Search factual and historical information, including biography, history, politics, geography, society, culture,
    science, technology, people, animal species, mathematics, and other subjects.

    Args:
        query: The topic or question to search for on Wikipedia.

    Returns:
        The information found via searching Wikipedia.
    """
    full_text = False
    language = "en"
    tool = WikipediaTool(language=language)
    response = await tool.run(input=WikipediaToolInput(query=query, full_text=full_text))
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

# ## Explore Observability: See what is happening under the hood

# Create the function that sets up observability using `OpenTelemetry` and [Arize's Phoenix Platform](https://arize.com/docs/phoenix/inferences/how-to-inferences/manage-the-app). There a several ways to view what is happening under the hood of your agent. View the observability documentation [here](https://framework.beeai.dev/modules/observability).

def setup_observability(endpoint: str = "http://localhost:6006/v1/traces") -> None:
    """
    Sets up OpenTelemetry with OTLP HTTP exporter and instruments the beeai framework.
    """
    # Temporary instrument fix
    EventMeta.model_fields["context"].exclude = True


    # resource = Resource(attributes={})
    resource = Resource(attributes={
        ResourceAttributes.PROJECT_NAME: 'Intro to BeeAI workshop'
    })

    BeeAIInstrumentor().instrument()


# Enable OpenTelemetry integration
setup_observability("http://localhost:6006/v1/traces")


# ##  7️⃣ Assemble Your Reliable BeeAI Agent

# This is the part we've been working towards! Let's assemble the agent with all the parts we created.

# Add the server decorator with the agent detail + capabilities as required by A2A
agent_detail_extension_spec = AgentDetailExtensionSpec(
    params=AgentDetail(
        interaction_mode="multi-turn",
    )
)

from typing import Annotated
from beeai_sdk.a2a.extensions import TrajectoryExtensionServer, TrajectoryExtensionSpec


@server.agent(
    name=AGENT_NAME,
    detail=AgentDetail(
        ui_type="hands-off",
        user_greeting="Provide your triaged ticket details",
        framework="BeeAI",
        license="Apache 2.0",
        language="Python",
    ),
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
        form: Annotated[ui.form.FormExtensionServer, form_extension_spec]
):

    yield trajectory.trajectory_metadata(title="Setup", content="memory...")

    memory = SummarizeMemory(llm)

    yield trajectory.trajectory_metadata(title="Setup", content="Loading internal documents...")

    # Create the `internal_document_search` tool! Because the `VectorStoreSearchTool` is a built in tool wrapper, we don't need to use the `@tool` decorator or extend the custom `Tool class`.
    # Create the vector store search tool
    internal_document_search = VectorStoreSearchTool(vector_store=await get_vector_store())

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

    try:
        # Form
        parsed_form = form.parse_form_response(message=input)
        query = str(parsed_form.dict()["values"])  # TODO: Turn form values into query
    except ValueError as ve:
        # Message from CLI
        query = get_message_text(input)

    response = await requirement_agent.run(query, max_retries_per_step=3, total_max_retries=15)
    print("FULL RESPONSE: ", response)
    answer = response.last_message.text

    print("QUESTION: ", query)
    print("ANSWER: ", answer)
    yield answer


# ### *❗* Exercise: Test Your Agent
# Remember that your agent is meant to prep the field marketing team for upcoming conferences and has a limited set of "internal documents". Make up your own question or ask one of the sample ones below!
# 
# 
# **Sample Questions:**
# - Brief me for a Shopify meeting at the conference. Give me an overview of the company, some recent news about them, and anything important I need to know from our internal notes.
# 
# - I'm planning on meeting the Moderna rep at the next conference. Give me a one pager and remind me where we left off on previous discussions.
# 
# - Build a security talking sheet for Siemens Energy. How does their strategy compare to their competitors'?

# Run the agent with specific execution settings.

# ### *❗* Exercise: Test Your Agent
# Change the execution settings and see what happens. Does your agent run out of iterations? Every task is different and its important to balance flexibility with control.

async def cli_agent(question: str):
    """Run an async agent with a question, await and return the result"""

    async for x in agent(AgentMessage(text=question),
                         trajectory=TrajectoryExtensionServer(TrajectoryExtensionSpec()),
                         form=ui.form.FormExtensionServer(form_extension_spec)):
        print("AGENT RESPONSE: ", x)
    # return await agent(AgentMessage(text=question),
                       # trajectory=TrajectoryExtensionServer(TrajectoryExtensionSpec()),
                       # form=ui.form.FormExtensionServer(form_extension_spec))


def serve():
    """Start a server that runs the agent"""
    PORT = os.environ.get("PORT")
    if PORT is None:
        server.run(
            configure_telemetry=True,
            context_store=PlatformContextStore(),
        )  # Default port is 10000
    else:
        # Assign configured port
        # Note: 0=auto-assign but that is not supported for BeeAI Platform registration
        server.run(
            port=int(PORT),
            configure_telemetry=True,
            context_store=PlatformContextStore(),
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"RUNNING '{AGENT_NAME}' CLI:")
        asyncio.run(cli_agent(sys.argv[1]))
    else:
        print(f"SERVING '{AGENT_NAME}'")
        serve()
