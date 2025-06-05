import sys
import os
#Pydantic Framework
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
#ACP SDK
from acp_sdk import Metadata
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator
#Helpers
from helpers import package_response, flatten_messages

#load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up the ACP server
server = Server()

@server.agent(
    metadata=Metadata(ui={"type": "hands-off"})
)
async def ticket_response_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    An agent that responds to customer support tickets .
    """
    user_prompt = flatten_messages(input)

    model_name = os.getenv("MODEL_NAME", "gpt-4.1-mini-2025-04-14")
    model = OpenAIModel(model_name)
    TicketResponseAgent = Agent( model=model,
                            system_prompt=("""
                                           You are a helpful customer support agent that creates clear, helpful, human-sounding replies to a customer.
                                           Tone & Style Matrix:
                                            Category   | Primary Tone        | Secondary Goals
                                            Billing    | Efficient, courteous | Reassure accuracy, outline next steps, offer quick resolution
                                            Technical  | Clear, solution-oriented | Provide concise troubleshooting or escalation info
                                            Complaint  | Empathetic, apologetic | Acknowledge feelings, accept responsibility where appropriate, explain corrective action
                                            Account    | Professional, supportive | Clarify account status or changes, confirm security measures
                                            Feedback   | Appreciative, receptive | Thank the customer, highlight how feedback is used
                                            Other      | Warm, helpful        | Clarify intent, offer assistance
                                           """))
    response = await TicketResponseAgent.run(user_prompt)
    
    yield package_response(response.output)

#Run these agents on different ports
def run():
    server.run(port=int(os.getenv("PORT", 8000)))


if __name__ == "__main__":
    run()

