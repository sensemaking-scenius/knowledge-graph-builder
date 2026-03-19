# Pipeline Guide

## How the stages connect

```
Telegram API
     |
     v
+---------+   messages.jsonl
| extract |------------------+
|         |   participants.  |
|         |---jsonl----------+
|         |   channel.json   |
|         |---forums.json----+
+---------+                  |
                             v
                       +-----------+   linkml_graph.json
                       | transform |----------------------+
                       +-----------+                      |
                                                          v
                                                   +-------------+   sioc_graph.ttl
                                                   |  serialize  |----------------+
                                                   +-------------+                |
                                                          +------- --------------+
                                                          |                      |
                                                          v                      v
                                                   +------------+         +------------+
                                                   |    load    |         |    demo    |
                                                   | (HTTP POST |         | (reads TTL |
                                                   |  to Docker)|         |  directly) |
                                                   +-----+------+         +------------+
                                                         |
                                                         v
                                                   +------------+
                                                   |  Oxigraph  |
                                                   |  (Docker)  |
                                                   |  :7878     |
                                                   +------------+
```

## The stages

| Command | What it does | Input | Output |
|---------|-------------|-------|--------|
| `just extract` | Pulls messages + participants + channel metadata + forum structure from Telegram API | Telegram API | `data/raw/messages.jsonl`, `data/raw/participants.jsonl`, `data/raw/channel.json`, `data/raw/forums.json` |
| `just transform` | Converts raw JSON into a LinkML graph document with 13 entity types | `data/raw/*.jsonl` + `data/raw/*.json` | `data/graph/linkml_graph.json` |
| `just serialize` | Converts LinkML JSON into RDF/Turtle via rdflib | `data/graph/linkml_graph.json` | `data/rdf/sioc_graph.ttl` |
| `just load` | POSTs the Turtle file to the Dockerized Oxigraph server | `data/rdf/sioc_graph.ttl` | Oxigraph store (Docker volume) |
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

There are two independent ways to run SPARQL against the data:

### 1. `just demo` — standalone dashboard (no server needed)

Reads `data/rdf/sioc_graph.ttl` directly into an in-memory pyoxigraph store and runs pre-built queries. No Docker required. This is the fast path for the built-in dashboard.

**Use when:** you want to see the dashboard after a `just build`.

### 2. `just up` + `just query` — Dockerized SPARQL endpoint

`just up` starts an Oxigraph Docker container at `localhost:7878`. `just load` POSTs the Turtle file to the running server. `just query` sends an ad-hoc SPARQL query to the endpoint.

**Use when:** you want to run custom SPARQL queries interactively (via curl, a SPARQL GUI, or a notebook).

The Oxigraph web UI is available at `http://localhost:7878` for interactive SPARQL queries.

## Data directory layout

```
data/
├── raw/                      # Stage: extract
│   ├── messages.jsonl        #   Raw Telegram messages
│   ├── participants.jsonl    #   User metadata (id, username, first_name)
│   ├── channel.json          #   Channel/supergroup metadata (title, about)
│   ├── forums.json           #   Forum topic structure (id, title, closed)
│   └── extract_state.json    #   Incremental extraction state (newest/oldest msg IDs)
├── graph/                    # Stage: transform
│   └── linkml_graph.json     #   LinkML graph document (all 13 entity types)
├── rdf/                      # Stage: serialize
│   └── sioc_graph.ttl        #   RDF in Turtle format
└── store/                    # Oxigraph (Docker volume mount)
```

`just clean` removes all generated files but preserves the directory structure.
