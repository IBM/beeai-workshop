from datetime import datetime, timezone
from acp_sdk.models import Message, MessagePart
import json


def package_response(data: str | dict) -> Message:
    if isinstance(data, dict):  # auto-convert
        data = json.dumps(data, separators=(",", ":"))
    assistant_message = Message(
        parts=[MessagePart(content=data)],
        created_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
    )
    return assistant_message
