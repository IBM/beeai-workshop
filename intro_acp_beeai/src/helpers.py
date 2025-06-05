from typing import List, Dict
from datetime import datetime, timezone
from acp_sdk.models import Message, MessagePart
import json

def flatten_messages(messages: List[Message]) -> str:
    """
    Collapse the *text/plain* content of an entire Message list into one string.

    * If you only care about the first/last message you can slice before calling.
    * Non-plain parts (images, files, etc.) are ignored, mirroring Message.__str__.
    """
    if not messages:
        return ""

    # join in chronological order
    return "".join(
        part.content
        for m in messages
        for part in m.parts
        if part.content_type == "text/plain" and part.content is not None
    ).strip()

def package_response(data: str | dict) -> Dict[str, List[Message]]:
    if isinstance(data, dict):          # auto-convert
        data = json.dumps(data, separators=(",", ":"))
    assistant_message = Message(
        parts=[MessagePart(content=data)],
        created_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
    )
    return {"messages": [assistant_message]}
