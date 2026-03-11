"""Transform stage: raw Telegram JSON → LinkML graph document."""

import json

from collections import OrderedDict

from linkml_runtime.dumpers import json_dumper

from builder.config import MESSAGES_FILE, GRAPH_FILE, graph_uri
from builder.models import GraphDocument, Link, UserAccount
from builder.transform.channel import make_community
from builder.transform.messages import extract_channel_id, transform_message


def transform() -> GraphDocument:
    """Read raw messages and build a LinkML GraphDocument."""
    users: OrderedDict[int, UserAccount] = OrderedDict()
    links: OrderedDict[str, Link] = OrderedDict()
    posts = []

    first_channel_id: int | None = None

    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            raw = json.loads(line)

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
            )
            if post is not None:
                posts.append(post)

    if first_channel_id is None:
        raise RuntimeError(f"No messages found in {MESSAGES_FILE}")

    community = make_community(first_channel_id)

    doc = GraphDocument(
        id=graph_uri(first_channel_id),
        community=community.id,
        users={u.id: {"id": u.id} for u in users.values()},
        links={link.id: {"id": link.id} for link in links.values()},
        posts={p.id: p for p in posts},
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
    print(f"Wrote {n_posts} posts, {n_users} users, {n_links} links to {GRAPH_FILE}")
