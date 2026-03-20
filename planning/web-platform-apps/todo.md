# Web Platform — Todo

## Phase 1: Foundation
- [ ] Scaffold SvelteKit project in `web/` (TypeScript, node adapter)
- [ ] Install + configure shadcn-svelte
- [ ] Install deps: cytoscape, CodeMirror 6 packages
- [ ] Implement `sparql.ts` — typed HTTP client for Oxigraph SPARQL endpoint
- [ ] Implement `graph-service.ts` — getRecentPosts(), getRecentLinks(), getThreadGraph(), getLinkGraph(), getUserPostGraph(), runQuery()
- [ ] Write pre-built `.sparql` query files (top contributors, messages by topic, link frequency, etc.)

## Phase 2: Auth
- [ ] Create Telegram bot (if not already), get token
- [ ] Implement `/login` page with Telegram Login Widget
- [ ] Implement `/api/auth/callback` — hash verification + getChatMember check
- [ ] Implement encrypted session cookies in `auth.ts`
- [ ] Auth guard in `+layout.server.ts` — redirect unauthenticated to `/login`
- [ ] Header component with user info + logout

## Phase 3: Single-Page Layout + Graph Explorer
- [ ] Single-page layout in `+page.svelte` — hero graph + collapsible panels
- [ ] `graph-explorer.svelte` — Cytoscape.js init, force-directed layout, zoom/pan
- [ ] Conversation thread view — wire to getThreadGraph(), render posts + reply edges
- [ ] Node interaction — click to show message content in detail panel
- [ ] Filter controls — date range, forum/topic dropdowns
- [ ] (Stretch) View switching: threads / links / users

## Phase 4: Dashboard Panels
- [ ] `activity-feed.svelte` — collapsible panel, recent posts from getRecentPosts()
- [ ] `link-feed.svelte` — collapsible panel, shared URLs from getRecentLinks()
- [ ] Wire both into the single-page layout

## Phase 5: SPARQL Playground
- [ ] `query-editor.svelte` — CodeMirror 6 with SPARQL highlighting
- [ ] `query-library.svelte` — dropdown/sidebar of pre-built queries, click to load
- [ ] Run button -> runQuery() remote function -> results-table.svelte
- [ ] Save/load/delete custom queries in localStorage
- [ ] Collapsible panel integration

## Phase 6: Deploy
- [ ] Dockerfile for SvelteKit (node adapter, multi-stage build)
- [ ] Update `docker-compose.yml` — add web + nginx services
- [ ] Write `nginx.conf` — reverse proxy to SvelteKit, SSL termination
- [ ] Add `just` commands: web-dev, web-build, deploy
- [ ] Deploy to VPS — docker compose up, configure domain DNS + Let's Encrypt
- [ ] Set up cron for pipeline refresh (just run-all every 6h or similar)
- [ ] Smoke test: full auth flow, graph rendering, SPARQL queries, panel interactions

## Phase 7: CLI + MCP (post-MVP)
- [ ] Extract shared SPARQL client + types into `tools/shared/`
- [ ] CLI: scenius search, scenius sparql, scenius summarize
- [ ] MCP server: search_messages, get_thread, run_sparql, summarize_topic tools
- [ ] Package for distribution to community members

## Nice to Have (v0.1)
- [ ] Graph explorer: link sharing view
- [ ] Graph explorer: user-post network view
- [ ] Graph explorer: view switching UI
- [ ] Node click -> detail panel

## Later (v0.2+)
- [ ] Full-text search with filters
- [ ] Contributor stats / topic trends dashboard panels
- [ ] Telegram bot integration
- [ ] Semantic search (embeddings)
