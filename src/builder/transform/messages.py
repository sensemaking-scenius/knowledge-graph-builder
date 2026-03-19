"""Raw Telegram message dicts → Post + related entities."""

from typing import Any

from builder.config import (
    attachment_uri,
    forum_uri,
    message_uri,
    poll_uri,
    thread_uri,
    user_uri,
)
from builder.models import (
    Attachment,
    Concept,
    LinkedDocument,
    Person,
    Poll,
    Post,
    Thread,
    User,
)
from builder.transform.entities import (
    extract_entity_urls,
    extract_hashtags,
    extract_urls,
    is_valid_url,
    make_linked_document,
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
    if isinstance(r, dict) and r.get("reply_to_msg_id") is not None:
        return int(r["reply_to_msg_id"])
    return None


def extract_thread_id(obj: dict) -> int | None:
    """Get the forum thread (topic) ID from reply_to, if any."""
    r = obj.get("reply_to")
    if not isinstance(r, dict):
        return None
    top_id = r.get("reply_to_top_id")
    if top_id is not None:
        return int(top_id)
    if r.get("forum_topic") and r.get("reply_to_msg_id") is not None:
        return int(r["reply_to_msg_id"])
    return None


def extract_topic_id_from_reply(obj: dict) -> int | None:
    """Get the topic/forum ID for container assignment.

    In a forum supergroup, reply_to_top_id is the topic root message ID
    which equals the forum topic ID. If forum_topic flag is set on reply_to,
    the reply_to_msg_id is the topic ID.
    """
    r = obj.get("reply_to")
    if not isinstance(r, dict):
        return None
    # forum_topic flag means this message is in a topic
    if r.get("forum_topic"):
        top_id = r.get("reply_to_top_id")
        if top_id is not None:
            return int(top_id)
        return int(r["reply_to_msg_id"])
    # reply_to_top_id without forum_topic is still a topic indicator
    top_id = r.get("reply_to_top_id")
    if top_id is not None:
        return int(top_id)
    return None


def classify_media_type(media: dict) -> str | None:
    """Classify media into a MediaType enum value."""
    type_name = media.get("_", "")
    if type_name == "MessageMediaPhoto":
        return "photo"
    if type_name == "MessageMediaDocument":
        return _classify_document_type(media)
    if type_name == "MessageMediaWebPage":
        return None  # WebPage is handled as LinkedDocument, not Attachment
    if "Photo" in type_name:
        return "photo"
    if "Video" in type_name:
        return "video"
    if type_name:
        return "other"
    return None


def _classify_document_type(media: dict) -> str:
    """Sub-classify document media."""
    doc = media.get("document")
    if not isinstance(doc, dict):
        return "document"
    mime = doc.get("mime_type", "")
    if isinstance(mime, str):
        if mime.startswith("video/"):
            return "video"
        if mime.startswith("audio/") and "ogg" in mime:
            return "voice"
        if mime.startswith("audio/"):
            return "audio"
        if "sticker" in mime or mime == "application/x-tgsticker":
            return "sticker"
        if mime == "video/mp4":
            # Check for animation
            attrs = doc.get("attributes") or []
            for attr in attrs:
                if isinstance(attr, dict) and "Animated" in attr.get("_", ""):
                    return "animation"
            return "video"
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


def extract_attachments(
    raw: dict, channel_id: int, msg_id: int,
) -> list[Attachment]:
    """Create Attachment entities from message media."""
    media = raw.get("media")
    if not isinstance(media, dict):
        return []

    mtype = classify_media_type(media)
    if mtype is None:
        return []

    # Extract document metadata
    doc = media.get("document") or media.get("photo") or {}
    if not isinstance(doc, dict):
        doc = {}

    mime = doc.get("mime_type")
    size = doc.get("size")
    duration = None

    # Get duration from attributes
    attrs = doc.get("attributes") or []
    for attr in attrs:
        if isinstance(attr, dict) and "duration" in attr:
            duration = attr["duration"]
            break

    return [Attachment(
        id=attachment_uri(channel_id, msg_id),
        format=mime,
        extent=int(size) if size is not None else None,
        media_type=mtype,
        duration=int(duration) if duration is not None else None,
    )]


def extract_webpage(raw: dict) -> dict | None:
    """Extract WebPage preview data from media."""
    media = raw.get("media")
    if not isinstance(media, dict):
        return None
    if media.get("_") != "MessageMediaWebPage":
        return None
    wp = media.get("webpage")
    if not isinstance(wp, dict):
        return None
    return wp


def extract_poll_entity(
    raw: dict, channel_id: int, msg_id: int,
) -> Poll | None:
    """Create a Poll entity from MessageMediaPoll."""
    media = raw.get("media")
    if not isinstance(media, dict) or media.get("_") != "MessageMediaPoll":
        return None

    poll_data = media.get("poll")
    results_data = media.get("results")
    if not isinstance(poll_data, dict):
        return None

    question_text = poll_data.get("question")
    if isinstance(question_text, dict):
        question_text = question_text.get("text", "")

    answers_raw = poll_data.get("answers") or []
    answer_results = (results_data or {}).get("results") or []

    answers: list[str] = []
    for i, ans in enumerate(answers_raw):
        if not isinstance(ans, dict):
            continue
        text = ans.get("text")
        if isinstance(text, dict):
            text = text.get("text", "")
        voters = 0
        if i < len(answer_results) and isinstance(answer_results[i], dict):
            voters = answer_results[i].get("voters", 0)
        answers.append(f"{text}:{voters}")

    total_voters = None
    if isinstance(results_data, dict):
        total_voters = results_data.get("total_voters")

    return Poll(
        id=poll_uri(channel_id, msg_id),
        question=str(question_text) if question_text else None,
        answers=answers if answers else None,
        total_voters=int(total_voters) if total_voters is not None else None,
        quiz=poll_data.get("quiz") or None,
        poll_closed=poll_data.get("closed") or None,
        public_voters=poll_data.get("public_voters") or None,
        multiple_choice=poll_data.get("multiple_choice") or None,
    )


def extract_sibling_uri(raw: dict) -> str | None:
    """Extract sibling (forward source) URI from fwd_from."""
    fwd = raw.get("fwd_from")
    if not isinstance(fwd, dict):
        return None
    from_id = fwd.get("from_id")
    channel_post = fwd.get("channel_post")
    if isinstance(from_id, dict) and "channel_id" in from_id and channel_post:
        return message_uri(int(from_id["channel_id"]), int(channel_post))
    return None


def transform_message(
    raw: dict,
    *,
    expected_channel_id: int,
    users: dict[int, User],
    persons: dict[int, Person],
    threads: dict[int, Thread],
    concepts: dict[str, Concept],
    linked_documents: dict[str, LinkedDocument],
    attachments: dict[str, Attachment],
    polls: dict[str, Poll],
    participant_names: dict[int, str] | None = None,
    participant_metadata: dict[int, dict] | None = None,
    forum_topic_ids: set[int] | None = None,
) -> Post | None:
    """Transform a single raw Telegram message dict into a Post.

    Populates registry dicts as side effects.
    Returns None if the message should be skipped (service messages, invalid).
    """
    # Skip service messages
    if raw.get("_") == "MessageService":
        return None

    ch_id = extract_channel_id(raw.get("peer_id"))
    if ch_id is None or ch_id != expected_channel_id:
        return None

    msg_id = raw.get("id")
    created = raw.get("date")
    if msg_id is None or created is None:
        return None

    text = raw.get("message") or ""
    from_user_id = extract_from_user_id(raw)
    reply_to_id = extract_reply_to_msg_id(raw)
    forwards = raw.get("forwards")
    pinned = raw.get("pinned")
    edit_date = raw.get("edit_date")
    grouped_id = raw.get("grouped_id")
    entities_raw = raw.get("entities") or []

    # Creator — register User + Person
    creator_ref: str | None = None
    if from_user_id is not None:
        _ensure_user(from_user_id, users, persons, participant_names, participant_metadata)
        creator_ref = users[from_user_id].id

    # Container — map to forum URI if topic is known
    topic_id = extract_topic_id_from_reply(raw)
    container_ref: str | None = None
    if topic_id is not None and forum_topic_ids and topic_id in forum_topic_ids:
        container_ref = forum_uri(ch_id, topic_id)
    else:
        container_ref = forum_uri(ch_id)

    # Reply
    reply_of_ref = message_uri(ch_id, reply_to_id) if reply_to_id is not None else None

    # Sibling (forward source)
    sibling_ref = extract_sibling_uri(raw)

    # Topics (hashtags → Concept)
    hashtag_concepts = extract_hashtags(text, entities_raw)
    topic_refs: list[str] | None = None
    if hashtag_concepts:
        for c in hashtag_concepts:
            if c.id not in concepts:
                concepts[c.id] = c
        topic_refs = [c.id for c in hashtag_concepts]

    # URLs → LinkedDocument
    regex_urls = extract_urls(text)
    entity_urls = extract_entity_urls(text, entities_raw)
    all_urls = ordered_dedup([
        u for u in (normalize_url(raw_u) for raw_u in [*regex_urls, *entity_urls])
        if u and is_valid_url(u)
    ])

    # WebPage preview metadata
    webpage = extract_webpage(raw)
    webpage_url = webpage.get("url") if webpage else None

    link_refs: list[str] | None = None
    if all_urls:
        for url in all_urls:
            if url not in linked_documents:
                wp = webpage if webpage and webpage_url == url else None
                linked_documents[url] = make_linked_document(url, wp)
        link_refs = [linked_documents[url].id for url in all_urls]

    # If there's a webpage URL not in the text URLs, add it too
    if webpage_url and webpage_url not in (all_urls or []):
        if webpage_url not in linked_documents:
            linked_documents[webpage_url] = make_linked_document(webpage_url, webpage)
        if link_refs is None:
            link_refs = []
        link_refs.append(linked_documents[webpage_url].id)

    # Attachments
    msg_attachments = extract_attachments(raw, ch_id, int(msg_id))
    attachment_refs: list[str] | None = None
    if msg_attachments:
        for att in msg_attachments:
            attachments[att.id] = att
        attachment_refs = [att.id for att in msg_attachments]

    # Poll
    poll_entity = extract_poll_entity(raw, ch_id, int(msg_id))
    poll_ref: str | None = None
    if poll_entity:
        polls[poll_entity.id] = poll_entity
        poll_ref = poll_entity.id

    # Thread detection
    thread_id = extract_thread_id(raw)
    if thread_id is not None and thread_id not in threads:
        thread_forum = forum_uri(ch_id, thread_id) if (forum_topic_ids and thread_id in (forum_topic_ids or set())) else forum_uri(ch_id)
        threads[thread_id] = Thread(
            id=thread_uri(ch_id, thread_id),
            has_parent_forum=thread_forum,
        )

    # Quote text
    quote_text = None
    reply_to_obj = raw.get("reply_to")
    if isinstance(reply_to_obj, dict):
        quote_text = reply_to_obj.get("quote_text")

    return Post(
        id=message_uri(ch_id, int(msg_id)),
        content=text,
        created=str(created),
        modified=str(edit_date) if edit_date else None,
        has_container=container_ref,
        has_creator=creator_ref,
        reply_of=reply_of_ref,
        sibling=sibling_ref,
        links_to=link_refs,
        attachment=attachment_refs,
        has_poll=poll_ref,
        topics=topic_refs,
        forwards=int(forwards) if forwards is not None else None,
        pinned=bool(pinned) if pinned else None,
        quote_text=str(quote_text) if quote_text else None,
        grouped_id=str(grouped_id) if grouped_id else None,
    )


def _ensure_user(
    uid: int,
    users: dict[int, User],
    persons: dict[int, Person],
    participant_names: dict[int, str] | None,
    participant_metadata: dict[int, dict] | None,
) -> None:
    """Register a User + Person in the registries if not already present."""
    if uid in users:
        return

    from builder.transform.users import make_person, make_user

    name = (participant_names or {}).get(uid)
    meta = (participant_metadata or {}).get(uid, {})

    users[uid] = make_user(
        uid,
        name=name,
        username=meta.get("username"),
        is_bot=meta.get("bot"),
    )
    persons[uid] = make_person(uid, name=name)
