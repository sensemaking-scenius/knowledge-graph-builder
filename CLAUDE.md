# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Telegram Community Knowledge Graph Builder — a Python ETL pipeline that extracts messages from Telegram channels/groups, transforms them via a LinkML schema aligned with the SIOC ontology, and loads the resulting RDF into an Oxigraph triplestore for SPARQL querying.

## Commands

All commands use `just` (task runner) and `uv` (Python package manager).

```bash
# Oxigraph server (Docker) — must be running for load/query
just up               # Start Oxigraph container (localhost:7878)
just down             # Stop Oxigraph container
just logs             # Tail Oxigraph logs

# Full pipeline (extract → transform → serialize → load)
just run-all

# Build only (transform → serialize → load, skips extraction)
just build

# Individual pipeline stages
just extract          # Telegram API → data/raw/messages.jsonl
just transform        # Raw JSON → data/graph/linkml_graph.json
just serialize        # LinkML JSON → data/rdf/sioc_graph.ttl
just load             # Turtle → Oxigraph (HTTP POST)

# Querying
just query            # SPARQL count query against running server
just demo             # Rich CLI dashboard (in-memory, no server needed)

# Schema tooling
just gen-model        # Regenerate models.py from schema
just validate         # Validate LinkML schema

# Type checking
just typecheck

# Clean generated data (preserves directory structure)
just clean
```

## Architecture

### 4-Stage Pipeline

```
Telegram API → Extract → Transform → Serialize → Load
                 ↓            ↓            ↓          ↓
              data/raw/    data/graph/   data/rdf/  data/store/
              (messages)   (LinkML JSON)  (Turtle)   (Oxigraph)
```

Each stage is a module in `src/builder/`, invoked via `uv run python -m builder.<stage>`.

| Stage | Module | Input | Output |
|-------|--------|-------|--------|
| **Extract** | `builder.extract` | Telegram API | `messages.jsonl` |
| **Transform** | `builder.transform` | Raw JSON files | `linkml_graph.json` |
| **Serialize** | `builder.serialize` | LinkML JSON + schema | `sioc_graph.ttl` |
| **Load** | `builder.load` | Turtle file | Oxigraph (HTTP POST) |

### Schema-Driven Data Model

The schema lives in `schemas/sioc.yaml` (LinkML format, SIOC ontology-aligned). It defines 13 classes:

- **GraphDocument** — root container (tree_root)
- **Community** → `sioc:Community` — the Telegram channel/group
- **Site** → `sioc:Site` — "Telegram" platform
- **Forum** → `sioc:Forum` — supergroup + topic channels (container hierarchy)
- **Thread** → `sioc:Thread` — forum threads
- **User** → `sioc:User` — message authors (agent accounts)
- **Person** → `foaf:Person` — real people behind accounts
- **Post** → `sioc:Post` — individual messages (with replies, topics, attachments, links)
- **Poll** → `sioc_types:Poll` — poll messages
- **Attachment** → `foaf:Document` — media files (photos, videos, documents)
- **LinkedDocument** → `foaf:Document` — linked web pages with metadata
- **Concept** → `skos:Concept` — hashtag topics
- **Reaction** → `tg:Reaction` — emoji reactions (schema-only, not yet populated)

`src/builder/models.py` is **auto-generated** from the schema via `just gen-model`. Do not edit it directly; modify `schemas/sioc.yaml` and regenerate.

### Key Ontology Prefixes

| Prefix       | Namespace                            |
|--------------|--------------------------------------|
| `sioc:`      | `http://rdfs.org/sioc/ns#`           |
| `sioc_types:`| `http://rdfs.org/sioc/types#`        |
| `dcterms:`   | `http://purl.org/dc/terms/`          |
| `dc:`        | `http://purl.org/dc/elements/1.1/`   |
| `foaf:`      | `http://xmlns.com/foaf/0.1/`         |
| `skos:`      | `http://www.w3.org/2004/02/skos/core#`|
| `tg:`        | `https://example.org/telegram/`      |

### Entity Extraction (Transform Stage)

The `builder.transform.entities` module extracts from raw Telegram messages: hashtags → `skos:Concept` topics, URLs → `LinkedDocument` objects (with webpage preview metadata), media → `Attachment` entities, reply/forward relationships, and pinned status.

### Key Modules

- **`config.py`** — paths, env vars, URI helpers (single source of truth)
- **`extract.py`** — Telegram API client (single session, ~20 req/min rate limit, crash-safe checkpointing)
- **`transform/`** — package with sub-modules for messages, users, channels, entities
- **`serialize.py`** — LinkML JSON → RDF/Turtle via rdflib
- **`load.py`** — Turtle → Oxigraph via HTTP POST (requires `just up`)

## Configuration

Requires a `.env` file (see `.env.example`):
- `TG_API_ID` / `TG_API_HASH` — Telegram API credentials
- `TG_SESSION` — Telethon session file name
- `TG_ENTITY` — target channel/group (invite link, @username, or numeric peer ID)

## Tech Stack

- **Python 3.13+**, managed with `uv`
- **LinkML** — schema definition + code generation
- **Oxigraph** — RDF triplestore (Docker container for persistence, pyoxigraph for in-memory demo)
- **Telethon** — Telegram client API
- **Pyright** — type checking (configured in `pyrightconfig.json`, source root: `src/`)

# CLAUDE INSTRUCTIONS:

## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately — don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff your behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management
1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## Core Principles
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
