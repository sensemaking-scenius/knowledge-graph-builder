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
- Supergroup with -100 prefix: `-1001234567890`

### Authenticate

Run the extraction script once to authenticate:

```bash
just extract
```

You'll be prompted to:
1. Enter your phone number (with country code, e.g., `+1234567890`)
2. Enter the verification code sent to Telegram

This creates a `tg.session` file that persists your login.

## 4. Run the Pipeline

### First Time Setup

Initialize data directories (happens automatically, but can be done manually):

```bash
just init
```

### Run Full Pipeline

Process messages and build the knowledge graph:

```bash
just run-all
```

This will:
1. Extract messages from Telegram (last 7 days)
2. Canonicalize the data
3. Transform to LinkML format
4. Generate RDF triples
5. Load into Oxigraph database

Expected output:
```
Read 150 lines, wrote 150 canonical messages to data/raw/canonical_last_7_days.jsonl
Wrote 150 posts, 45 users, 89 links to data/raw/linkml_graph.json
Wrote RDF to data/rdf/sioc_graph.ttl
Loaded RDF into Oxigraph store
Triple count: 2847
OK: pipeline complete. Run 'just serve' in another terminal, then 'just query-http'.
```

## 5. Query the Graph

### Start Oxigraph Server

In a separate terminal:

```bash
just serve
```

Keep this running while querying.

### Run Test Query

In another terminal:

```bash
just query-http
```

This counts all triples in the graph.

### Access Web UI

Open in your browser:
```
http://localhost:7878
```

Try this SPARQL query in the web interface:

```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>

SELECT ?post ?content ?creator
WHERE {
  ?post a sioc:Post ;
        sioc:content ?content ;
        sioc:has_creator ?creator .
}
LIMIT 10
```

## 6. Verify Everything Works

Check pipeline status:

```bash
just status
```

You should see files in:
- `data/raw/` - Intermediate JSON files
- `data/rdf/` - RDF Turtle files
- `data/oxigraph/store/` - Database files

## Troubleshooting

### "Could not find the input entity"

- Check that `TG_ENTITY` is correct in `.env`
- For private channels, ensure your account has access
- Try using the numeric channel ID instead of username

### "Session file is corrupted"

Delete and re-authenticate:
```bash
rm tg.session
just extract
```

### Empty data files

Check each stage:
```bash
just status
ls -lah data/raw/
```

If extraction fails, verify your API credentials and network connection.

### Permission denied on scripts

Make scripts executable:
```bash
chmod +x scripts/*.py
```

## Next Steps

- **Customize time range**: Edit `scripts/extract_last_7_days.py` and change `timedelta(days=7)`
- **Add more channels**: Run pipeline with different `TG_ENTITY` values
- **Learn SPARQL**: Check the [SPARQL tutorial](https://www.w3.org/TR/sparql11-query/)
- **Explore the schema**: Review `schemas/sioc_min.yaml`

## Daily Usage

After initial setup, your typical workflow:

```bash
# Extract new messages and update graph
just run-all

# Start server and explore
just serve
# (in another terminal)
open http://localhost:7878

# Clean old data before fresh run
just clean
just run-all
```

## Getting Help

- Check full documentation in `README.md`
- Review justfile recipes: `just --list`
- Examine script code in `scripts/` directory
- Read LinkML schema in `schemas/sioc_min.yaml`
