"""Community/channel object creation."""

from builder.config import channel_uri
from builder.models import Community


def make_community(channel_id: int) -> Community:
    """Create a Community for a Telegram channel ID."""
    return Community(id=channel_uri(channel_id))
