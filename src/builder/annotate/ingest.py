"""Import parsed annotation entities into the LinkML graph."""

import json
from typing import Any

from builder.config import (
    GRAPH_FILE,
    SESSIONS_FILE,
    annotation_session_uri,
    annotation_uri,
    concept_uri,
)


def _load_graph() -> dict[str, Any]:
    with open(GRAPH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_graph(graph: dict[str, Any]) -> None:
    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)


def _update_session_status(harmonica_session_id: str, status: str) -> None:
    if not SESSIONS_FILE.exists():
        return
    with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
        sessions = json.load(f)
    for s in sessions:
        if s["harmonica_session_id"] == harmonica_session_id:
            s["status"] = status
            break
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2)


def ingest_entities(
    harmonica_session_id: str,
    entities: list[dict[str, Any]],
    post_ids: list[str],
    participant_count: int,
    theme: str,
    created: str,
) -> dict[str, int]:
    """Import annotation entities into the graph.

    Creates Concept entries for discovered entities,
    Annotation records linking them to source posts,
    and an AnnotationSession record.

    Returns counts of created entities.
    """
    graph = _load_graph()

    concepts = graph.setdefault("concepts", {})
    annotations = graph.setdefault("annotations", {})
    sessions = graph.setdefault("annotation_sessions", {})

    session_uri = annotation_session_uri(harmonica_session_id)
    sessions[session_uri] = {
        "id": session_uri,
        "harmonica_session_id": harmonica_session_id,
        "theme": theme,
        "messages_annotated": post_ids,
        "participant_count": participant_count,
        "created": created,
        "session_status": "imported",
    }

    new_concepts = 0
    new_annotations = 0

    for i, entity in enumerate(entities):
        name = entity["name"]
        entity_type = entity["type"]
        description = entity.get("description", "")
        confidence = entity["confidence"]

        tag = name.lower().replace(" ", "-")
        c_uri = concept_uri(tag)

        if c_uri not in concepts:
            concepts[c_uri] = {
                "id": c_uri,
                "pref_label": name,
                "concept_type": entity_type,
                "concept_description": description or None,
                "confidence": confidence,
            }
            new_concepts += 1
        else:
            existing = concepts[c_uri]
            if confidence > (existing.get("confidence") or 0):
                existing["confidence"] = confidence
            if description and not existing.get("concept_description"):
                existing["concept_description"] = description

        ann_uri = annotation_uri(harmonica_session_id, i)
        annotations[ann_uri] = {
            "id": ann_uri,
            "annotation_body": name,
            "entity_type": entity_type,
            "confidence": confidence,
            "session_ref": session_uri,
            "created": created,
        }
        new_annotations += 1

    posts = graph.get("posts", {})
    entity_concept_ids = []
    for entity in entities:
        tag = entity["name"].lower().replace(" ", "-")
        entity_concept_ids.append(concept_uri(tag))

    for pid in post_ids:
        if pid in posts:
            existing_topics = posts[pid].get("topics") or []
            merged = list(dict.fromkeys(existing_topics + entity_concept_ids))
            posts[pid]["topics"] = merged

    _save_graph(graph)
    _update_session_status(harmonica_session_id, "imported")

    return {
        "new_concepts": new_concepts,
        "new_annotations": new_annotations,
        "posts_linked": len(post_ids),
    }
