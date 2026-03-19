# Telegram Community Knowledge Graph Builder

A Python ETL pipeline that extracts messages from Telegram channels/groups, transforms them into a semantic knowledge graph using the [SIOC ontology](http://rdfs.org/sioc/spec/) and [LinkML](https://linkml.io/), and loads the resulting RDF into an [Oxigraph](https://github.com/oxigraph/oxigraph) triplestore for SPARQL querying.

## Pipeline

```
Telegram API
     |
     v
+---------+   messages.jsonl        +-----------+   linkml_graph.json
| extract |---participants.jsonl--->| transform |----------------------+
|         |   channel.json          +-----------+                      |
|         |   forums.json                                              v
+---------+                                                    +-------------+   sioc_graph.ttl
                                                               |  serialize  |----------------+
                                                               +-------------+                |
                                                                                    +---------+
                                                                                    v         v
                                                                             +--------+  +--------+
                                                                             |  load  |  |  demo  |
                                                                             |(Docker)|  |(in-mem)|
                                                                             +--------+  +--------+
```

| Stage | Module | Input | Output |
|-------|--------|-------|--------|
| **Extract** | `builder.extract` | Telegram API | `data/raw/` (messages, participants, channel, forums) |
| **Transform** | `builder.transform` | `data/raw/*.jsonl` + `*.json` | `data/graph/linkml_graph.json` |
| **Serialize** | `builder.serialize` | LinkML JSON + schema | `data/rdf/sioc_graph.ttl` |
| **Load** | `builder.load` | Turtle file | Oxigraph server (HTTP POST to Docker container) |

## Features

- **SIOC-aligned data model** — 13 classes mapped to SIOC, FOAF, Dublin Core, and SKOS ontologies
- **Incremental extraction** — date-bounded (`--days N`), full history with incremental updates (`--full`), or fresh re-fetch (`--fresh`). Crash-safe: resumes from checkpoint if interrupted
- **Account-safe rate limiting** — ~20 requests/minute via Telethon's `wait_time=3`, auto-waits through flood bans up to 5 minutes, single client session per run
- **Forum hierarchy** — Community → Site → Forum (supergroup + topic channels) → Thread
- **Entity extraction** — hashtags → `skos:Concept`, URLs → `LinkedDocument` with preview metadata, media → `Attachment` with MIME types
- **Reply + forward graphs** — `sioc:reply_of`/`has_reply` (both directions) and `sioc:sibling` for cross-posted content
- **Rich dashboard** — 11-section CLI dashboard via `just demo` (community snapshot, top contributors, reply network, forum hierarchy, topic distribution, and more)
- **Schema-driven** — LinkML schema → auto-generated Python models → RDF/Turtle → SPARQL

## Data Model

The schema (`schemas/sioc.yaml`) defines 13 classes and 1 enum:

| Class | Ontology Mapping | Description |
|-------|-----------------|-------------|
| **GraphDocument** | *(tree root)* | Root container for all entities |
| **Community** | `sioc:Community` | The community (people + purpose) |
| **Site** | `sioc:Site` | Telegram platform |
| **Forum** | `sioc:Forum` | Supergroup (organizational) or topic channel (where messages live) |
| **Thread** | `sioc:Thread` | Reply thread within a topic channel |
| **User** | `sioc:User` | Telegram account |
| **Person** | `foaf:Person` | Real person behind an account |
| **Post** | `sioc:Post` | Individual message |
| **Poll** | `sioc_types:Poll` | Poll attached to a message |
| **Attachment** | `foaf:Document` | Media file (photo, video, document, etc.) |
| **LinkedDocument** | `foaf:Document` | Linked web page with preview metadata |
| **Concept** | `skos:Concept` | Hashtag topic |
| **Reaction** | `tg:Reaction` | Emoji reaction *(schema-only, not yet populated)* |

| Enum | Values |
|------|--------|
| **MediaType** | photo, video, document, audio, voice, sticker, animation, other |

### Key Ontology Prefixes

| Prefix | Namespace |
|--------|-----------|
| `sioc:` | `http://rdfs.org/sioc/ns#` |
| `sioc_types:` | `http://rdfs.org/sioc/types#` |
| `dcterms:` | `http://purl.org/dc/terms/` |
| `dc:` | `http://purl.org/dc/elements/1.1/` |
| `foaf:` | `http://xmlns.com/foaf/0.1/` |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` |
| `tg:` | `https://example.org/telegram/` |

### Entity Hierarchy

```
sioc:Community — "Sensemaking Scenius"
  +-- dcterms:hasPart --> sioc:Site — "Telegram"
        +-- sioc:host_of --> sioc:Forum — Supergroup (organizational)
        |     +-- sioc:parent_of --> sioc:Forum — "General" (topic channel)
        |     +-- sioc:parent_of --> sioc:Forum — "Resources" (topic channel)
        |     +-- sioc:parent_of --> sioc:Forum — "Events" (topic channel)
        +-- sioc:host_of --> sioc:Forum — Side Channel (independent)
```

## Quick Start

### Prerequisites

- **Python 3.13+**
- **[uv](https://github.com/astral-sh/uv)** — Python package manager
- **[just](https://github.com/casey/just)** — command runner
- **A Docker-compatible runtime** (e.g. [Colima](https://github.com/ablemachines/colima), [Docker Desktop](https://docs.docker.com/get-docker/)) — for the Oxigraph triplestore
- **Telegram API credentials** from [my.telegram.org](https://my.telegram.org)

### Setup

```bash
git clone <repository-url>
cd knowledge-graph-builder
uv sync
```

Create a `.env` file (see `.env.example`):

```env
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
TG_SESSION=tg.session
TG_ENTITY=@channel_username_or_id
```

### Run

```bash
# Start the Oxigraph triplestore
just up

# Extract last 7 days + build graph + load into Oxigraph
just extract 7
just build

# Query via CLI dashboard (in-memory, no server needed) or SPARQL endpoint
just demo
just query
```

First run will prompt for Telegram phone number and verification code.

## All Commands

### Pipeline

| Command | Description |
|---------|-------------|
| `just run-all` | Full pipeline: extract → transform → serialize → load |
| `just build` | Build only: transform → serialize → load (skips extraction) |
| `just extract` | Extract last 30 days (default) |
| `just extract 7` | Extract last N days |
| `just extract-full` | Full history, incremental on subsequent runs (crash-safe) |
| `just extract-fresh` | Clear state, re-fetch everything |
| `just transform` | Raw JSON → LinkML graph document |
| `just serialize` | LinkML JSON → RDF/Turtle |
| `just load` | Turtle → Oxigraph server (requires `just up`) |

### Oxigraph Server

| Command | Description |
|---------|-------------|
| `just up` | Start Oxigraph container (Docker, `localhost:7878`) |
| `just down` | Stop Oxigraph container |
| `just logs` | Tail Oxigraph container logs |

### Querying

| Command | Description |
|---------|-------------|
| `just demo` | Rich CLI dashboard (reads Turtle directly, no server needed) |
| `just query` | SPARQL count query against running server |

### Tooling

| Command | Description |
|---------|-------------|
| `just status` | Show data directory contents |
| `just clean` | Remove generated data, preserve directories |
| `just gen-model` | Regenerate `models.py` from schema |
| `just validate` | Validate LinkML schema |
| `just typecheck` | Run Pyright type checker |

## Project Structure

```
knowledge-graph-builder/
├── schemas/
│   └── sioc.yaml                  # LinkML schema (SIOC-aligned, 13 classes)
├── src/builder/
│   ├── __init__.py
│   ├── config.py                  # Paths, env vars, URI helpers
│   ├── extract.py                 # Stage 1: Telegram API → raw files
│   ├── transform/                 # Stage 2: raw → LinkML graph
│   │   ├── __init__.py            #   Orchestrator + graph assembly
│   │   ├── channel.py             #   Community + Site + Forum hierarchy
│   │   ├── users.py               #   User + Person builder
│   │   ├── messages.py            #   Post builder (replies, forwards, media)
│   │   └── entities.py            #   Hashtags → Concept, URLs → LinkedDocument
│   ├── serialize.py               # Stage 3: LinkML JSON → RDF/Turtle
│   ├── load.py                    # Stage 4: Turtle → Oxigraph (HTTP POST)
│   ├── query.py                   # Demo dashboard (11-section rich CLI)
│   └── models.py                  # Auto-generated from schema (don't edit)
├── data/
│   ├── raw/                       # Extract output (messages, participants, etc.)
│   ├── graph/                     # Transform output (linkml_graph.json)
│   ├── rdf/                       # Serialize output (sioc_graph.ttl)
│   └── store/                     # Oxigraph database (Docker volume)
├── docs/
│   ├── SETUP.md                   # Quick setup guide
│   ├── PIPELINE.md                # Pipeline architecture details
│   ├── GRAPH.md                   # Graph inventory (what's in the data)
│   ├── sioc.md                    # SIOC ontology reference
│   └── telethon.md                # Telethon field inventory
├── docker-compose.yml             # Oxigraph triplestore service
├── justfile                       # Task automation recipes
├── pyproject.toml                 # Dependencies (uv)
└── .env                           # Telegram credentials (create this)
```

## Example SPARQL Queries

### Forum activity

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>

SELECT ?forum ?name (COUNT(?post) AS ?posts)
WHERE {
  ?post a sioc:Post ;
        sioc:has_container ?forum .
  ?forum sioc:name ?name .
}
GROUP BY ?forum ?name
ORDER BY DESC(?posts)
```

### Reply network

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>

SELECT ?from ?to (COUNT(*) AS ?replies)
WHERE {
  ?reply sioc:has_creator ?replier ;
         sioc:reply_of ?parent .
  ?parent sioc:has_creator ?original .
  ?replier sioc:name ?from .
  ?original sioc:name ?to .
}
GROUP BY ?from ?to
ORDER BY DESC(?replies)
LIMIT 10
```

### Posts with attachments

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX tg:   <https://example.org/telegram/>

SELECT ?post ?content ?mtype
WHERE {
  ?post a sioc:Post ;
        sioc:content ?content ;
        sioc:attachment ?att .
  ?att tg:media_type ?mtype .
}
LIMIT 10
```

### Shared links with metadata

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX dc:   <http://purl.org/dc/elements/1.1/>
PREFIX tg:   <https://example.org/telegram/>

SELECT ?title ?site_name (COUNT(?post) AS ?shares)
WHERE {
  ?post sioc:links_to ?doc .
  ?doc dc:title ?title .
  OPTIONAL { ?doc tg:site_name ?site_name }
}
GROUP BY ?title ?site_name
ORDER BY DESC(?shares)
LIMIT 10
```

### Topic (hashtag) distribution

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?label (COUNT(?post) AS ?posts)
WHERE {
  ?post sioc:topic ?concept .
  ?concept skos:prefLabel ?label .
}
GROUP BY ?label
ORDER BY DESC(?posts)
```

## Dependencies

- **[linkml](https://linkml.io/)** — schema definition + code generation
- **[linkml-runtime](https://linkml.io/)** — runtime support for generated models
- **[Oxigraph](https://github.com/oxigraph/oxigraph)** — RDF triplestore (Docker for persistence, pyoxigraph for in-memory demo)
- **[telethon](https://docs.telethon.dev/)** — Telegram client API
- **[rich](https://github.com/Textualized/rich)** — terminal formatting
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** — environment variable management

## Resources

- [SIOC Ontology Specification](http://rdfs.org/sioc/spec/)
- [LinkML Documentation](https://linkml.io/)
- [Oxigraph Documentation](https://github.com/oxigraph/oxigraph)
- [Telethon Documentation](https://docs.telethon.dev/)
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
