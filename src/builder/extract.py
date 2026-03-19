import argparse
import asyncio
import json
import logging

from datetime import datetime, timedelta, timezone

from telethon import TelegramClient
from telethon.tl.types import PeerChannel

from builder.config import (
    TG_API_ID, TG_API_HASH, TG_SESSION, TG_ENTITY,
    MESSAGES_FILE, PARTICIPANTS_FILE, CHANNEL_FILE, TOPICS_FILE,
    STATE_FILE, EXTRACT_DAYS,
)

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# State management for incremental extraction
# ---------------------------------------------------------------------------

def load_state() -> dict | None:
    """Load extraction state from disk, or None if no state exists."""
    if not STATE_FILE.exists():
        return None
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict) -> None:
    """Persist extraction state to disk."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Entity coercion
# ---------------------------------------------------------------------------

def coerce_entity(entity_str: str):
    """Parse TG_ENTITY into a form Telethon can resolve."""
    s = entity_str.strip()
    if s.startswith("-100") and s[4:].isdigit():
        channel_id = int(s[4:])
        return PeerChannel(channel_id)
    if s.lstrip("-").isdigit():
        return int(s)
    return s


# ---------------------------------------------------------------------------
# Message fetching — date-bounded (default mode)
# ---------------------------------------------------------------------------

async def fetch(days: int = EXTRACT_DAYS) -> int:
    """Fetch messages bounded by date. Overwrites messages file.

    Returns the number of messages written.
    """
    since = datetime.now(timezone.utc) - timedelta(days=days)

    async with TelegramClient(TG_SESSION, TG_API_ID, TG_API_HASH) as client:
        client.flood_sleep_threshold = 120

        entity = coerce_entity(TG_ENTITY)
        entity = await client.get_entity(entity)

        count = 0
        MESSAGES_FILE.parent.mkdir(parents=True, exist_ok=True)

        log.info("Fetching messages from last %d days...", days)

        with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
            async for msg in client.iter_messages(entity, limit=None):
                if not msg.date:
                    continue
                if msg.date < since:
                    break
                f.write(json.dumps(msg.to_dict(), ensure_ascii=False, default=str) + "\n")
                count += 1

                if count % 100 == 0:
                    log.info("  %d messages fetched...", count)
                    await asyncio.sleep(0.5)

        log.info("Fetched %d messages total.", count)

    return count


# ---------------------------------------------------------------------------
# Message fetching — full history (incremental)
# ---------------------------------------------------------------------------

async def fetch_full() -> int:
    """Fetch full message history incrementally.

    First run: fetches everything newest→oldest, appends to messages file.
    Subsequent runs: fetches only messages newer than the saved newest_msg_id.
    Saves state every 500 messages for resume on interruption.

    Returns the number of new messages written.
    """
    state = load_state()

    async with TelegramClient(TG_SESSION, TG_API_ID, TG_API_HASH) as client:
        client.flood_sleep_threshold = 120

        entity = coerce_entity(TG_ENTITY)
        entity = await client.get_entity(entity)
        channel_id = getattr(entity, "id", None)

        MESSAGES_FILE.parent.mkdir(parents=True, exist_ok=True)

        if state and state.get("complete") and state.get("channel_id") == channel_id:
            # Incremental: fetch only new messages since last run
            return await _fetch_incremental(client, entity, state)
        else:
            # First run: fetch entire history
            return await _fetch_full_history(client, entity, channel_id)


async def _fetch_full_history(client: TelegramClient, entity, channel_id: int | None) -> int:
    """Fetch entire history from newest to oldest. Overwrites messages file."""
    count = 0
    newest_id: int | None = None
    oldest_id: int | None = None

    log.info("Full history extraction: fetching all messages newest→oldest...")

    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        async for msg in client.iter_messages(entity, limit=None):
            if not msg.date:
                continue
            msg_dict = msg.to_dict()
            f.write(json.dumps(msg_dict, ensure_ascii=False, default=str) + "\n")

            msg_id = msg_dict.get("id")
            if msg_id is not None:
                if newest_id is None:
                    newest_id = int(msg_id)
                oldest_id = int(msg_id)

            count += 1

            if count % 100 == 0:
                log.info("  %d messages fetched...", count)
                await asyncio.sleep(0.5)

            if count % 500 == 0:
                save_state({
                    "channel_id": channel_id,
                    "newest_msg_id": newest_id,
                    "oldest_msg_id": oldest_id,
                    "total_fetched": count,
                    "complete": False,
                })

    # Mark complete
    save_state({
        "channel_id": channel_id,
        "newest_msg_id": newest_id,
        "oldest_msg_id": oldest_id,
        "total_fetched": count,
        "complete": True,
    })

    log.info("Full history complete: %d messages (IDs %s→%s).", count, newest_id, oldest_id)
    return count


async def _fetch_incremental(client: TelegramClient, entity, state: dict) -> int:
    """Fetch only messages newer than state's newest_msg_id. Prepends to existing file."""
    saved_newest = state.get("newest_msg_id")
    if saved_newest is None:
        log.warning("State exists but no newest_msg_id — falling back to full fetch.")
        return await _fetch_full_history(client, entity, state.get("channel_id"))

    log.info("Incremental extraction: fetching messages newer than ID %d...", saved_newest)

    # Fetch new messages into a temporary buffer
    new_messages: list[str] = []
    new_newest_id = saved_newest
    count = 0

    async for msg in client.iter_messages(entity, limit=None, min_id=saved_newest):
        if not msg.date:
            continue
        msg_dict = msg.to_dict()
        line = json.dumps(msg_dict, ensure_ascii=False, default=str) + "\n"
        new_messages.append(line)

        msg_id = msg_dict.get("id")
        if msg_id is not None and int(msg_id) > new_newest_id:
            new_newest_id = int(msg_id)

        count += 1

        if count % 100 == 0:
            log.info("  %d new messages fetched...", count)
            await asyncio.sleep(0.5)

    if not new_messages:
        log.info("No new messages since last run.")
        return 0

    # Prepend new messages to existing file (new messages come first = newest→oldest)
    existing_content = b""
    if MESSAGES_FILE.exists():
        existing_content = MESSAGES_FILE.read_bytes()

    with open(MESSAGES_FILE, "wb") as f:
        for line in new_messages:
            f.write(line.encode("utf-8"))
        f.write(existing_content)

    # Update state
    save_state({
        **state,
        "newest_msg_id": new_newest_id,
        "total_fetched": state.get("total_fetched", 0) + count,
        "complete": True,
    })

    log.info("Incremental: added %d new messages (newest ID now %d).", count, new_newest_id)
    return count


