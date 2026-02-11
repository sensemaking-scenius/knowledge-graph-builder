# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Telegram Community Knowledge Graph Builder — a Python ETL pipeline that extracts messages from Telegram channels/groups, transforms them via a LinkML schema aligned with the SIOC ontology, and loads the resulting RDF into an Oxigraph triplestore for SPARQL querying.

## Commands

All commands use `just` (task runner) and `uv` (Python package manager).

```bash
# Full pipeline (canonicalize → transform → dump-rdf → load-oxigraph)
just run-all

# Individual pipeline stages (each depends on prior stages)
just extract          # Telegram API → data/raw/messages_last_7_days.jsonl
just canonicalize     # Normalize → data/raw/canonical_last_7_days.jsonl
just transform        # LinkML objects → data/raw/linkml_graph.json
just dump-rdf         # RDF/Turtle → data/rdf/sioc_graph.ttl
just load-oxigraph    # Ingest into Oxigraph store

# Run a single script directly
uv run python scripts/<script_name>.py

# Serve Oxigraph for SPARQL queries
just serve            # localhost:7878
just query-http       # Test SPARQL count query against running server
just query-python     # Query via pyoxigraph Python API

# Type checking
uv run pyright

# Clean generated data (preserves directory structure)
just clean
```

## Architecture

### 5-Stage Pipeline

```
Telegram API → Extract → Canonicalize → Transform → Dump RDF → Load Oxigraph
                 ↓            ↓             ↓            ↓           ↓
              .jsonl       .jsonl      linkml_graph   .ttl      oxigraph/store
             (raw msgs)  (normalized)    .json      (Turtle)    (triplestore)
```

Each stage is a standalone script in `scripts/` that reads from the previous stage's output in `data/`.

### Schema-Driven Data Model

The schema lives in `schemas/sioc_min.yaml` (LinkML format, SIOC ontology-aligned). It defines five classes:

- **GraphDocument** — root container (tree_root)
- **Community** → `sioc:Community` — the Telegram channel/group
- **UserAccount** → `sioc:UserAccount` — message authors
- **Post** → `sioc:Post` — individual messages (with replies, topics, mentions, links)
- **Link** → `schema:URL` — extracted URLs

`src/builder/sioc_model.py` is **auto-generated** from the schema via `linkml gen-python`. Do not edit it directly; modify `schemas/sioc_min.yaml` and regenerate.

### Key Ontology Prefixes

| Prefix   | Namespace                            |
|----------|--------------------------------------|
| `sioc:`  | `http://rdfs.org/sioc/ns#`           |
| `dcterms:` | `http://purl.org/dc/terms/`        |
| `schema:` | `http://schema.org/`                |
| `tg:`    | `https://example.org/telegram/`      |

### Entity Extraction (Canonicalize Stage)

The canonicalize step extracts from raw Telegram messages: hashtags → topics, @mentions, URLs (via regex + Telegram entities), reply relationships, forward counts, and pinned status.

## Configuration

Requires a `.env` file (see `.env.example`):
- `TG_API_ID` / `TG_API_HASH` — Telegram API credentials
- `TG_SESSION` — Telethon session file name
- `TG_ENTITY` — target channel/group (invite link, @username, or numeric peer ID)

## Tech Stack

- **Python 3.13+**, managed with `uv`
- **LinkML** — schema definition + code generation
- **pyoxigraph** — embedded RDF triplestore
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
