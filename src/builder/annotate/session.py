"""Create and manage Harmonica annotation sessions."""

import json
from datetime import datetime, timezone
from typing import Any

from builder.annotate.harmonica import create_session, get_responses, get_summary
from builder.annotate.select import format_messages_for_session, select_batch
from builder.config import SESSIONS_FILE

THEME_PROMPTS: dict[str, dict[str, str]] = {
    "free_hunt": {
        "label": "Free Hunt",
        "goal": (
            "Help build our community's knowledge graph by identifying any "
            "notable entities — people, tools, projects, concepts, or "
            "organizations — mentioned in these messages."
        ),
        "focus": "anything notable",
    },
    "whos_who": {
        "label": "Who's Who",
        "goal": (
            "Identify the people and organizations mentioned or discussed "
            "in these messages. Who are the key figures?"
        ),
        "focus": "people and organizations",
    },
    "tool_chest": {
        "label": "Tool Chest",
        "goal": (
            "Find all tools, libraries, frameworks, platforms, and services "
            "mentioned in these messages."
        ),
        "focus": "tools and technologies",
    },
    "project_radar": {
        "label": "Project Radar",
        "goal": (
            "Spot projects, initiatives, products, and collaborative efforts "
            "mentioned in these messages."
        ),
        "focus": "projects and initiatives",
    },
    "idea_map": {
        "label": "Idea Map",
        "goal": (
            "Map the abstract concepts, methodologies, theories, and ideas "
            "discussed in these messages."
        ),
        "focus": "concepts and ideas",
    },
    "link_dive": {
        "label": "Link Dive",
        "goal": (
            "Evaluate the shared URLs and linked resources in these messages. "
            "What are they about and why are they relevant?"
        ),
        "focus": "linked resources",
    },
}

FACILITATOR_QUESTIONS = [
    "Read through these messages carefully. What {focus} do you notice?",
    "For each entity you found, what type is it? (person / tool / project / concept / organization)",
    "How would you describe each one in a single sentence?",
    "Do any of these entities seem related to each other? How?",
    "Anything surprising or non-obvious you noticed?",
]


def _load_sessions() -> list[dict[str, Any]]:
    if not SESSIONS_FILE.exists():
        return []
    with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_sessions(sessions: list[dict[str, Any]]) -> None:
    SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2)


def create_annotation_session(
    theme: str = "free_hunt",
    batch_size: int | None = None,
    forum_id: str | None = None,
) -> dict[str, Any]:
    """Create a Harmonica session for entity annotation.

    Returns the session record (local tracking + Harmonica metadata).
    """
    from builder.config import BATCH_SIZE

    bs = batch_size or BATCH_SIZE
    theme_config = THEME_PROMPTS.get(theme, THEME_PROMPTS["free_hunt"])

    posts = select_batch(batch_size=bs, forum_id=forum_id)
    if not posts:
        raise RuntimeError("No unannotated messages available for a session.")

    context = format_messages_for_session(posts)
    topic = f"Entity Discovery: {theme_config['label']}"
    goal = theme_config["goal"]
    questions = [
        q.format(focus=theme_config["focus"]) for q in FACILITATOR_QUESTIONS
    ]

    result = create_session(
        topic=topic,
        goal=goal,
        context=context,
        questions=questions,
    )

    post_ids = [p["id"] for p in posts]
    session_record = {
        "harmonica_session_id": result.get("id", result.get("session_id", "")),
        "theme": theme,
        "messages_annotated": post_ids,
        "participant_count": 0,
        "created": datetime.now(timezone.utc).isoformat(),
        "status": "active",
        "join_url": result.get("join_url", result.get("url", "")),
        "harmonica_response": result,
    }

    sessions = _load_sessions()
    sessions.append(session_record)
    _save_sessions(sessions)

    return session_record


def check_session(harmonica_session_id: str) -> dict[str, Any]:
    """Check a session's status and fetch responses + summary if ready."""
    responses = get_responses(harmonica_session_id)
    summary = get_summary(harmonica_session_id)

    sessions = _load_sessions()
    for s in sessions:
        if s["harmonica_session_id"] == harmonica_session_id:
            resp_list = (
                responses if isinstance(responses, list)
                else responses.get("responses", [])
            )
            s["participant_count"] = len(resp_list)
            if summary:
                s["status"] = "synthesized"
            break
    _save_sessions(sessions)

    return {
        "responses": responses,
        "summary": summary,
    }
