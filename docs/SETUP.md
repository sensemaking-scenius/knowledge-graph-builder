# Quick Setup Guide

This guide will get you up and running with the Knowledge Graph Builder in minutes.

## 1. Prerequisites

Before you begin, install:

- **Python 3.13+** - Check with `python --version`
- **uv** - Python package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **just** - Command runner: `brew install just` (macOS) or see [installation guide](https://github.com/casey/just#installation)

## 2. Clone and Install

```bash
git clone <repository-url>
cd knowledge-graph-builder
uv sync
```

The `uv sync` command will:
- Create a virtual environment (`.venv/`)
- Install all dependencies from `pyproject.toml`

## 3. Configure Telegram Access

### Get API Credentials

1. Go to https://my.telegram.org
2. Log in with your phone number
3. Click "API development tools"
4. Create a new application
5. Copy your `api_id` and `api_hash`

### Create .env File

Create a `.env` file in the project root:

```env
TG_API_ID=your_api_id_here
TG_API_HASH=your_api_hash_here
TG_SESSION=tg.session
TG_ENTITY=@your_channel_username
```

**TG_ENTITY examples:**
- Public channel: `@channelname`
- Private channel by ID: `-1001234567890`
- Invite link: `https://t.me/+AbCdEfGhIjK`

### Authenticate

Run the extraction once to authenticate:

```bash
just extract 7
```

You'll be prompted to:
1. Enter your phone number (with country code, e.g., `+1234567890`)
2. Enter the verification code sent to Telegram

This creates a `tg.session` file that persists your login.

## 4. Run the Pipeline

### Build the Graph

```bash
just build
```

This will:
1. Transform raw messages into a LinkML graph document
2. Serialize the graph to RDF/Turtle
3. Load the Turtle into Oxigraph's on-disk store

Expected output:
```
Wrote 86 posts, 15 users, 33 links to data/graph/linkml_graph.json
Wrote RDF to data/rdf/sioc_graph.ttl
Loaded RDF into Oxigraph store
```

### View the Dashboard

```bash
just demo
```

This reads the Turtle file directly into an in-memory store and displays an 11-section rich dashboard — no server needed.

### Full Pipeline (Extract + Build)

```bash
just run-all
```

This runs extraction (last 30 days by default) followed by the full build.

## 5. Query the Graph

### Option 1: Built-in Dashboard (recommended)

```bash
just demo
```

No server needed. Shows community snapshot, top contributors, reply network, forum threads, media breakdown, and more.

### Option 2: SPARQL Endpoint

Start the Oxigraph server:

```bash
just serve
```

Then in another terminal:

```bash
just query
```

Or open `http://localhost:7878` in your browser for the SPARQL web interface.

## 6. Verify Everything Works

Check pipeline status:

```bash
just status
```

You should see files in:
- `data/raw/` — messages.jsonl, participants.jsonl, channel.json, topics.json
- `data/graph/` — linkml_graph.json
- `data/rdf/` — sioc_graph.ttl
- `data/store/` — Oxigraph database files

## Troubleshooting

### "Could not find the input entity"

- Check that `TG_ENTITY` is correct in `.env`
- For private channels, ensure your account has access
- Try using the numeric channel ID instead of username

### "Session file is corrupted"

Delete and re-authenticate:
```bash
rm tg.session
just extract 7
```

### Empty data files

Check each stage:
```bash
just status
ls -lah data/raw/
```

If extraction fails, verify your API credentials and network connection.

## Next Steps

- **Different time ranges**: `just extract 7` (week), `just extract 90` (quarter)
- **Full history**: `just extract-full` (incremental on re-runs)
- **Fresh re-fetch**: `just extract-fresh` (clears state first)
- **Add more channels**: Run pipeline with different `TG_ENTITY` values
- **Learn SPARQL**: Check the [SPARQL tutorial](https://www.w3.org/TR/sparql11-query/)
- **Explore the schema**: Review `schemas/sioc.yaml`

## Daily Usage

After initial setup, your typical workflow:

```bash
# Extract new messages and update graph
just run-all

# View the dashboard
just demo

# Or start SPARQL endpoint for custom queries
just serve
# (in another terminal)
open http://localhost:7878

# Clean old data before fresh run
just clean
just run-all
```

## Getting Help

- Check full documentation in `README.md`
- Pipeline details in `docs/PIPELINE.md`
- Graph inventory in `docs/GRAPH.md`
- Review justfile recipes: `just --list`
- Read LinkML schema in `schemas/sioc.yaml`
