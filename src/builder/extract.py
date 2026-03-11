import asyncio
import json

from datetime import datetime, timedelta, timezone

from telethon import TelegramClient
from telethon.tl.types import PeerChannel

from builder.config import TG_API_ID, TG_API_HASH, TG_SESSION, TG_ENTITY, MESSAGES_FILE


def coerce_entity(entity_str: str):
    """Parse TG_ENTITY into a form Telethon can resolve."""
    s = entity_str.strip()
    # Telegram "supergroup/channel" ids are often represented as -100<channel_id>
    if s.startswith("-100") and s[4:].isdigit():
        channel_id = int(s[4:])  # drop the -100 prefix
        return PeerChannel(channel_id)
    # Plain negative int — let Telethon try
    if s.lstrip("-").isdigit():
        return int(s)
    return s  # @username, invite link, etc.


async def fetch(days: int = 7) -> int:
    """Fetch messages from the configured Telegram entity.

    Returns the number of messages written.
    """
    since = datetime.now(timezone.utc) - timedelta(days=days)

    async with TelegramClient(TG_SESSION, TG_API_ID, TG_API_HASH) as client:
        entity = coerce_entity(TG_ENTITY)
        entity = await client.get_entity(entity)

        count = 0
        MESSAGES_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
            async for msg in client.iter_messages(entity, limit=None):
                if not msg.date:
                    continue
                if msg.date < since:
                    break
                f.write(json.dumps(msg.to_dict(), ensure_ascii=False, default=str) + "\n")
                count += 1

    return count


def main() -> None:
    count = asyncio.run(fetch())
    print(f"Wrote {count} messages to {MESSAGES_FILE}")


if __name__ == "__main__":
    main()
