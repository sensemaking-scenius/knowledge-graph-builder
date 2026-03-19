"""Transform stage: raw Telegram JSON → LinkML graph document."""

import json

from collections import OrderedDict

from linkml_runtime.dumpers import json_dumper

from builder.config import MESSAGES_FILE, PARTICIPANTS_FILE, TOPICS_FILE, GRAPH_FILE, graph_uri
from builder.models import GraphDocument, Link, Thread, UserAccount
from builder.transform.channel import make_community
from builder.transform.messages import extract_channel_id, transform_message


def load_participants() -> tuple[dict[int, str], dict[int, dict]]:
    """Load participant metadata.

    Returns:
        (names: user_id → display name, metadata: user_id → full metadata dict)
    """
    names: dict[int, str] = {}
    metadata: dict[int, dict] = {}
    if not PARTICIPANTS_FILE.exists():
        return names, metadata

    with open(PARTICIPANTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            uid = p.get("id")
            if uid is None:
                continue
            uid = int(uid)
            username = p.get("username")
            first_name = p.get("first_name")
            if username:
                names[uid] = f"@{username}"
            elif first_name:
                names[uid] = first_name
            metadata[uid] = {
                "username": username,
                "bot": p.get("bot"),
                "verified": p.get("verified"),
                "premium": p.get("premium"),
            }
    return names, metadata


def load_topic_names() -> dict[int, str]:
    """Load forum topic names from topics.json.

    Returns topic_id → title mapping.
    """
    if not TOPICS_FILE.exists():
        return {}
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # JSON keys are strings, convert to int
    return {int(k): v for k, v in raw.items()}


def transform() -> GraphDocument:
    """Read raw messages and build a LinkML GraphDocument."""
    users: OrderedDict[int, UserAccount] = OrderedDict()
    links: OrderedDict[str, Link] = OrderedDict()
    threads: OrderedDict[int, Thread] = OrderedDict()
    posts = []
    seen_msg_ids: set[int] = set()
    participant_names, participant_metadata = load_participants()
    topic_names = load_topic_names()

    first_channel_id: int | None = None

    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            raw = json.loads(line)

            # Deduplication by message ID
            msg_id = raw.get("id")
            if msg_id is not None:
                if msg_id in seen_msg_ids:
                    continue
                seen_msg_ids.add(msg_id)

            # Determine channel ID from first message
            if first_channel_id is None:
                first_channel_id = extract_channel_id(raw.get("peer_id"))
                if first_channel_id is None:
                    continue

            post = transform_message(
                raw,
                expected_channel_id=first_channel_id,
                users=users,
                links=links,
                threads=threads,
                participant_names=participant_names,
                participant_metadata=participant_metadata,
                topic_names=topic_names,
            )
            if post is not None:
                posts.append(post)

    if first_channel_id is None:
        raise RuntimeError(f"No messages found in {MESSAGES_FILE}")

    community = make_community(first_channel_id)

    # Build user dicts with all available fields
    users_dict = {}
    for u in users.values():
        entry: dict = {"id": u.id}
        if u.name:
            entry["name"] = u.name
        if u.username:
            entry["username"] = u.username
        if u.is_bot:
            entry["is_bot"] = True
        if u.is_verified:
            entry["is_verified"] = True
        if u.is_premium:
            entry["is_premium"] = True
        users_dict[u.id] = entry

    # Build thread dicts
    threads_dict = {}
    for t in threads.values():
        entry = {"id": t.id}
        if t.name:
            entry["name"] = t.name
        if t.has_parent:
            entry["has_parent"] = t.has_parent
        threads_dict[t.id] = entry

    doc = GraphDocument(
        id=graph_uri(first_channel_id),
        community=community,
        users=users_dict,
        links={link.id: {"id": link.id} for link in links.values()},
        posts={p.id: p for p in posts},
        threads=threads_dict if threads_dict else None,
    )

    return doc


def main() -> None:
    doc = transform()
    GRAPH_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        f.write(json_dumper.dumps(doc, inject_type=False))

    n_posts = len(doc.posts) if isinstance(doc.posts, dict) else 0
    n_users = len(doc.users) if isinstance(doc.users, dict) else 0
    n_links = len(doc.links) if isinstance(doc.links, dict) else 0
    n_threads = len(doc.threads) if isinstance(doc.threads, dict) else 0
    print(f"Wrote {n_posts} posts, {n_users} users, {n_links} links, {n_threads} threads to {GRAPH_FILE}")
