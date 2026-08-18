"""Parse Harmonica synthesis results into entity annotations."""

import re
from typing import Any

from builder.config import CONFIDENCE_THRESHOLD

ENTITY_TYPE_ALIASES: dict[str, str] = {
    "person": "person",
    "people": "person",
    "human": "person",
    "org": "organization",
    "organization": "organization",
    "organisation": "organization",
    "company": "organization",
    "tool": "tool",
    "library": "tool",
    "framework": "tool",
    "platform": "tool",
    "service": "tool",
    "software": "tool",
    "technology": "tool",
    "project": "project",
    "initiative": "project",
    "product": "project",
    "concept": "concept",
    "idea": "concept",
    "methodology": "concept",
    "theory": "concept",
    "pattern": "concept",
    "method": "concept",
}


def _normalize_entity_type(raw: str) -> str:
    key = raw.strip().lower()
    return ENTITY_TYPE_ALIASES.get(key, "concept")


def _extract_confidence(text: str, participant_count: int) -> float:
    """Extract confidence from patterns like '4/5 participants' or '80%'."""
    ratio_match = re.search(r"(\d+)\s*/\s*(\d+)", text)
    if ratio_match:
        n = int(ratio_match.group(1))
        m = int(ratio_match.group(2))
        if m > 0:
            return n / m

    pct_match = re.search(r"(\d+)%", text)
    if pct_match:
        return int(pct_match.group(1)) / 100.0

    if participant_count > 0:
        return 1.0 / participant_count

    return 0.5


def parse_summary_entities(
    summary: dict[str, Any] | str,
    responses: dict[str, Any] | list[Any],
    participant_count: int,
) -> list[dict[str, Any]]:
    """Parse entities from a Harmonica summary.

    Returns a list of entity dicts with: name, type, description, confidence.
    """
    summary_text = ""
    if isinstance(summary, dict):
        summary_text = summary.get("summary", summary.get("text", ""))
    elif isinstance(summary, str):
        summary_text = summary

    if not summary_text:
        return []

    entities: list[dict[str, Any]] = []
    seen_names: set[str] = set()

    for line in summary_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        bullet_match = re.match(
            r"^[-*•]\s+\*?\*?(.+?)\*?\*?"
            r"\s*(?:\(([^)]+)\))?"
            r"\s*(?:[-—–:](.*))?$",
            line,
        )
        if not bullet_match:
            continue

        name = bullet_match.group(1).strip().strip("*").strip()
        type_hint = bullet_match.group(2) or ""
        description = bullet_match.group(3) or ""

        if not name or len(name) > 100:
            continue

        name_key = name.lower()
        if name_key in seen_names:
            continue
        seen_names.add(name_key)

        confidence = _extract_confidence(
            line, participant_count
        )

        entity_type = _normalize_entity_type(type_hint) if type_hint else "concept"

        entities.append({
            "name": name,
            "type": entity_type,
            "description": description.strip().strip("-").strip(),
            "confidence": round(confidence, 2),
        })

    return entities


def filter_by_confidence(
    entities: list[dict[str, Any]],
    threshold: float = CONFIDENCE_THRESHOLD,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split entities into above/below confidence threshold."""
    above = [e for e in entities if e["confidence"] >= threshold]
    below = [e for e in entities if e["confidence"] < threshold]
    return above, below
