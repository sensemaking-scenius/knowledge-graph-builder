# Scenius Knowledge Graph — Web Platform Plan

## Vision

A community knowledge platform for Scenius Telegram members. Four roles: searchable archive, knowledge/insight tool, agent substrate (MCP/CLI), and social mirror. Auth-gated to group members via Telegram Login Widget.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Serving stack | TypeScript / SvelteKit | Unified language for web, CLI, MCP; remote functions as API |
| UI framework | shadcn-svelte | Consistent, accessible component library |
| Python role | ETL pipeline only | Pipeline writes Turtle to Oxigraph; serving layer talks HTTP SPARQL |
| Repo layout | Monorepo `web/` subfolder | One repo, pipeline + web app together |
| Hosting | VPS + Docker + nginx + SSL | Domain and VPS already available |
| Auth | Telegram Login Widget + Bot API membership check | Only verified Scenius members get access |
| Session | Encrypted cookies | Stateless, no extra infrastructure |
| Bot strategy | Single bot for auth + future chat | Simple; split later if needed |
| Data layer | SPARQL abstraction + raw escape hatch | Named methods for common ops, raw SPARQL for power users/agents |
| SPARQL editor | CodeMirror 6 | Rich editing with SPARQL syntax highlighting |
| Graph viz | Cytoscape.js, force-directed | Multiple views: conversation threads, link sharing, user-post network |
| CLI/MCP scope | Search/query + summarization (read-only) | For community members + in-channel bots |
| Rate limiting | None | Trusted community, small dataset |
| Pipeline refresh | Scheduled cron | Auto-run ETL on a schedule to keep graph current |

## Architecture

### Page Layout (Single Page)

```
┌─────────────────────────────────────────────────────────┐
│  Header: Scenius Knowledge Graph    [user] [logout]     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │                                                   │  │
│  │           Graph Explorer (Cytoscape.js)           │  │
│  │              Main content area                    │  │
│  │         [view: threads | links | users]           │  │
│  │         [filters: date, forum, topic]             │  │
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ Activity ──────────────────┐ ┌─ Links ───────────┐  │
│  │  ▼ collapsible              │ │  ▼ collapsible     │  │
│  │  Recent posts feed          │ │  Shared URLs feed  │  │
│  │  (author, time, preview)    │ │  (title, source)   │  │
│  └─────────────────────────────┘ └────────────────────┘  │
│                                                         │
│  ┌─ SPARQL Playground ──────────────────────────────┐   │
│  │  ▼ collapsible                                    │   │
│  │  [Query Library ▼]  [Run] [Save]                  │   │
│  │  ┌──────────────────────────────────────────────┐ │   │
│  │  │  CodeMirror 6 editor                         │ │   │
│  │  └──────────────────────────────────────────────┘ │   │
│  │  Results table                                    │   │
│  └───────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

All content on a single page (`/`). Graph explorer is the hero. Activity feed, link feed, and SPARQL playground are collapsible panels below. Login page (`/login`) is the only separate route.

### File Structure

```
knowledge-graph-builder/
├── src/builder/              # Python ETL pipeline (existing)
├── schemas/                  # LinkML schema (existing)
├── data/                     # Pipeline data (existing)
├── web/                      # SvelteKit app (NEW)
│   ├── src/
│   │   ├── lib/
│   │   │   ├── server/
│   │   │   │   ├── sparql.ts         # Oxigraph HTTP client
│   │   │   │   ├── graph-service.ts  # Abstraction layer
│   │   │   │   ├── auth.ts           # Telegram auth verification + session
│   │   │   │   └── queries/          # Pre-built .sparql files
│   │   │   ├── components/
│   │   │   │   ├── graph-explorer.svelte   # Cytoscape.js wrapper + controls
│   │   │   │   ├── activity-feed.svelte    # Collapsible recent posts
│   │   │   │   ├── link-feed.svelte        # Collapsible shared links
│   │   │   │   ├── query-editor.svelte     # CodeMirror 6 + run/save
│   │   │   │   ├── query-library.svelte    # Pre-built query selector
│   │   │   │   ├── results-table.svelte    # SPARQL results display
│   │   │   │   └── node-detail.svelte      # Graph node click panel
│   │   │   ├── types.ts              # Shared types
│   │   │   └── stores.ts             # Svelte stores (saved queries, filters)
│   │   ├── routes/
│   │   │   ├── +layout.server.ts     # Auth guard
│   │   │   ├── +layout.svelte        # Header + auth state
│   │   │   ├── +page.svelte          # Single page: graph + panels
│   │   │   ├── +page.server.ts       # Load initial data
│   │   │   ├── login/
│   │   │   │   └── +page.svelte      # Telegram Login Widget
│   │   │   └── api/
│   │   │       └── auth/
│   │   │           └── callback/+server.ts
│   │   └── app.html
│   ├── static/
│   ├── package.json
│   ├── svelte.config.js
│   ├── tsconfig.json
│   └── Dockerfile
├── tools/                    # CLI + MCP (NEW, post-MVP)
│   ├── cli/
│   │   ├── index.ts
│   │   └── commands/
│   ├── mcp/
│   │   ├── index.ts
│   │   └── tools/
│   ├── shared/
│   │   ├── sparql.ts
│   │   └── types.ts
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml        # Updated: oxigraph + web + nginx
├── justfile                  # Updated: web dev/build/deploy commands
└── .env                      # Updated: TG_BOT_TOKEN, TG_CHAT_ID, domain, etc.
```

### Data Flow

```
[Browser] ──Telegram Login──▶ [SvelteKit Server]
                                  │
                    ┌─────────────┼──────────────┐
                    ▼             ▼               ▼
              remote funcs   SPARQL proxy    static assets
              (typed API)    (raw queries)
                    │             │
                    ▼             ▼
              ┌───────────────────────┐
              │   graph-service.ts    │
              │   (abstraction layer) │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │   sparql.ts           │
              │   (HTTP POST to       │
              │    Oxigraph :7878)    │
              └───────────────────────┘

