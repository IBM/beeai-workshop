#Framework imports
from beeai_framework.adapters.openai import OpenAIChatModel
from beeai_framework.backend import UserMessage, SystemMessage

#ACP SDK imports
from acp_sdk.models import Message
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator
#Helper imports     
from helpers import package_response, flatten_messages
from typing import List, Optional
import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

#load environment variables
load_dotenv()

# Set up the ACP server
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


@server.agent()
async def ticket_triage_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
        """ An agent that classifies customer support tickets.
        """
        user_prompt = flatten_messages(input[-1:])
        model_name = os.getenv("MODEL_NAME", "gpt-4.1-mini-2025-04-14")
        llm = OpenAIChatModel(model_name)
        system_msg = SystemMessage(
             """
            You are “Support-Sensei,” an AI assistant that must:
            1. Choose the single best ticket category.
            2. Extract the required fields.
            """
        )
        response = await llm.create_structure(
            schema=TicketClassifierOutput,
            messages=[system_msg, UserMessage(user_prompt)],
        )
        yield package_response(response.object)


def run():
    server.run(port=int(os.getenv("PORT", 8000)))


if __name__ == "__main__":
    run()