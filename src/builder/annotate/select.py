"""Select batches of unannotated messages for Harmonica sessions."""

import json
from typing import Any

from builder.config import BATCH_SIZE, GRAPH_FILE, SESSIONS_FILE


def _load_graph() -> dict[str, Any]:
    with open(GRAPH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _already_annotated_post_ids() -> set[str]:
    """Collect Post IDs that have already been included in annotation sessions."""
    if not SESSIONS_FILE.exists():
        return set()
    with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
        sessions = json.load(f)
    annotated: set[str] = set()
    for s in sessions:
        annotated.update(s.get("messages_annotated", []))
    return annotated


def select_batch(
    batch_size: int = BATCH_SIZE,
    forum_id: str | None = None,
) -> list[dict[str, Any]]:
    """Pick a batch of unannotated posts, prioritizing those with replies.

    Returns list of post dicts with id, content, has_creator, created.
    """
    graph = _load_graph()
    posts_data = graph.get("posts", {})
    if not posts_data:
        return []

    annotated = _already_annotated_post_ids()

    candidates: list[dict[str, Any]] = []
    for post_id, post in posts_data.items():
        if post_id in annotated:
            continue
        if not post.get("content"):
            continue
        if forum_id and post.get("has_container") != forum_id:
            continue
        candidates.append(post)

    candidates.sort(
        key=lambda p: (
            len(p.get("has_reply", []) or []),
            p.get("created", ""),
        ),
        reverse=True,
    )

    return candidates[:batch_size]


def format_messages_for_session(posts: list[dict[str, Any]]) -> str:
    """Format a batch of posts as readable context for a Harmonica session."""
    lines: list[str] = []
    for i, post in enumerate(posts, 1):
        creator = post.get("has_creator", "unknown")
        created = post.get("created", "")
        content = post.get("content", "")
        date_str = created[:10] if created else "?"
        lines.append(f"[Message {i}] {creator} ({date_str}):")
        lines.append(content)
        lines.append("")
    return "\n".join(lines)
