# Telegram Community Knowledge Graph Builder

A Python pipeline for extracting Telegram messages and transforming them into a semantic knowledge graph using SIOC ontology and RDF.

## Overview

This project extracts messages from Telegram channels/groups, processes them through a multi-stage ETL pipeline, and loads them into an RDF graph database (Oxigraph) for semantic querying. The data model follows the [SIOC (Semantically-Interlinked Online Communities)](http://rdfs.org/sioc/spec/) ontology for representing social media content.

## Features

- **Telegram Message Extraction**: Fetch messages from Telegram channels/groups using the Telethon API
- **Data Canonicalization**: Normalize raw Telegram data into a consistent format
- **LinkML Schema**: Type-safe data modeling using LinkML with SIOC alignment
- **RDF Generation**: Transform data into semantic RDF triples (Turtle format)
- **Graph Database**: Load and query data using Oxigraph triplestore
- **Entity Extraction**: Parse hashtags, mentions, URLs, and reply relationships
- **Automated Pipeline**: Justfile recipes for running the entire ETL process

## Architecture

### Pipeline Stages

```
┌──────────────────┐
│  Telegram API    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  1. Extract      │  scripts/extract_last_7_days.py
│  Raw Messages    │  → data/raw/messages_last_7_days.jsonl
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  2. Canonicalize │  scripts/canonicalize_last_7_days.py
│  Message Data    │  → data/raw/canonical_last_7_days.jsonl
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  3. Transform to │  scripts/transform_to_linkml.py
│  LinkML Model    │  → data/raw/linkml_graph.json
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  4. Dump RDF     │  scripts/dump_rdf.py
│  (Turtle)        │  → data/rdf/sioc_graph.ttl
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  5. Load into    │  scripts/load_into_oxigraph.py
│  Oxigraph Store  │  → data/oxigraph/store/
└──────────────────┘
```

### Data Model

The schema (`schemas/sioc_min.yaml`) defines:

- **GraphDocument**: Root container for the knowledge graph
- **Community**: Telegram channel/group (mapped to `sioc:Community`)
- **UserAccount**: Telegram users (mapped to `sioc:UserAccount`)
- **Post**: Individual messages (mapped to `sioc:Post`)
- **Link**: URLs referenced in messages (mapped to `schema:URL`)

Key relationships:
- Posts have creators (users)
- Posts belong to communities
- Posts can reply to other posts
- Posts can link to URLs
- Posts can mention users and contain hashtag topics

## Prerequisites

- **Python 3.13+** (specified in `.python-version`)
- **uv** - Fast Python package manager ([installation](https://github.com/astral-sh/uv))
- **just** - Command runner ([installation](https://github.com/casey/just))
- **Telegram API credentials** (API ID and API Hash from [my.telegram.org](https://my.telegram.org))
- **(Optional) Oxigraph CLI** - For serving the graph database ([installation](https://github.com/oxigraph/oxigraph))

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd knowledge-graph-builder
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   TG_API_ID=your_api_id
   TG_API_HASH=your_api_hash
   TG_SESSION=tg.session
   TG_ENTITY=@channel_username_or_id
   ```

   - `TG_API_ID` and `TG_API_HASH`: Get from [my.telegram.org](https://my.telegram.org)
   - `TG_ENTITY`: Can be:
     - Channel username (e.g., `@channelname`)
     - Channel ID (e.g., `-1001234567890`)
     - Invite link

4. **Authenticate with Telegram** (first run only)
   ```bash
   uv run python scripts/extract_last_7_days.py
   ```
   You'll be prompted to enter your phone number and verification code.

## Usage

### Quick Start - Full Pipeline

Run the complete ETL pipeline:

```bash
just run-all
```

This executes all stages sequentially and reports success when complete.

### Individual Pipeline Stages

Run specific stages using `just` recipes:

```bash
# 1. Extract messages from Telegram (last 7 days)
just extract

# 2. Canonicalize raw data
just canonicalize

# 3. Transform to LinkML format
just transform

# 4. Generate RDF (Turtle format)
just dump-rdf

# 5. Load into Oxigraph
just load-oxigraph
```

### Query the Knowledge Graph

**Option 1: Python queries**
```bash
uv run python scripts/query_oxigraph.py
```

**Option 2: HTTP queries** (requires Oxigraph server)

Start the Oxigraph server:
```bash
just serve
# or manually:
oxigraph serve --location data/oxigraph/store --bind localhost:7878
```

Query via HTTP:
```bash
just query-http
# or manually:
curl -X POST http://localhost:7878/query \
  -H "Content-Type: application/sparql-query" \
  --data 'SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }'
```

### Check Pipeline Status

View the current state of data directories:
```bash
just status
```

## Project Structure

```
knowledge-graph-builder/
├── schemas/
│   └── sioc_min.yaml           # LinkML schema definition
├── src/
│   └── builder/
│       ├── __init__.py
│       └── sioc_model.py       # Generated Python classes from schema
├── scripts/
│   ├── extract_last_7_days.py  # Stage 1: Telegram extraction
│   ├── canonicalize_last_7_days.py  # Stage 2: Data normalization
│   ├── transform_to_linkml.py  # Stage 3: LinkML transformation
│   ├── dump_rdf.py             # Stage 4: RDF serialization
│   └── load_into_oxigraph.py   # Stage 5: Graph database loading
├── data/
│   ├── raw/                    # Intermediate JSON/JSONL files
│   ├── rdf/                    # RDF Turtle files
│   └── oxigraph/               # Oxigraph database files
├── justfile                    # Task automation recipes
├── pyproject.toml              # Python dependencies (uv)
├── .env                        # Environment variables (create this)
└── README.md
```

## Configuration

### Adjusting Time Range

By default, the pipeline extracts messages from the last 7 days. To change this, edit `scripts/extract_last_7_days.py`:

```python
since = datetime.now(timezone.utc) - timedelta(days=7)  # Change 7 to desired days
```

### Multiple Channels

The current implementation processes one channel per run. To process multiple channels:
1. Run the pipeline for each channel separately with different `TG_ENTITY` values
2. Modify the scripts to merge graphs or use separate graph documents

## Data Flow Details

### Stage 1: Extract (Raw)
- Connects to Telegram using Telethon
- Fetches messages from specified channel/group
- Outputs: `data/raw/messages_last_7_days.jsonl` (raw Telegram API format)

### Stage 2: Canonicalize
- Extracts key fields: chat_id, message_id, text, timestamps
- Parses URLs using regex
- Handles reply relationships
- Outputs: `data/raw/canonical_last_7_days.jsonl` (normalized format)

### Stage 3: Transform
- Builds LinkML-compliant object graph
- Creates Community, UserAccount, Post, and Link objects
- Extracts entities: hashtags → topics, mentions, URLs
- Outputs: `data/raw/linkml_graph.json` (typed JSON)

### Stage 4: Dump RDF
- Serializes LinkML objects to RDF triples
- Uses SIOC vocabulary for social data
- Outputs: `data/rdf/sioc_graph.ttl` (Turtle format)

### Stage 5: Load
- Ingests RDF into Oxigraph triplestore
- Enables SPARQL queries
- Outputs: `data/oxigraph/store/` (database files)

## Example SPARQL Queries

### Count all triples
```sparql
SELECT (COUNT(*) AS ?count) 
WHERE { ?s ?p ?o }
```

### List all posts with creators
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

### Find posts with hashtags
```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>

SELECT ?post ?content ?topic
WHERE {
  ?post a sioc:Post ;
        sioc:content ?content ;
        sioc:topic ?topic .
}
LIMIT 10
```

### Find reply threads
```sparql
PREFIX sioc: <http://rdfs.org/sioc/ns#>

SELECT ?post ?content ?replyTo
WHERE {
  ?post a sioc:Post ;
        sioc:content ?content ;
        sioc:reply_of ?replyTo .
}
LIMIT 10
```

## Dependencies

Core libraries (see `pyproject.toml`):
- **linkml** (1.9.6+): Schema definition and validation
- **linkml-runtime** (1.9.5+): Runtime support for LinkML models
- **pyoxigraph** (0.5.4+): Python bindings for Oxigraph RDF store
- **telethon** (1.42.0+): Telegram API client
- **python-dotenv** (1.2.1+): Environment variable management
- **rich** (14.3.1+): Terminal formatting

## Troubleshooting

### Authentication Issues
If you encounter "Could not find the input entity", ensure:
- Your API credentials are correct
- The `TG_ENTITY` value is valid
- For private channels, your account has access

### Session Expired
Delete `tg.session` and re-run to re-authenticate:
```bash
rm tg.session
uv run python scripts/extract_last_7_days.py
```

### Empty Data Files
Check pipeline status:
```bash
just status
```
Verify each stage produces output before proceeding to the next.

### RDF Serialization Errors
If you see issues with URL normalization or entity extraction, check:
- The canonical format has valid JSON
- URLs are properly prefixed with protocols
- Entity offsets are within text bounds

## Development

### Regenerate Python Model from Schema
After modifying `schemas/sioc_min.yaml`:
```bash
uv run gen-python schemas/sioc_min.yaml > src/builder/sioc_model.py
```

### Type Checking
```bash
uv run pyright
```

## Resources

- [SIOC Ontology Specification](http://rdfs.org/sioc/spec/)
- [LinkML Documentation](https://linkml.io/)
- [Oxigraph Documentation](https://github.com/oxigraph/oxigraph)
- [Telethon Documentation](https://docs.telethon.dev/)
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
