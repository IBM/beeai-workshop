import textwrap

# Framework imports
from acp_sdk import Metadata
from beeai_framework.adapters.openai import OpenAIChatModel
from beeai_framework.backend import UserMessage, SystemMessage

# ACP SDK imports
from acp_sdk.models import Message
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator

# Helper imports
from helpers import package_response
from typing import List, Optional
import os
from pydantic import BaseModel, Field

# Set up the ACP server
server = Server()


class TicketClassifierOutput(BaseModel):
    """Structured payload returned by the LLM for a single ticket."""

    category: List[str] = Field(
        description="Options: Billing, Technical, Complaint, Account, Feedback, Other"
    )
    customer_name: Optional[str] = Field(
        default=None, description="Full customer name; null if not mentioned."
    )
    account_id: Optional[str] = Field(
        default=None,
        description="Exact account identifier as it appears in the ticket.",
    )
    product: Optional[str] = Field(
        default=None, description="Product/SKU referenced in the ticket."
    )
    issue_summary: str = Field(
        description="concise plain-language summary of the problem, extracting key insights."
    )
    severity: str = Field(description='One of: "critical", "high", "medium", "low".')
    sentiment: str = Field(description='One of: "negative", "neutral", "positive".')
    incident_date: Optional[str] = Field(
        default=None, description="ISO-8601 date (YYYY-MM-DD) if provided."
    )


@server.agent(metadata=Metadata(ui={"type": "hands-off"}))
async def ticket_triage_agent(
    input: list[Message],
) -> AsyncGenerator[RunYield, RunYieldResume]:
    """An agent that classifies customer support tickets."""
    llm = OpenAIChatModel(
        "dummy", api_key="dummy", base_url="http://localhost:8333/api/v1/llm"
    )
    response = await llm.create(
        messages=[
            SystemMessage(
                textwrap.dedent(
                    """\
                    You are “Support-Sensei,” an AI assistant that must:
                    1. Choose the single best ticket category.
                    2. Extract the required fields.
                    """
                )
            ),
            UserMessage(str(input[-1])),
        ],
    )
    yield package_response(response.get_text_content())


def run():
    server.run(port=int(os.getenv("PORT", 8000)))


if __name__ == "__main__":
    run()
