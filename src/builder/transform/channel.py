"""Community/channel object creation."""

import json

from builder.config import CHANNEL_FILE, channel_uri
from builder.models import Community


def make_community(channel_id: int) -> Community:
    """Create a Community for a Telegram channel ID, enriched from channel.json if available."""
    name = None
    description = None
    member_count = None

    if CHANNEL_FILE.exists():
        with open(CHANNEL_FILE, "r", encoding="utf-8") as f:
            meta = json.load(f)
        name = meta.get("title")
        description = meta.get("about")
        member_count = meta.get("members_count")

    return Community(
        id=channel_uri(channel_id),
        name=name,
        description=description,
        member_count=member_count,
    )
