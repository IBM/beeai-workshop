import textwrap
import os

# Pydantic Framework
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# ACP SDK
from acp_sdk import Metadata
from acp_sdk.models import Message
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator

# Helpers
from helpers import package_response

# Set up the ACP server
server = Server()


@server.agent(metadata=Metadata(ui={"type": "hands-off"}))
async def ticket_response_agent(
    input: list[Message],
) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    An agent that responds to customer support tickets .
    """
    model = OpenAIModel(
        "dummy", provider=OpenAIProvider(base_url="http://localhost:8333/api/v1/llm")
    )
    TicketResponseAgent = Agent(
        model=model,
        system_prompt=(
            textwrap.dedent(
                """\
                You are a helpful customer support agent that creates clear, helpful, human-sounding replies to a customer.
                Tone & Style Matrix:
                Category   | Primary Tone             | Secondary Goals
                Billing    | Efficient, courteous     | Reassure accuracy, outline next steps, offer quick resolution
                Technical  | Clear, solution-oriented | Provide concise troubleshooting or escalation info
                Complaint  | Empathetic, apologetic   | Acknowledge feelings, accept responsibility where appropriate, explain corrective action
                Account    | Professional, supportive | Clarify account status or changes, confirm security measures
                Feedback   | Appreciative, receptive  | Thank the customer, highlight how feedback is used
                Other      | Warm, helpful            | Clarify intent, offer assistance
                """
            )
        ),
    )
    response = await TicketResponseAgent.run(str(input[-1]))

    yield package_response(response.output)


# Run these agents on different ports
def run():
    server.run(port=int(os.getenv("PORT", 8001)))


if __name__ == "__main__":
    run()
