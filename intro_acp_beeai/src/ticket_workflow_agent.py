import textwrap

#Framework imports
from beeai_framework.adapters.openai import OpenAIChatModel
from beeai_framework.backend import UserMessage, SystemMessage
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
#ACP SDK
from acp_sdk import Annotations, Metadata, PlatformUIAnnotation
from acp_sdk.models import Message, MessagePart
from acp_sdk.models.platform import PlatformUIType
from acp_sdk.server import RunYield, RunYieldResume, Server, Context
from collections.abc import AsyncGenerator
from acp_sdk.client import Client
#Helpers
from helpers import package_response, flatten_messages
from pydantic import BaseModel, Field
from typing import List, Optional
import os
#load environment variables
from dotenv import load_dotenv
load_dotenv()

#set up the ACP server
server = Server()

class TicketClassifierOutput(BaseModel):
    """Structured payload returned by the LLM for a single ticket."""
    category: List[str] = Field(
        description="Options: Billing, Technical, Complaint, Account, Feedback, Other"
    )
    customer_name: Optional[str] = Field(
        default=None,
        description="Full customer name; null if not mentioned."
    )
    account_id: Optional[str] = Field(
        default=None,
        description="Exact account identifier as it appears in the ticket."
    )
    product: Optional[str] = Field(
        default=None,
        description="Product/SKU referenced in the ticket."
    )
    issue_summary: str = Field(
        description="concise plain-language summary of the problem, extracting key insights."
    )
    severity: str = Field(
        description='One of: "critical", "high", "medium", "low".'
    )
    sentiment: str = Field(
        description='One of: "negative", "neutral", "positive".'
    )
    incident_date: Optional[str] = Field(
        default=None,
        description="ISO-8601 date (YYYY-MM-DD) if provided."
    )


#make Agents ACP Compatible

@server.agent(
    name="ticket_triage_agent",
    metadata=Metadata(
        annotations=Annotations(
            beeai_ui=PlatformUIAnnotation(
                ui_type=PlatformUIType.HANDSOFF,
                user_greeting="How can I help you?",
            ),
        ),
    ),
)
async def ticket_triage_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """An agent that classifies customer support tickets."""
    user_prompt = flatten_messages(input[-1:])
    model_name = os.getenv("MODEL_NAME", "gpt-4.1-mini-2025-04-14")
    llm = OpenAIChatModel(model_name)
    system_msg = SystemMessage(textwrap.dedent("""
        You are “Support-Sensei,” an AI assistant that must:
        1. Choose the single best ticket category.
        2. Extract the required fields.
        """)
    )
    response = await llm.create_structure(
        schema=TicketClassifierOutput,
        messages=[system_msg, UserMessage(user_prompt)],
    )
    yield str(response.object)


@server.agent(
    name="ticket_response_agent",
    metadata=Metadata(
        annotations=Annotations(
            beeai_ui=PlatformUIAnnotation(
                ui_type=PlatformUIType.HANDSOFF,
                user_greeting="Enter triaged ticket details to get a response.",
            ),
        ),
    ),
)
async def ticket_response_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    An agent that responds to customer support tickets .
    """
    user_prompt = flatten_messages(input)

    model = os.getenv("MODEL_NAME", "gpt-4.1-mini-2025-04-14")
    model = OpenAIModel(model, provider=OpenAIProvider(api_key=os.getenv('OPENAI_API_KEY')))
    TicketResponseAgent = Agent( model=model,
                            system_prompt=(textwrap.dedent("""
                                           You are a helpful customer support agent that creates clear, helpful, human-sounding replies to a customer.
                                           Tone & Style Matrix:
                                            Category   | Primary Tone        | Secondary Goals
                                            Billing    | Efficient, courteous | Reassure accuracy, outline next steps, offer quick resolution
                                            Technical  | Clear, solution-oriented | Provide concise troubleshooting or escalation info
                                            Complaint  | Empathetic, apologetic | Acknowledge feelings, accept responsibility where appropriate, explain corrective action
                                            Account    | Professional, supportive | Clarify account status or changes, confirm security measures
                                            Feedback   | Appreciative, receptive | Thank the customer, highlight how feedback is used
                                            Other      | Warm, helpful        | Clarify intent, offer assistance
                                           """)))
    response = await TicketResponseAgent.run(user_prompt)
    
    yield str(response.output)


#Main ACP Agent that orchestrates the workflow
async def run_agent(agent: str, input: str) -> list[Message]:
    async with Client(base_url="http://localhost:8000") as client:
        run = await client.run_sync(
            agent=agent, input=[Message(parts=[MessagePart(content=input, content_type="text/plain")])]
        )
    return run.output


@server.agent(
    name="TicketWorkflow",
    metadata=Metadata(
        annotations=Annotations(
            beeai_ui=PlatformUIAnnotation(
                ui_type=PlatformUIType.HANDSOFF,
                user_greeting="How can I help you?",
            ),
        ),
    ),
)
async def main_agent(input: list[Message], context: Context) -> AsyncGenerator:
    """
    Main agent that orchestrates the ticket triage and response workflow.
    """
    ticket_triage_response = await run_agent("ticket_triage_agent", str(input))
    if not ticket_triage_response:
        raise Exception("Empty response from ticket triage agent")
    yield str(ticket_triage_response[0])

    ticket_response_to_user = await run_agent("ticket_response_agent", str(ticket_triage_response))
    if not ticket_response_to_user:
        raise Exception("Empty response from ticket response agent")
    yield str(ticket_response_to_user[0])

#Run these agents
def run():
    server.run()


if __name__ == "__main__":
    run()