# ---------------------------------------------------------------------------
# Participants & channel metadata
# ---------------------------------------------------------------------------

async def fetch_participants() -> int:
    """Fetch participant metadata from the configured Telegram entity."""
    async with TelegramClient(TG_SESSION, TG_API_ID, TG_API_HASH) as client:
        client.flood_sleep_threshold = 120

        entity = coerce_entity(TG_ENTITY)
        entity = await client.get_entity(entity)

        PARTICIPANTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        count = 0

        log.info("Fetching participants...")

        with open(PARTICIPANTS_FILE, "w", encoding="utf-8") as f:
            async for user in client.iter_participants(entity):
                record = {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "bot": getattr(user, "bot", None),
                    "verified": getattr(user, "verified", None),
                    "premium": getattr(user, "premium", None),
                }
                f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
                count += 1

        log.info("Fetched %d participants.", count)

    return count


async def fetch_channel_metadata() -> None:
    """Fetch channel/supergroup metadata and write to channel.json."""
    from telethon.tl.functions.channels import GetFullChannelRequest

    async with TelegramClient(TG_SESSION, TG_API_ID, TG_API_HASH) as client:
        client.flood_sleep_threshold = 120

        entity = coerce_entity(TG_ENTITY)
        entity = await client.get_entity(entity)

        full = await client(GetFullChannelRequest(entity))
        chat = full.chats[0] if full.chats else None
        full_chat = full.full_chat

        metadata = {
            "id": chat.id if chat else None,
            "title": getattr(chat, "title", None),
            "about": getattr(full_chat, "about", None),
            "members_count": getattr(full_chat, "participants_count", None),
        }

        CHANNEL_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CHANNEL_FILE, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        log.info("Wrote channel metadata to %s", CHANNEL_FILE)


async def fetch_forum_topics() -> int:
    """Fetch forum topic names and write to topics.json.

    Returns the number of topics written.
    """
    from telethon.tl.functions.messages import GetForumTopicsRequest

    async with TelegramClient(TG_SESSION, TG_API_ID, TG_API_HASH) as client:
        client.flood_sleep_threshold = 120

        entity = coerce_entity(TG_ENTITY)
        entity = await client.get_entity(entity)

        topics: dict[int, str] = {}
        offset_date: datetime | None = None
        offset_id = 0
        offset_topic = 0

        log.info("Fetching forum topics...")

        while True:
            result = await client(GetForumTopicsRequest(
                peer=entity,
                offset_date=offset_date,
                offset_id=offset_id,
                offset_topic=offset_topic,
                limit=100,
            ))

            if not result.topics:
                break

            for topic in result.topics:
                tid = getattr(topic, "id", None)
                title = getattr(topic, "title", None)
                if tid is not None and title:
                    topics[tid] = title

            # Pagination: use the last topic for offsets
            last = result.topics[-1]
            offset_id = getattr(last, "top_message", 0)
            offset_topic = getattr(last, "id", 0)
            offset_date = getattr(last, "date", None)

            if len(result.topics) < 100:
                break

            await asyncio.sleep(0.5)

        TOPICS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TOPICS_FILE, "w", encoding="utf-8") as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)

        log.info("Fetched %d forum topics to %s", len(topics), TOPICS_FILE)

    return len(topics)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Telegram messages")
    parser.add_argument("--days", type=int, default=None,
                        help=f"Number of days to fetch (default: {EXTRACT_DAYS})")
    parser.add_argument("--full", action="store_true",
                        help="Fetch full history (incremental on subsequent runs)")
    parser.add_argument("--fresh", action="store_true",
                        help="Clear state and fetch full history from scratch")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    if args.fresh:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
            log.info("Cleared extraction state.")
        args.full = True

    if args.full and args.days:
        parser.error("Cannot use --full and --days together")

    count, p_count = asyncio.run(_run_extract(
        days=args.days or EXTRACT_DAYS,
        full=args.full,
    ))
    print(f"Wrote {count} messages to {MESSAGES_FILE}")
    print(f"Wrote {p_count} participants to {PARTICIPANTS_FILE}")


async def _run_extract(days: int = EXTRACT_DAYS, full: bool = False) -> tuple[int, int]:
    """Run message, participant, and channel metadata extraction."""
    if full:
        msg_count = await fetch_full()
    else:
        msg_count = await fetch(days=days)
    p_count = await fetch_participants()
    await fetch_channel_metadata()
    await fetch_forum_topics()
    return msg_count, p_count


if __name__ == "__main__":
    main()
