"""Entity extraction: hashtags, mentions, URLs from raw Telegram messages."""

import re

from builder.config import topic_uri

URL_RE = re.compile(r"(https?://[^\s<>()\[\]{}\"']+)", re.IGNORECASE)


def extract_urls(text: str) -> list[str]:
    """Extract URLs from message text via regex."""
    if not text:
        return []
    return URL_RE.findall(text)


def normalize_url(url: str) -> str:
    """Ensure a URL has a protocol prefix.

    Telegram sometimes detects bare domain names (e.g. "Fly.io")
    as URLs. These need https:// to avoid RDF CURIE confusion.
    """
    url = url.strip()
    if not url:
        return url
    if "://" in url:
        return url
    return f"https://{url}"


def ordered_dedup(items: list[str]) -> list[str]:
    """Deduplicate a list while preserving order."""
    seen: set[str] = set()
    out: list[str] = []
    for x in items:
        if not x:
            continue
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def extract_entities(
    text: str, entities: list[dict],
) -> tuple[list[str], list[str], list[str]]:
    """Parse Telegram entity objects from a raw message.

    Returns (topic_iris, mention_iris, entity_urls).
    """
    topics: list[str] = []
    mentions: list[str] = []
    entity_urls: list[str] = []

    for ent in entities:
        if not isinstance(ent, dict):
            continue

        t = ent.get("_")  # Telegram entity type discriminator
        off = ent.get("offset")
        ln = ent.get("length")

        snippet: str | None = None
        if isinstance(off, int) and isinstance(ln, int) and ln > 0:
            # Note: Telegram entity offsets are UTF-16 code units.
            # This substring can be off for emojis; MVP accepts occasional mismatch.
            snippet = text[off : off + ln]

        if t == "MessageEntityHashtag" and snippet:
            tag = snippet.lstrip("#")
            if tag:
                topics.append(topic_uri(tag))

        if t == "MessageEntityMention" and snippet:
            handle = snippet.lstrip("@")
            if handle:
                mentions.append(f"tg:mention/{handle}")

        if t == "MessageEntityUrl" and snippet:
            entity_urls.append(snippet)

        if t == "MessageEntityTextUrl":
            url = ent.get("url")
            if isinstance(url, str) and url:
                entity_urls.append(url)

    return topics, mentions, entity_urls
