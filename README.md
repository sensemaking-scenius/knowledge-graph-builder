# Telegram Community Knowledge Graph Builder

A Python ETL pipeline that extracts messages from Telegram channels/groups, transforms them into a semantic knowledge graph using the [SIOC ontology](http://rdfs.org/sioc/spec/) and [LinkML](https://linkml.io/), and loads the resulting RDF into an [Oxigraph](https://github.com/oxigraph/oxigraph) triplestore for SPARQL querying.

## Pipeline

```
Telegram API
     │
     ▼
┌─────────┐   messages.jsonl        ┌───────────┐   linkml_graph.json
│ extract  │───participants.jsonl───▶│ transform │──────────────────────┐
│          │   channel.json          └───────────┘                      │
│          │   topics.json                                              ▼
└──────────┘                                                    ┌─────────────┐   sioc_graph.ttl
                                                                │  serialize  │────────────────┐
                                                                └─────────────┘                │
                                                                                    ┌──────────┤
                                                                                    ▼          ▼
                                                                             ┌────────┐  ┌────────┐
                                                                             │  load  │  │  demo  │
                                                                             │(store) │  │(in-mem)│
                                                                             └────────┘  └────────┘
```

| Stage | Module | Input | Output |
|-------|--------|-------|--------|
| **Extract** | `builder.extract` | Telegram API | `data/raw/` (messages, participants, channel, topics) |
| **Transform** | `builder.transform` | `data/raw/*.jsonl` + `*.json` | `data/graph/linkml_graph.json` |
| **Serialize** | `builder.serialize` | LinkML JSON + schema | `data/rdf/sioc_graph.ttl` |
| **Load** | `builder.load` | Turtle file | Oxigraph server (HTTP POST) |

## Features

- **Incremental extraction** — date-bounded (`--days N`), full history with incremental updates (`--full`), or fresh re-fetch (`--fresh`)
- **Forum thread support** — maps Telegram forum topics to `sioc:Thread` with names
- **Reactions & engagement** — reaction counts, individual emoji reactions, view counts, reply counts
- **Media classification** — photo, video, document, webpage, audio, sticker via `MediaType` enum
- **Service actions** — join/leave/pin/title changes via `ServiceActionType` enum
- **Entity extraction** — hashtags → topics, @mentions, URLs, reply chains, forwards
- **Rich dashboard** — 11-section CLI dashboard via `just demo` (community snapshot, top contributors, reply network, forum threads, media breakdown, and more)
- **Schema-driven** — LinkML schema → auto-generated Python models → RDF/Turtle → SPARQL

## Data Model

The schema (`schemas/sioc.yaml`) defines 6 classes and 2 enums:

| Class | Ontology Mapping | Description |
|-------|-----------------|-------------|
| **GraphDocument** | (tree root) | Root container |
| **Community** | `sioc:Community` | Telegram channel/group |
| **Thread** | `sioc:Thread` | Forum topic |
| **UserAccount** | `sioc:UserAccount` | Message author |
| **Post** | `sioc:Post` | Individual message (22 slots) |
| **Link** | `schema:URL` | Extracted URL |

| Enum | Values |
|------|--------|
| **MediaType** | photo, video, document, webpage, audio, sticker, other |
| **ServiceActionType** | join, leave, pin, title_change, photo_change, other |

### Key Ontology Prefixes

| Prefix | Namespace |
|--------|-----------|
| `sioc:` | `http://rdfs.org/sioc/ns#` |
| `dcterms:` | `http://purl.org/dc/terms/` |
| `schema:` | `http://schema.org/` |
| `foaf:` | `http://xmlns.com/foaf/0.1/` |
| `tg:` | `https://example.org/telegram/` |

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
| `just extract-full` | Full history, incremental on subsequent runs |
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
│   └── sioc.yaml                  # LinkML schema (SIOC-aligned)
├── src/builder/
│   ├── __init__.py
│   ├── config.py                  # Paths, env vars, URI helpers
│   ├── extract.py                 # Stage 1: Telegram API → raw files
│   ├── transform/                 # Stage 2: raw → LinkML graph
│   │   ├── __init__.py            #   Orchestrator + graph assembly
│   │   ├── channel.py             #   Community + thread builders
│   │   ├── users.py               #   UserAccount builder
│   │   ├── messages.py            #   Post builder
│   │   └── entities.py            #   Hashtags, mentions, URLs, replies
│   ├── serialize.py               # Stage 3: LinkML JSON → RDF/Turtle
│   ├── load.py                    # Stage 4: Turtle → Oxigraph store
│   ├── query.py                   # Demo dashboard (11-section rich CLI)
│   └── models.py                  # Auto-generated from schema (don't edit)
├── data/
│   ├── raw/                       # Extract output (messages, participants, etc.)
│   ├── graph/                     # Transform output (linkml_graph.json)
│   ├── rdf/                       # Serialize output (sioc_graph.ttl)
│   └── store/                     # Load output (Oxigraph database)
├── docs/
│   ├── SETUP.md                   # Quick setup guide
│   ├── PIPELINE.md                # Pipeline architecture details
│   └── GRAPH.md                   # Graph inventory (what's in the data)
├── docker-compose.yml             # Oxigraph triplestore service
├── justfile                       # Task automation recipes
├── pyproject.toml                 # Dependencies (uv)
└── .env                           # Telegram credentials (create this)
```

## Example SPARQL Queries

### Posts with reactions

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX tg:   <https://example.org/telegram/>

SELECT ?post ?content ?count
WHERE {
  ?post a sioc:Post ;
        sioc:content ?content ;
        tg:reaction_count ?count .
}
ORDER BY DESC(?count)
LIMIT 10
```

### Forum thread activity

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX tg:   <https://example.org/telegram/>

SELECT ?name (COUNT(?post) AS ?posts)
WHERE {
  ?post a sioc:Post ;
        tg:has_thread ?thread .
  ?thread foaf:name ?name .
}
GROUP BY ?name
ORDER BY DESC(?posts)
```

### Posts with media

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX tg:   <https://example.org/telegram/>

SELECT ?post ?content ?mtype
WHERE {
  ?post a sioc:Post ;
        sioc:content ?content ;
        tg:media_type ?mtype .
}
LIMIT 10
```

### Reply threads

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?replier_name ?original_name (COUNT(*) AS ?count)
WHERE {
  ?reply sioc:has_creator ?replier ;
         sioc:reply_of ?parent .
  ?parent sioc:has_creator ?original .
  OPTIONAL { ?replier foaf:accountName ?replier_name }
  OPTIONAL { ?original foaf:accountName ?original_name }
}
GROUP BY ?replier_name ?original_name
ORDER BY DESC(?count)
LIMIT 10
```

## Dependencies

- **[linkml](https://linkml.io/)** — schema definition + code generation
- **[linkml-runtime](https://linkml.io/)** — runtime support for generated models
- **[Oxigraph](https://github.com/oxigraph/oxigraph)** — RDF triplestore (Docker for persistence, pyoxigraph for in-memory demo)
- **[telethon](https://docs.telethon.dev/)** — Telegram client API
- **[rich](https://github.com/Textualize/rich)** — terminal formatting
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** — environment variable management

## Resources

- [SIOC Ontology Specification](http://rdfs.org/sioc/spec/)
- [LinkML Documentation](https://linkml.io/)
- [Oxigraph Documentation](https://github.com/oxigraph/oxigraph)
- [Telethon Documentation](https://docs.telethon.dev/)
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
