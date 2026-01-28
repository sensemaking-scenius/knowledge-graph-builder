import json
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import PeerChannel

load_dotenv()

API_ID = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]
SESSION = os.environ.get("TG_SESSION", "tg.session")
ENTITY = os.environ["TG_ENTITY"]

OUT = "data/raw/messages_last_7_days.jsonl"

def coerce_entity(entity_str: str):
    s = entity_str.strip()
    # Telegram "supergroup/channel" ids are often represented as -100<channel_id>
    if s.startswith("-100") and s[4:].isdigit():
        channel_id = int(s[4:])  # drop the -100 prefix
        return PeerChannel(channel_id)
    # If it's a plain negative int (e.g. -123...), let Telethon try
    if s.lstrip("-").isdigit():
        return int(s)
    return s  # @username, invite link, etc.

async def main():
    since = datetime.now(timezone.utc) - timedelta(days=7)

    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        entity = coerce_entity(ENTITY)
        entity = await client.get_entity(entity)  # now resolves PeerChannel properly

        count = 0
        os.makedirs(os.path.dirname(OUT), exist_ok=True)

        with open(OUT, "w", encoding="utf-8") as f:
            async for msg in client.iter_messages(entity, limit=None):
                if not msg.date:
                    continue
                if msg.date < since:
                    break
                f.write(json.dumps(msg.to_dict(), ensure_ascii=False, default=str) + "\n")
                count += 1

        print(f"Wrote {count} messages to {OUT}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
