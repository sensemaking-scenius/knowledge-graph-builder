"""Raw Telegram message dicts → Post objects."""

from typing import Any

from builder.config import channel_uri, message_uri, thread_uri, user_uri
from builder.models import Link, Post, Thread, UserAccount
from builder.transform.entities import (
    extract_entities,
    extract_urls,
    is_valid_url,
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


def extract_thread_id(obj: dict) -> int | None:
    """Get the forum thread (topic) ID from reply_to, if any."""
    r = obj.get("reply_to")
    if not isinstance(r, dict):
        return None
    # reply_to_top_id is the thread root in forum supergroups
    top_id = r.get("reply_to_top_id")
    if top_id is not None:
        return int(top_id)
    # If forum_topic is set and reply_to_msg_id exists, that's the thread root
    if r.get("forum_topic") and "reply_to_msg_id" in r:
        return int(r["reply_to_msg_id"])
    return None


def classify_media(raw: dict) -> str | None:
    """Classify media type from the raw message's media field."""
    media = raw.get("media")
    if not isinstance(media, dict):
        return None
    type_name = media.get("_", "")
    mapping = {
        "MessageMediaPhoto": "photo",
        "MessageMediaDocument": _classify_document(media),
        "MessageMediaWebPage": "webpage",
    }
    if type_name in mapping:
        result = mapping[type_name]
        return result if isinstance(result, str) else result
    if "Photo" in type_name:
        return "photo"
    if "Video" in type_name:
        return "video"
    if "Document" in type_name:
        return "document"
    if "WebPage" in type_name:
        return "webpage"
    if type_name:
        return "other"
    return None


def _classify_document(media: dict) -> str:
    """Sub-classify document media into video/audio/sticker/document."""
    doc = media.get("document")
    if not isinstance(doc, dict):
        return "document"
    mime = doc.get("mime_type", "")
    if isinstance(mime, str):
        if mime.startswith("video/"):
            return "video"
        if mime.startswith("audio/"):
            return "audio"
        if "sticker" in mime or mime == "application/x-tgsticker":
            return "sticker"
    # Check attributes for video/audio/sticker markers
    attrs = doc.get("attributes") or []
    for attr in attrs:
        if isinstance(attr, dict):
            t = attr.get("_", "")
            if "Video" in t:
                return "video"
            if "Audio" in t:
                return "audio"
            if "Sticker" in t:
                return "sticker"
    return "document"


def extract_reactions(raw: dict) -> tuple[int, list[str]]:
    """Extract reaction_count and reactions list from raw message.

    Returns (total_count, ["emoji:count", ...]).
    """
    reactions_obj = raw.get("reactions")
    if not isinstance(reactions_obj, dict):
        return 0, []
    results = reactions_obj.get("results")
    if not isinstance(results, list):
        return 0, []

    total = 0
    items: list[str] = []
    for r in results:
        if not isinstance(r, dict):
            continue
        count = r.get("count", 0)
        if not isinstance(count, int):
            continue
        total += count
        reaction = r.get("reaction", {})
        if isinstance(reaction, dict):
            emoticon = reaction.get("emoticon", "")
        else:
            emoticon = str(reaction) if reaction else ""
        if emoticon and count:
            items.append(f"{emoticon}:{count}")

    return total, items


def extract_forwarded_from(raw: dict) -> str | None:
    """Extract forward origin description from fwd_from."""
    fwd = raw.get("fwd_from")
    if not isinstance(fwd, dict):
        return None
    # Try channel/chat name first
    from_id = fwd.get("from_id")
    if isinstance(from_id, dict):
        if "channel_id" in from_id:
            return f"channel/{from_id['channel_id']}"
        if "user_id" in from_id:
            return f"user/{from_id['user_id']}"
    from_name = fwd.get("from_name")
    if from_name:
        return str(from_name)
    return "unknown"


def classify_service_action(raw: dict) -> str | None:
    """Classify service message action type."""
    action = raw.get("action")
    if not isinstance(action, dict):
        return None
    type_name = action.get("_", "")
    if "Join" in type_name or "AddUser" in type_name:
        return "join"
    if "Left" in type_name or "DeleteUser" in type_name or "Kick" in type_name:
        return "leave"
    if "Pin" in type_name:
        return "pin"
    if "Title" in type_name or "ChatEditTitle" in type_name:
        return "title_change"
    if "Photo" in type_name and "Chat" in type_name:
        return "photo_change"
    if type_name:
        return "other"
    return None


def transform_message(
    raw: dict,
    *,
    expected_channel_id: int,
    users: dict[int, UserAccount],
    links: dict[str, Link],
    threads: dict[int, Thread],
    participant_names: dict[int, str] | None = None,
    participant_metadata: dict[int, dict] | None = None,
    topic_names: dict[int, str] | None = None,
) -> Post | None:
    """Transform a single raw Telegram message dict into a Post.

    Populates `users`, `links`, and `threads` dicts as side effects (dedup registries).
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

    is_service_msg = raw.get("_") == "MessageService"
    text = raw.get("message") or ""
    from_user_id = extract_from_user_id(raw)
    reply_to_id = extract_reply_to_msg_id(raw)
    forwards = raw.get("forwards")
    pinned = raw.get("pinned")
    entities_raw = raw.get("entities") or []

    # New fields
    edit_date = raw.get("edit_date")
    views = raw.get("views")
    replies_obj = raw.get("replies")
    num_replies_val = None
    if isinstance(replies_obj, dict):
        num_replies_val = replies_obj.get("replies")

    # Creator
    creator_ref: str | None = None
    if from_user_id is not None:
        if from_user_id not in users:
            name = (participant_names or {}).get(from_user_id)
            meta = (participant_metadata or {}).get(from_user_id, {})
            users[from_user_id] = UserAccount(
                id=user_uri(from_user_id),
                name=name,
                username=meta.get("username"),
                is_bot=meta.get("bot") if meta.get("bot") else None,
                is_verified=meta.get("verified") if meta.get("verified") else None,
                is_premium=meta.get("premium") if meta.get("premium") else None,
            )
        creator_ref = users[from_user_id].id

    # Entity extraction
    topics, mentions, entity_urls = extract_entities(text, entities_raw)
    topics = ordered_dedup(topics)
    mentions = ordered_dedup(mentions)

    # URLs: regex + entity-derived, normalized, validated, and deduped
    regex_urls = extract_urls(text)
    all_urls = ordered_dedup([
        u for u in (normalize_url(raw_u) for raw_u in [*regex_urls, *entity_urls])
        if u and is_valid_url(u)
    ])

    for url in all_urls:
        if url not in links:
            links[url] = Link(id=url)

    link_refs = [links[url].id for url in all_urls] if all_urls else None

    # Thread detection
    thread_id = extract_thread_id(raw)
    thread_ref: str | None = None
    if thread_id is not None:
        if thread_id not in threads:
            thread_name = (topic_names or {}).get(thread_id)
            threads[thread_id] = Thread(
                id=thread_uri(ch_id, thread_id),
                name=thread_name,
                has_parent=channel_uri(ch_id),
            )
        thread_ref = threads[thread_id].id

    # Reactions
    reaction_count, reactions_list = extract_reactions(raw)

    # Media
    media_type_val = classify_media(raw)

    # Forwarded from
    forwarded_from_val = extract_forwarded_from(raw)

    # Service action
    service_action_val = classify_service_action(raw) if is_service_msg else None

    return Post(
        id=message_uri(ch_id, int(msg_id)),
        content=text,
        created=str(created),
        modified=str(edit_date) if edit_date else None,
        has_container=channel_uri(ch_id),
        has_creator=creator_ref,
        has_thread=thread_ref,
        links_to=link_refs,
        reply_to=message_uri(ch_id, reply_to_id) if reply_to_id is not None else None,
        forwards=int(forwards) if forwards is not None else None,
        pinned=bool(pinned) if pinned is not None else None,
        topics=topics if topics else None,
        mentions=mentions if mentions else None,
        num_views=int(views) if views is not None else None,
        num_replies=int(num_replies_val) if num_replies_val is not None else None,
        reaction_count=reaction_count if reaction_count > 0 else None,
        reactions=reactions_list if reactions_list else None,
        media_type=media_type_val,
        forwarded_from=forwarded_from_val,
        is_service=True if is_service_msg else None,
        service_action=service_action_val,
    )