[CLI / MCP] ──────▶ [shared/sparql.ts] ──────▶ [Oxigraph :7878]
  (local)              (direct, no auth)          (local or remote)
```

### Auth Flow

1. User visits `/` → `+layout.server.ts` checks session cookie → redirects to `/login`
2. `/login` renders Telegram Login Widget
3. Widget calls back with user data + hash → POST to `/api/auth/callback`
4. Server verifies hash (HMAC-SHA-256 with bot token)
5. Server calls Bot API `getChatMember(chat_id, user_id)` → verify Scenius membership
6. On success → set encrypted session cookie with user data
7. Redirect to `/` → layout loads, page renders with graph + panels

### Deployment (Docker Compose)

```yaml
services:
  oxigraph:
    image: ghcr.io/oxigraph/oxigraph
    volumes: [./data/store:/data]
    ports: ["7878:7878"]

  web:
    build: ./web
    environment:
      - OXIGRAPH_URL=http://oxigraph:7878
      - TG_BOT_TOKEN=${TG_BOT_TOKEN}
      - TG_CHAT_ID=${TG_CHAT_ID}
      - SESSION_SECRET=${SESSION_SECRET}
    ports: ["3000:3000"]
    depends_on: [oxigraph]

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/letsencrypt:ro
    ports: ["80:80", "443:443"]
    depends_on: [web]
