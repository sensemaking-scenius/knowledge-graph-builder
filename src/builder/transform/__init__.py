"""Transform stage: raw Telegram JSON → LinkML graph document."""

import json

from collections import OrderedDict

from linkml_runtime.dumpers import json_dumper

import yaml

from builder.config import (
    CHANNEL_FILE,
    FORUMS_FILE,
    GRAPH_FILE,
    MESSAGES_FILE,
    OVERRIDES_FILE,
    PARTICIPANTS_FILE,
    forum_uri,
    graph_uri,
)
from builder.models import (
    Attachment,
    Concept,
    Forum,
    GraphDocument,
    LinkedDocument,
    Person,
    Poll,
    Post,
    Site,
    Thread,
    User,
)
from builder.transform.channel import (
    make_community,
    make_site,
    make_supergroup_forum,
    make_topic_forum,
)
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


def load_forums(channel_id: int) -> tuple[list[Forum], set[int]]:
    """Load forum data from forums.json and build Forum entities.

    Returns:
        (forum_list, topic_ids set)
    """
    forums: list[Forum] = []
    topic_ids: set[int] = set()

    if not FORUMS_FILE.exists():
        return forums, topic_ids

    with open(FORUMS_FILE, "r", encoding="utf-8") as f:
        raw_forums = json.load(f)

    for entry in raw_forums:
        tid = entry.get("id")
        title = entry.get("title")
        closed = entry.get("closed", False)
        if tid is None:
            continue
        tid = int(tid)
        topic_ids.add(tid)
        forums.append(make_topic_forum(channel_id, tid, name=title, closed=closed))

    return forums, topic_ids


def load_user_overrides() -> tuple[dict[int, int], dict[int, dict]]:
    """Load merge and backfill rules from user_overrides.yaml."""
    merges: dict[int, int] = {}
    backfills: dict[int, dict] = {}
    if not OVERRIDES_FILE.exists():
        return merges, backfills
    with open(OVERRIDES_FILE, "r") as f:
        data = yaml.safe_load(f) or {}
    for old_id, new_id in (data.get("merge") or {}).items():
        merges[int(old_id)] = int(new_id)
    for uid, meta in (data.get("backfill") or {}).items():
        backfills[int(uid)] = meta
    return merges, backfills


def transform() -> GraphDocument:
    """Read raw messages and build a LinkML GraphDocument."""
    # Registries
    users: OrderedDict[int, User] = OrderedDict()
    persons: OrderedDict[int, Person] = OrderedDict()
    threads: OrderedDict[int, Thread] = OrderedDict()
    concepts: OrderedDict[str, Concept] = OrderedDict()
    linked_documents: OrderedDict[str, LinkedDocument] = OrderedDict()
    attachments: OrderedDict[str, Attachment] = OrderedDict()
    polls: OrderedDict[str, Poll] = OrderedDict()
    posts: list[Post] = []
    seen_msg_ids: set[int] = set()
    participant_names, participant_metadata = load_participants()
    merges, backfills = load_user_overrides()

    # Apply backfills to participant data
    for uid, meta in backfills.items():
        if "name" in meta and uid not in participant_names:
            participant_names[uid] = meta["name"]
        if "username" in meta:
            participant_metadata.setdefault(uid, {})["username"] = meta["username"]

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

            # Load forums once we know the channel
            if not hasattr(transform, "_forums_loaded"):
                pass  # handled below

    if first_channel_id is None:
        raise RuntimeError(f"No messages found in {MESSAGES_FILE}")

    # Load forums
    topic_forums, forum_topic_ids = load_forums(first_channel_id)

    # Second pass — now transform messages with full context
    seen_msg_ids.clear()

    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            raw = json.loads(line)

            # Apply user merges (rewrite sender to canonical ID)
            from_id = raw.get("from_id")
            if isinstance(from_id, dict) and "user_id" in from_id:
                old_uid = int(from_id["user_id"])
                if old_uid in merges:
                    from_id["user_id"] = merges[old_uid]

            msg_id = raw.get("id")
            if msg_id is not None:
                if msg_id in seen_msg_ids:
                    continue
                seen_msg_ids.add(msg_id)

            post = transform_message(
                raw,
                expected_channel_id=first_channel_id,
                users=users,
                persons=persons,
                threads=threads,
                concepts=concepts,
                linked_documents=linked_documents,
                attachments=attachments,
                polls=polls,
                participant_names=participant_names,
                participant_metadata=participant_metadata,
                forum_topic_ids=forum_topic_ids,
            )
            if post is not None:
                posts.append(post)

    # Build has_reply index (second pass over posts)
    reply_index: dict[str, list[str]] = {}
    for p in posts:
        if p.reply_of:
            reply_index.setdefault(p.reply_of, []).append(p.id)

    for p in posts:
        replies = reply_index.get(p.id)
        if replies:
            p.has_reply = replies

    # Build hierarchy
    community = make_community(first_channel_id)
    site = make_site()
    supergroup_forum = make_supergroup_forum(
        first_channel_id,
        name=community.name,
    )

    # Wire Site.host_of
    all_forums = [supergroup_forum] + topic_forums
    site.host_of = [f.id for f in all_forums]

    # Wire supergroup Forum.parent_of
    child_ids = [f.id for f in topic_forums]
    if child_ids:
        supergroup_forum.parent_of = child_ids

    # Build dicts for GraphDocument
    users_dict = {u.id: u for u in users.values()}
    persons_dict = {p.id: p for p in persons.values()}
    threads_dict = {t.id: t for t in threads.values()}
    forums_dict = {f.id: f for f in all_forums}

    doc = GraphDocument(
        id=graph_uri(first_channel_id),
        community=community,
        site=site,
        forums=forums_dict if forums_dict else None,
        users=users_dict if users_dict else None,
        persons=persons_dict if persons_dict else None,
        posts={p.id: p for p in posts} if posts else None,
        threads=threads_dict if threads_dict else None,
        concepts={c.id: c for c in concepts.values()} if concepts else None,
        attachments={a.id: a for a in attachments.values()} if attachments else None,
        linked_documents={d.id: d for d in linked_documents.values()} if linked_documents else None,
        polls={p.id: p for p in polls.values()} if polls else None,
    )

    return doc


def main() -> None:
    doc = transform()
    GRAPH_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        f.write(json_dumper.dumps(doc, inject_type=False))

    n_posts = len(doc.posts) if isinstance(doc.posts, dict) else 0
    n_users = len(doc.users) if isinstance(doc.users, dict) else 0
    n_forums = len(doc.forums) if isinstance(doc.forums, dict) else 0
    n_threads = len(doc.threads) if isinstance(doc.threads, dict) else 0
    n_concepts = len(doc.concepts) if isinstance(doc.concepts, dict) else 0
    n_attachments = len(doc.attachments) if isinstance(doc.attachments, dict) else 0
    n_linked_docs = len(doc.linked_documents) if isinstance(doc.linked_documents, dict) else 0
    n_persons = len(doc.persons) if isinstance(doc.persons, dict) else 0
    n_polls = len(doc.polls) if isinstance(doc.polls, dict) else 0
    print(
        f"Wrote {n_posts} posts, {n_users} users, {n_persons} persons, "
        f"{n_forums} forums, {n_threads} threads, {n_concepts} concepts, "
        f"{n_attachments} attachments, {n_linked_docs} linked docs, {n_polls} polls "
        f"to {GRAPH_FILE}"
    )
