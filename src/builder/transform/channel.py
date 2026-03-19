"""Community, Site, and Forum hierarchy construction."""

import json

from builder.config import CHANNEL_FILE, channel_uri, forum_uri, site_uri
from builder.models import Community, Forum, Site


def make_community(channel_id: int) -> Community:
    """Create a Community, enriched from channel.json if available."""
    name = None
    description = None

    if CHANNEL_FILE.exists():
        with open(CHANNEL_FILE, "r", encoding="utf-8") as f:
            meta = json.load(f)
        name = meta.get("title")
        description = meta.get("about")

    return Community(
        id=channel_uri(channel_id),
        name=name,
        description=description,
        has_part=site_uri(),
    )


def make_site() -> Site:
    """Create the Telegram Site entity."""
    return Site(
        id=site_uri(),
        name="Telegram",
    )


def make_supergroup_forum(channel_id: int, name: str | None = None) -> Forum:
    """Create the top-level Forum for a supergroup (organizational, not a chat channel)."""
    return Forum(
        id=forum_uri(channel_id),
        name=name,
        has_host=site_uri(),
    )


def make_topic_forum(
    channel_id: int,
    topic_id: int,
    name: str | None = None,
    closed: bool = False,
) -> Forum:
    """Create a child Forum for a topic channel within a supergroup."""
    return Forum(
        id=forum_uri(channel_id, topic_id),
        name=name,
        has_host=site_uri(),
        has_parent_forum=forum_uri(channel_id),
        closed=closed if closed else None,
    )
