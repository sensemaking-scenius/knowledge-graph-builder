"""Entity extraction: hashtags, URLs from raw Telegram messages."""

import re

from builder.config import concept_uri, document_uri
from builder.models import Concept, LinkedDocument

URL_RE = re.compile(r"(https?://[^\s<>()\[\]{}\"']+)", re.IGNORECASE)


def extract_urls(text: str) -> list[str]:
    """Extract URLs from message text via regex."""
    if not text:
        return []
    return URL_RE.findall(text)


def normalize_url(url: str) -> str:
    """Normalize a URL: strip whitespace/newlines, ensure protocol prefix."""
    url = url.split()[0] if url.strip() else ""
    if not url:
        return url
    if "://" in url:
        return url
    return f"https://{url}"


_URI_OK = re.compile(r"^[A-Za-z][A-Za-z0-9+\-.]*://[^\s<>\"{}|\\^`]+$")


def is_valid_url(url: str) -> bool:
    """Return True if *url* looks like a usable absolute URI."""
    return bool(_URI_OK.match(url))


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


def extract_hashtags(text: str, entities: list[dict]) -> list[Concept]:
    """Extract hashtag entities and return Concept objects."""
    concepts: list[Concept] = []
    seen: set[str] = set()

    for ent in entities:
        if not isinstance(ent, dict):
            continue
        if ent.get("_") != "MessageEntityHashtag":
            continue
        off = ent.get("offset")
        ln = ent.get("length")
        if not isinstance(off, int) or not isinstance(ln, int) or ln <= 0:
            continue
        snippet = text[off : off + ln]
        tag = snippet.lstrip("#").strip()
        if not tag:
            continue
        uri = concept_uri(tag)
        if uri in seen:
            continue
        seen.add(uri)
        concepts.append(Concept(id=uri, pref_label=tag))

    return concepts


def extract_entity_urls(text: str, entities: list[dict]) -> list[str]:
    """Extract URLs from Telegram entity objects."""
    urls: list[str] = []
    for ent in entities:
        if not isinstance(ent, dict):
            continue
        t = ent.get("_")
        off = ent.get("offset")
        ln = ent.get("length")

        if t == "MessageEntityUrl" and isinstance(off, int) and isinstance(ln, int) and ln > 0:
            snippet = text[off : off + ln]
            if snippet:
                urls.append(snippet)

        if t == "MessageEntityTextUrl":
            url = ent.get("url")
            if isinstance(url, str) and url:
                urls.append(url)

    return urls


def make_linked_document(url: str, webpage: dict | None = None) -> LinkedDocument:
    """Create a LinkedDocument from a URL and optional Telegram WebPage preview."""
    title = None
    description = None
    creator = None
    site_name_val = None

    if webpage:
        title = webpage.get("title")
        description = webpage.get("description")
        creator = webpage.get("author")
        site_name_val = webpage.get("site_name")

    return LinkedDocument(
        id=document_uri(url),
        title=title,
        doc_description=description,
        doc_creator=creator,
        site_name=site_name_val,
    )
