# Telegram Community Knowledge Graph Builder — Explained

## What This Is

This project turns a Telegram community's chat history into a **structured knowledge graph** — a queryable map of who said what, to whom, about which topics, linking to what resources.

Instead of chat messages disappearing into an endless scroll, the pipeline extracts them and organizes them into a web of connected entities: **people**, **messages**, **topics** (hashtags), **shared links**, **media**, **reply threads**, and **forum channels** — all with their relationships preserved.

## Why It Matters (The Problem It Solves)

Group chats are rich with knowledge but terrible at preserving it. Think about how much valuable information lives in your Telegram group right now:

- **Someone shared a great article** three months ago — good luck finding it
- **A nuanced discussion** happened across 40 replies — it's buried under thousands of messages
- **Who are the most active contributors** on a given topic? No way to tell at a glance
- **What links keep getting shared?** What topics dominate? How do conversations connect across threads?

A knowledge graph makes all of this **queryable**. Instead of scrolling, you ask structured questions:

- "Show me every link shared in the last month, ranked by how many people shared it"
- "Who replies to whom the most?" (reveals the actual social network)
- "What topics has person X contributed to?"
- "Show me the full reply tree of this conversation"

## How It Works (Simple Version)

Four steps, fully automated:

1. **Extract** — Pull messages, users, forums, and metadata from the Telegram API
2. **Transform** — Structure everything into a formal data model (people, posts, topics, links, and the relationships between them)
3. **Serialize** — Convert to RDF, the web standard for linked data
4. **Load** — Store in a graph database that understands SPARQL (a query language for graphs)

The data model follows **SIOC** (Semantically-Interlinked Online Communities), an established ontology specifically designed for representing online community data. This means the graph speaks a shared vocabulary — it's not a proprietary format locked to Telegram.

## What You Can Do With It Today

- **Visual graph explorer** — a web app (in progress) where you can see conversation threads, link networks, and user interaction patterns as interactive node-and-edge graphs
- **SPARQL playground** — write and run queries against the live data, with a library of pre-built queries
- **Activity and link feeds** — see recent posts and shared URLs at a glance
- **CLI dashboard** — a rich terminal view showing community stats, top contributors, topic distribution, reply networks, and more

## Where It Can Go From Here

**For the community:**
- **Search that actually works** — find past conversations, resources, and contributors by topic, date, person, or content
- **Collective memory** — the group's knowledge becomes durable and navigable, not ephemeral
- **Onboarding** — new members can explore what the community has discussed, who knows what, and where the key resources live

**For builders and agents:**
- **CLI tools** — `scenius search`, `scenius sparql` for terminal-based community exploration
- **MCP server** — an API that lets AI agents search messages, retrieve threads, run queries, and summarize topics from the graph (planned)
- **Semantic search** — add embeddings for natural-language queries ("what has the group said about X?")
- **Cross-platform** — the SIOC ontology isn't Telegram-specific. The same model could ingest Discord, forums, or any online community

**The key insight:** by giving community knowledge a structure and a standard vocabulary, you make it composable. Other tools, dashboards, bots, and agents can all build on the same foundation without re-extracting or re-interpreting raw chat logs.
