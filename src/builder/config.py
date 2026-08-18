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
ANNOTATIONS_DIR = ROOT / "data" / "annotations"

# Pipeline files
MESSAGES_FILE = RAW_DIR / "messages.jsonl"
CHANNEL_FILE = RAW_DIR / "channel.json"
PARTICIPANTS_FILE = RAW_DIR / "participants.jsonl"
FORUMS_FILE = RAW_DIR / "forums.json"
OVERRIDES_FILE = RAW_DIR / "user_overrides.yaml"
GRAPH_FILE = GRAPH_DIR / "linkml_graph.json"
TURTLE_FILE = RDF_DIR / "sioc_graph.ttl"
SCHEMA_FILE = ROOT / "schemas" / "sioc.yaml"

# Telegram config (required only for extraction)
TG_API_ID = int(os.environ.get("TG_API_ID", "0"))
TG_API_HASH = os.environ.get("TG_API_HASH", "")
TG_SESSION = os.environ.get("TG_SESSION", "tg.session")
TG_ENTITY = os.environ.get("TG_ENTITY", "")

# Extraction settings
EXTRACT_DAYS = int(os.environ.get("EXTRACT_DAYS", "30"))
STATE_FILE = RAW_DIR / "extract_state.json"

# Harmonica settings
HARMONICA_API_KEY = os.environ.get("HARMONICA_API_KEY", "")
HARMONICA_API_URL = os.environ.get("HARMONICA_API_URL", "https://app.harmonica.chat")
SESSIONS_FILE = ANNOTATIONS_DIR / "sessions.json"
BATCH_SIZE = int(os.environ.get("ANNOTATE_BATCH_SIZE", "8"))
MIN_PARTICIPANTS = int(os.environ.get("ANNOTATE_MIN_PARTICIPANTS", "3"))
CONFIDENCE_THRESHOLD = float(os.environ.get("ANNOTATE_CONFIDENCE_THRESHOLD", "0.6"))


# URI helpers
def channel_uri(channel_id: int) -> str:
    return f"tg:channel/{channel_id}"


def site_uri() -> str:
    return "tg:site/telegram"


def forum_uri(channel_id: int, topic_id: int | None = None) -> str:
    if topic_id is not None:
        return f"tg:channel/{channel_id}/forum/{topic_id}"
    return f"tg:channel/{channel_id}/forum"


def thread_uri(channel_id: int, topic_id: int) -> str:
    return f"tg:channel/{channel_id}/thread/{topic_id}"


def message_uri(channel_id: int, msg_id: int) -> str:
    return f"tg:channel/{channel_id}/message/{msg_id}"


def user_uri(user_id: int) -> str:
    return f"tg:user/{user_id}"


def person_uri(user_id: int) -> str:
    return f"tg:person/{user_id}"


def concept_uri(tag: str) -> str:
    return f"tg:topic/{tag.lower()}"


def attachment_uri(channel_id: int, msg_id: int, index: int = 0) -> str:
    return f"tg:attachment/{channel_id}/{msg_id}/{index}"


def poll_uri(channel_id: int, msg_id: int) -> str:
    return f"tg:poll/{channel_id}/{msg_id}"


def document_uri(url: str) -> str:
    return url


def graph_uri(channel_id: int) -> str:
    return f"tg:graph/{channel_id}"


def annotation_uri(session_id: str, index: int) -> str:
    return f"tg:annotation/{session_id}/{index}"


def annotation_session_uri(session_id: str) -> str:
    return f"tg:annotation-session/{session_id}"
