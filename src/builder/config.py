import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project root
ROOT = Path(__file__).parent.parent.parent

# Data directories
RAW_DIR = ROOT / "data" / "raw"
GRAPH_DIR = ROOT / "data" / "graph"
RDF_DIR = ROOT / "data" / "rdf"
STORE_DIR = ROOT / "data" / "store"

# Pipeline files
MESSAGES_FILE = RAW_DIR / "messages.jsonl"
CHANNEL_FILE = RAW_DIR / "channel.json"
PARTICIPANTS_FILE = RAW_DIR / "participants.jsonl"
TOPICS_FILE = RAW_DIR / "topics.json"
GRAPH_FILE = GRAPH_DIR / "linkml_graph.json"
TURTLE_FILE = RDF_DIR / "sioc_graph.ttl"
SCHEMA_FILE = ROOT / "schemas" / "sioc.yaml"

# Telegram config
TG_API_ID = int(os.environ["TG_API_ID"])
TG_API_HASH = os.environ["TG_API_HASH"]
TG_SESSION = os.environ.get("TG_SESSION", "tg.session")
TG_ENTITY = os.environ["TG_ENTITY"]

# Extraction settings
EXTRACT_DAYS = int(os.environ.get("EXTRACT_DAYS", "30"))
STATE_FILE = RAW_DIR / "extract_state.json"


# URI helpers
def channel_uri(channel_id: int) -> str:
    return f"tg:channel/{channel_id}"


def thread_uri(channel_id: int, topic_id: int) -> str:
    return f"tg:channel/{channel_id}/thread/{topic_id}"


def message_uri(channel_id: int, msg_id: int) -> str:
    return f"tg:channel/{channel_id}/message/{msg_id}"


def user_uri(user_id: int) -> str:
    return f"tg:user/{user_id}"


def person_uri(user_id: int) -> str:
    return f"tg:person/{user_id}"


def topic_uri(tag: str) -> str:
    return f"tg:topic/{tag.lower()}"


def graph_uri(channel_id: int) -> str:
    return f"tg:graph/{channel_id}"
