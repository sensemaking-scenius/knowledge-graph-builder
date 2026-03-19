# Pipeline Guide

## How the stages connect

```
Telegram API
     │
     ▼
┌─────────┐   messages.jsonl
│ extract  │──────────────────┐
│          │   participants.  │
│          │───jsonl──────────┤
│          │   channel.json   │
│          │───topics.json────┤
└─────────┘                   │
                              ▼
                        ┌───────────┐   linkml_graph.json
                        │ transform │──────────────────────┐
                        └───────────┘                      │
                                                           ▼
                                                    ┌─────────────┐   sioc_graph.ttl
                                                    │  serialize  │────────────────┐
                                                    └─────────────┘                │
                                                           ┌───────────────────────┤
                                                           │                       │
                                                           ▼                       ▼
                                                    ┌────────────┐          ┌────────────┐
                                                    │    load    │          │    demo    │
                                                    │ (Oxigraph  │          │ (reads TTL │
                                                    │   store)   │          │  directly) │
                                                    └─────┬──────┘          └────────────┘
                                                          │
                                                          ▼
                                                    ┌────────────┐
                                                    │   serve    │
                                                    │ (SPARQL    │
                                                    │  endpoint) │
                                                    └────────────┘
```

## The stages

| Command | What it does | Input | Output |
|---------|-------------|-------|--------|
| `just extract` | Pulls messages + participants + channel metadata + forum topics from Telegram API | Telegram API | `data/raw/messages.jsonl`, `data/raw/participants.jsonl`, `data/raw/channel.json`, `data/raw/topics.json` |
| `just transform` | Converts raw JSON into a LinkML graph document | `data/raw/*.jsonl` + `data/raw/*.json` | `data/graph/linkml_graph.json` |
| `just serialize` | Converts LinkML JSON into RDF/Turtle | `data/graph/linkml_graph.json` | `data/rdf/sioc_graph.ttl` |
| `just load` | Imports the Turtle file into Oxigraph's on-disk store | `data/rdf/sioc_graph.ttl` | `data/store/` |
| `just serve` | Starts Oxigraph as a SPARQL HTTP server on `localhost:7878` | `data/store/` | — |
| `just demo` | Runs pre-built SPARQL queries and prints a rich dashboard | `data/rdf/sioc_graph.ttl` | terminal output |

## Extraction modes

| Command | Mode | Behavior |
|---------|------|----------|
| `just extract` | Date-bounded | Last 30 days (default). Overwrites `messages.jsonl` |
| `just extract 7` | Date-bounded | Last N days (positional arg). Overwrites `messages.jsonl` |
| `just extract-full` | Full history | First run: fetches everything. Subsequent runs: incremental (only new messages since last run) |
| `just extract-fresh` | Fresh full | Clears `extract_state.json`, then runs full history from scratch |

State is tracked in `data/raw/extract_state.json` — stores `newest_msg_id`, `oldest_msg_id`, `total_fetched`, and `complete` flag for incremental logic.

## Shortcut recipes

| Command | Equivalent to |
|---------|---------------|
| `just build` | `transform` → `serialize` → `load` |
| `just run-all` | `extract` → `build` |

## Two ways to query the data

There are two independent ways to run SPARQL against the data, and they don't share state:

### 1. `just demo` — standalone dashboard (no server needed)

Reads `data/rdf/sioc_graph.ttl` directly into an in-memory store and runs pre-built queries. No lock file, no server process. This is the fast path for the built-in dashboard.

**Use when:** you want to see the dashboard after a `just build`.

### 2. `just serve` + `just query` — SPARQL HTTP endpoint

`just load` writes the Turtle into Oxigraph's **on-disk store** (`data/store/`). `just serve` then opens that store and exposes it as a SPARQL endpoint at `localhost:7878`. `just query` sends an ad-hoc SPARQL query to the running server.

**Use when:** you want to run custom SPARQL queries interactively (via curl, a SPARQL GUI, or a notebook).

## The LOCK conflict

Oxigraph uses an exclusive file lock on `data/store/LOCK`. Only **one process** can open the store at a time. This means:

- `just load` and `just serve` **cannot run simultaneously**
- If the server is running, `just build` will fail at the load step

**Typical workflows:**

```bash
# Workflow A: rebuild + view dashboard (no server needed)
just build          # transform → serialize → load
just demo           # dashboard reads the TTL file directly, no conflict

# Workflow B: rebuild while server is running
# 1. Stop the server first (Ctrl-C the terminal running `just serve`)
# 2. Rebuild
just build
# 3. Restart
just serve

# Workflow C: full pipeline from scratch
just run-all        # extract → transform → serialize → load
just demo           # see the dashboard
just serve          # optionally start the SPARQL endpoint
```

## Data directory layout

```
data/
├── raw/                      # Stage: extract
│   ├── messages.jsonl        #   Raw Telegram messages
│   ├── participants.jsonl    #   User metadata (id, username, first_name)
│   ├── channel.json          #   Channel/supergroup metadata (title, about, member count)
│   ├── topics.json           #   Forum topic ID→name mapping
│   └── extract_state.json    #   Incremental extraction state (newest/oldest msg IDs)
├── graph/                    # Stage: transform
│   └── linkml_graph.json     #   LinkML graph document
├── rdf/                      # Stage: serialize
│   └── sioc_graph.ttl        #   RDF in Turtle format
└── store/                    # Stage: load
    ├── LOCK                  #   Oxigraph exclusive lock
    └── ...                   #   Oxigraph internal files
```

`just clean` removes all generated files but preserves the directory structure.
