import json
import os
from collections import OrderedDict

from linkml_runtime.dumpers import json_dumper

from builder.sioc_model import Community, GraphDocument, Link, Post, UserAccount

INP = "data/raw/canonical_last_7_days.jsonl"
OUT = "data/raw/linkml_graph.json"


def community_id(chat_id: str) -> str:
    return f"tg:community/{chat_id}"


def user_id(user_id: int) -> str:
    return f"tg:user/{user_id}"


def post_id(chat_id: str, message_id: int) -> str:
    return f"tg:post/{chat_id}/{message_id}"


def hashtag_topic_iri(tag: str) -> str:
    # Keep it simple + deterministic; you can URL-encode later if you want.
    return f"tg:tag/hashtag/{tag}"


def mention_iri(handle: str) -> str:
    return f"tg:mention/{handle}"


def normalize_url(url: str) -> str:
    """
    Normalize a URL-like string to a proper URL.

    Telegram sometimes detects bare domain names like "Fly.io" or "Gitcoin.co"
    as URLs. These need to be normalized to proper URLs with a protocol
    to avoid issues with RDF serialization (where they'd be mistaken for CURIEs).
    """
    url = url.strip()
    if not url:
        return url

    # If it already has a protocol, return as-is
    if "://" in url:
        return url

    # Otherwise, add https:// prefix
    return f"https://{url}"


def ordered_dedup(items: list[str]) -> list[str]:
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

def graph_id(chat_id: str) -> str:
    return f"tg:graph/{chat_id}/last7d"


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    # Keep these for dedup and stable output ordering
    users: "OrderedDict[int, UserAccount]" = OrderedDict()
    links: "OrderedDict[str, Link]" = OrderedDict()
    posts: list[Post] = []

    first_chat_id: str | None = None

    with open(INP, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)

            chat_id = obj["chat_id"]
            if first_chat_id is None:
                first_chat_id = chat_id
            elif chat_id != first_chat_id:
                # MVP: single community in one run
                continue

            message_id = int(obj["message_id"])
            created_at = obj["created_at"]
            text = obj.get("text") or ""
            from_user_id = obj.get("from_user_id")
            reply_to_message_id = obj.get("reply_to_message_id")

            # From Slice 3
            urls = obj.get("urls") or []
            forwards = obj.get("forwards")
            pinned = obj.get("pinned")

            # From Slice 4 (entities)
            entities = obj.get("entities") or []

            # Create community object (kept in the document),
            # but posts will reference it by id string to satisfy LinkML typing.
            community_obj = Community(id=community_id(chat_id))
            community_ref = community_obj.id

            creator_ref: str | None = None
            if from_user_id is not None:
                uid = int(from_user_id)
                if uid not in users:
                    users[uid] = UserAccount(id=user_id(uid))
                creator_ref = users[uid].id

            # --- Slice 4 parsing: topics, mentions, entity URLs ---
            topics: list[str] = []
            mentions: list[str] = []
            entity_urls: list[str] = []

            for ent in entities:
                if not isinstance(ent, dict):
                    continue

                t = ent.get("type")
                off = ent.get("offset")
                ln = ent.get("length")

                snippet: str | None = None
                if isinstance(off, int) and isinstance(ln, int) and ln > 0:
                    # Note: Telegram entity offsets are in UTF-16 code units.
                    # This substring can be off for emojis; MVP accepts occasional mismatch.
                    snippet = text[off : off + ln]

                if t == "MessageEntityHashtag" and snippet:
                    tag = snippet.lstrip("#")
                    if tag:
                        topics.append(hashtag_topic_iri(tag))

                if t == "MessageEntityMention" and snippet:
                    handle = snippet.lstrip("@")
                    if handle:
                        mentions.append(mention_iri(handle))

                if t == "MessageEntityUrl" and snippet:
                    entity_urls.append(snippet)

                if t == "MessageEntityTextUrl":
                    url = ent.get("url")
                    if isinstance(url, str) and url:
                        entity_urls.append(url)

            topics = ordered_dedup(topics)
            mentions = ordered_dedup(mentions)

            # Merge regex URLs + entity-derived URLs, normalizing them
            all_urls = ordered_dedup([normalize_url(u) for u in [*urls, *entity_urls]])

            link_objs: list[Link] = []
            for url in all_urls:
                if url not in links:
                    links[url] = Link(id=url)  # URL string as identifier
                link_objs.append(links[url])

            link_refs = [lo.id for lo in link_objs] if link_objs else None

            # NOTE: This assumes you've added `topics` and `mentions` slots to Post in your schema.
            p = Post(
                id=post_id(chat_id, message_id),
                content=text,
                created=created_at,
                has_container=community_ref,  # reference by id
                has_creator=creator_ref,      # reference by id
                links_to=link_refs,           # list of ids
                reply_to=post_id(chat_id, int(reply_to_message_id)) if reply_to_message_id is not None else None,
                forwards=int(forwards) if forwards is not None else None,
                pinned=bool(pinned) if pinned is not None else None,
                topics=topics if topics else None,
                mentions=mentions if mentions else None,
            )
            posts.append(p)

    if first_chat_id is None:
        raise RuntimeError("No messages found in canonical input file.")

    # Build a single root document.
    # Use dict forms for inlined multivalued slots to satisfy generated LinkML typing.
    doc = GraphDocument(
        id=graph_id(first_chat_id),
        community=community_id(first_chat_id),
        users={u.id: {"id": u.id} for u in users.values()},
        links={link.id: {"id": link.id} for link in links.values()},
        posts={p.id: p for p in posts},
    )

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(json_dumper.dumps(doc, inject_type=False))

    print(f"Wrote {len(posts)} posts, {len(users)} users, {len(links)} links to {OUT}")


if __name__ == "__main__":
    main()
