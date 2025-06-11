# ACP SDK
from acp_sdk import Metadata
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Server, Context
from collections.abc import AsyncGenerator
from acp_sdk.client import Client

# Helpers
import os

# set up the ACP server
server = Server()


# Main ACP Agent that orchestrates the workflow
async def run_agent(agent: str, input: str) -> list[Message]:
    async with Client(base_url="http://localhost:8333/api/v1/acp") as client:
        run = await client.run_sync(
            agent=agent,
            input=[
                Message(parts=[MessagePart(content=input, content_type="text/plain")])
            ],
        )
    return run.output


@server.agent(metadata=Metadata(ui={"type": "hands-off"}))
async def ticket_workflow_agent(
    input: list[Message], context: Context
) -> AsyncGenerator:
    """
    Main agent that orchestrates the ticket triage and response workflow.
    """
    ticket_triage_response = await run_agent("ticket_triage_agent", str(input))
    ticket_response_to_user = await run_agent(
        "ticket_response_agent", str(ticket_triage_response)
    )

    yield str(ticket_response_to_user[0])


def run():
    server.run(port=int(os.getenv("PORT", 8002)))


if __name__ == "__main__":
    run()