```

Pipeline refresh via cron on the VPS (e.g. `crontab -e` → `0 */6 * * * cd /path && just run-all`).

## MVP Scope (v0.1)

### Must Have
- [ ] SvelteKit project scaffold with shadcn-svelte
- [ ] Telegram auth (login widget + membership check + encrypted session)
- [ ] SPARQL client (`sparql.ts`) + abstraction layer (`graph-service.ts`)
- [ ] Single-page layout: header + graph explorer + collapsible panels
- [ ] Graph explorer: Cytoscape.js with conversation thread view
- [ ] Activity feed panel: recent posts with author, timestamp, content, forum context
- [ ] Link feed panel: recently shared URLs with preview metadata
- [ ] SPARQL playground panel: CodeMirror 6 editor + query execution + results table
- [ ] Query library: pre-built queries loadable into editor
- [ ] Query save/load to localStorage
- [ ] Docker Compose deployment (Oxigraph + SvelteKit + nginx)
- [ ] SSL + domain setup
- [ ] Cron job for pipeline refresh

### Nice to Have (v0.1)
- [ ] Graph explorer: link sharing view
- [ ] Graph explorer: user-post network view
- [ ] Graph explorer: view switching UI
- [ ] Node click → detail panel

### Later (v0.2+)
- [ ] Full-text search with filters
- [ ] Contributor stats / topic trends dashboard panels
- [ ] CLI tool (search, query, summarize)
- [ ] MCP server (same tools)
- [ ] Telegram bot integration
- [ ] Semantic search (embeddings)

## Build Plan

### Phase 1: Foundation
1. Scaffold SvelteKit project in `web/` (TypeScript, node adapter)
2. Install + configure shadcn-svelte
3. Install deps: `cytoscape`, `@codemirror/lang-sql` (SPARQL mode), `@codemirror/view`
4. Implement `sparql.ts` — typed HTTP client for Oxigraph SPARQL endpoint
5. Implement `graph-service.ts` — `getRecentPosts()`, `getRecentLinks()`, `getThreadGraph()`, `getLinkGraph()`, `getUserPostGraph()`, `runQuery(sparql)`
6. Write pre-built `.sparql` query files (top contributors, messages by topic, link frequency, etc.)

### Phase 2: Auth
7. Create Telegram bot (if not already), get token
8. Implement `/login` page with Telegram Login Widget
9. Implement `/api/auth/callback` — hash verification + `getChatMember` check
10. Implement encrypted session cookies in `auth.ts`
11. Auth guard in `+layout.server.ts` — redirect unauthenticated to `/login`
12. Header component with user info + logout

### Phase 3: Single-Page Layout + Graph Explorer
13. Single-page layout in `+page.svelte` — hero graph + collapsible panels
14. `graph-explorer.svelte` — Cytoscape.js init, force-directed layout, zoom/pan
15. Conversation thread view — wire to `getThreadGraph()`, render posts + reply edges
16. Node interaction — click to show message content in detail panel
17. Filter controls — date range, forum/topic dropdowns
18. (Stretch) View switching: threads / links / users

### Phase 4: Dashboard Panels
19. `activity-feed.svelte` — collapsible panel, recent posts from `getRecentPosts()`
20. `link-feed.svelte` — collapsible panel, shared URLs from `getRecentLinks()`
21. Wire both into the single-page layout

### Phase 5: SPARQL Playground
22. `query-editor.svelte` — CodeMirror 6 with SPARQL highlighting
23. `query-library.svelte` — dropdown/sidebar of pre-built queries, click to load
24. Run button → `runQuery()` remote function → `results-table.svelte`
25. Save/load/delete custom queries in localStorage
26. Collapsible panel integration

### Phase 6: Deploy
27. Dockerfile for SvelteKit (node adapter, multi-stage build)
28. Update `docker-compose.yml` — add web + nginx services
29. Write `nginx.conf` — reverse proxy to SvelteKit, SSL termination
30. Add `just` commands: `just web-dev`, `just web-build`, `just deploy`
31. Deploy to VPS — docker compose up, configure domain DNS + Let's Encrypt
32. Set up cron for pipeline refresh (`just run-all` every 6h or similar)
33. Smoke test: full auth flow, graph rendering, SPARQL queries, panel interactions

### Phase 7: CLI + MCP (post-MVP)
34. Extract shared SPARQL client + types into `tools/shared/`
35. CLI: `scenius search <query>`, `scenius sparql <file-or-inline>`, `scenius summarize <topic>`
36. MCP server: `search_messages`, `get_thread`, `run_sparql`, `summarize_topic` tools
37. Package for distribution to community members
