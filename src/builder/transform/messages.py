"""Raw Telegram message dicts → Post objects."""

from typing import Any

from builder.config import channel_uri, message_uri, user_uri
from builder.models import Link, Post, UserAccount
from builder.transform.entities import (
    extract_entities,
    extract_urls,
    normalize_url,
    ordered_dedup,
)


def extract_channel_id(peer_id_obj: Any) -> int | None:
    """Extract numeric channel/chat/user ID from a raw Telegram peer_id object."""
    if not isinstance(peer_id_obj, dict):
        return None
    if "channel_id" in peer_id_obj:
        return int(peer_id_obj["channel_id"])
    if "chat_id" in peer_id_obj:
        return int(peer_id_obj["chat_id"])
    if "user_id" in peer_id_obj:
        return int(peer_id_obj["user_id"])
    return None


def extract_from_user_id(obj: dict) -> int | None:
    """Get the sender's user ID from a raw Telegram message."""
    from_id = obj.get("from_id")
    if isinstance(from_id, dict) and "user_id" in from_id:
        return int(from_id["user_id"])
    return None


def extract_reply_to_msg_id(obj: dict) -> int | None:
    """Get the replied-to message ID, if any."""
    r = obj.get("reply_to")
    if isinstance(r, dict) and "reply_to_msg_id" in r:
        return int(r["reply_to_msg_id"])
    return None


def transform_message(
    raw: dict,
    *,
    expected_channel_id: int,
    users: dict[int, UserAccount],
    links: dict[str, Link],
) -> Post | None:
    """Transform a single raw Telegram message dict into a Post.

    Populates `users` and `links` dicts as side effects (dedup registries).
    Returns None if the message should be skipped.
    """
    ch_id = extract_channel_id(raw.get("peer_id"))
    if ch_id is None:
        return None
    if ch_id != expected_channel_id:
        return None  # MVP: single community per run

    msg_id = raw.get("id")
    created = raw.get("date")
    if msg_id is None or created is None:
        return None

    text = raw.get("message") or ""
    from_user_id = extract_from_user_id(raw)
    reply_to_id = extract_reply_to_msg_id(raw)
    forwards = raw.get("forwards")
    pinned = raw.get("pinned")
    entities_raw = raw.get("entities") or []

    # Creator
    creator_ref: str | None = None
    if from_user_id is not None:
        if from_user_id not in users:
            users[from_user_id] = UserAccount(id=user_uri(from_user_id))
        creator_ref = users[from_user_id].id

    # Entity extraction
    topics, mentions, entity_urls = extract_entities(text, entities_raw)
    topics = ordered_dedup(topics)
    mentions = ordered_dedup(mentions)

    # URLs: regex + entity-derived, normalized and deduped
    regex_urls = extract_urls(text)
    all_urls = ordered_dedup([normalize_url(u) for u in [*regex_urls, *entity_urls]])

    for url in all_urls:
        if url not in links:
            links[url] = Link(id=url)

    link_refs = [links[url].id for url in all_urls] if all_urls else None

    return Post(
        id=message_uri(ch_id, int(msg_id)),
        content=text,
        created=str(created),
        has_container=channel_uri(ch_id),
        has_creator=creator_ref,
        links_to=link_refs,
        reply_to=message_uri(ch_id, reply_to_id) if reply_to_id is not None else None,
        forwards=int(forwards) if forwards is not None else None,
        pinned=bool(pinned) if pinned is not None else None,
        topics=topics if topics else None,
        mentions=mentions if mentions else None,
    )
