import json
import os
import re
from datetime import timezone

INP = "data/raw/messages_last_7_days.jsonl"
OUT = "data/raw/canonical_last_7_days.jsonl"

URL_RE = re.compile(r"(https?://[^\s<>()\[\]{}\"']+)", re.IGNORECASE)

def to_iso_utc(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()

def extract_chat_id(peer_id_obj):
    # Telethon encodes peer_id like {"_":"PeerChannel","channel_id":...} etc.
    if not isinstance(peer_id_obj, dict):
        return None
    if "channel_id" in peer_id_obj:
        return f"-100{peer_id_obj['channel_id']}"
    if "chat_id" in peer_id_obj:
        return f"-{peer_id_obj['chat_id']}"
    if "user_id" in peer_id_obj:
        return str(peer_id_obj["user_id"])
    return None

def extract_from_user_id(obj):
    # Prefer from_id.user_id if present, else None
    from_id = obj.get("from_id")
    if isinstance(from_id, dict) and "user_id" in from_id:
        return int(from_id["user_id"])
    return None

def extract_reply_to_message_id(obj):
    r = obj.get("reply_to")
    if isinstance(r, dict) and "reply_to_msg_id" in r:
        return int(r["reply_to_msg_id"])
    return None

def build_permalink(chat_id, message_id):
    # Best-effort; true permalink depends on whether the group has a public username.
    # For now keep None; we can fill later if you provide group username.
    return None

def extract_urls(text):
    if not text:
        return []
    return URL_RE.findall(text)

def simplify_entities(entities):
    out=[]
    if not entities:
        return out
    for e in entities:
        # e is already a dict in your raw JSON
        if not isinstance(e, dict):
            continue
        item = {
            "type": e.get("_"),
            "offset": e.get("offset"),
            "length": e.get("length"),
        }
        if "url" in e:
            item["url"] = e.get("url")
        # mention-name entities can embed user_id-ish structures depending on constructor
        if "user_id" in e:
            item["user_id"] = e.get("user_id")
        out.append(item)
    return out

def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    n_in = 0
    n_out = 0

    with open(INP, "r", encoding="utf-8") as f_in, open(OUT, "w", encoding="utf-8") as f_out:
        for line in f_in:
            n_in += 1
            obj = json.loads(line)

            chat_id = extract_chat_id(obj.get("peer_id"))
            msg_id = obj.get("id")
            created = obj.get("date")
            # Telethon to_dict() already serializes datetime to ISO-ish string sometimes,
            # but treat it as a string and pass through if so.
            if isinstance(created, str):
                created_at = created
            else:
                created_at = to_iso_utc(created)

            text = obj.get("message") or ""
            from_user_id = extract_from_user_id(obj)
            reply_to_message_id = extract_reply_to_message_id(obj)
            urls = extract_urls(text)

            if chat_id is None or msg_id is None or created_at is None:
                # Skip messages missing core identifiers
                continue

            canonical = {
                "chat_id": chat_id,
                "message_id": int(msg_id),
                "created_at": created_at,
                "text": text,
                "from_user_id": from_user_id,
                "reply_to_message_id": reply_to_message_id,
                "permalink": build_permalink(chat_id, int(msg_id)),
                "urls": urls,
                "forwards": obj.get("forwards"),
                "pinned": bool(obj.get("pinned")) if obj.get("pinned") is not None else None,
                "entities": simplify_entities(obj.get("entities")),
            }

            f_out.write(json.dumps(canonical, ensure_ascii=False) + "\n")
            n_out += 1

    print(f"Read {n_in} lines, wrote {n_out} canonical messages to {OUT}")

if __name__ == "__main__":
    main()
