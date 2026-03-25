# Self-Hosting TODO

## Phase 1: Dockerize the SvelteKit App

- [ ] Create `web/Dockerfile` (multi-stage: pnpm install + build → production image with `node build`)
- [ ] Create `web/.dockerignore` (exclude node_modules, .svelte-kit, etc.)
- [ ] Verify the SvelteKit app builds and runs inside Docker locally
- [ ] Configure SPARQL endpoint env vars:
  - `ORIGIN` — required by adapter-node for CSRF protection
  - Server-side: `SPARQL_ENDPOINT` env var → `http://oxigraph:7878` in Docker network
  - Client-side: relative `/sparql` path (proxied by Caddy)
- [ ] Ensure the app's SPARQL queries use the correct endpoint for SSR vs client

## Phase 2: Production Docker Compose

- [ ] Create `docker-compose.prod.yml` with all 4 services:
  - [ ] `oxigraph` — Oxigraph image, internal network only, persistent volume
  - [ ] `sveltekit` — built from `web/Dockerfile`, depends on oxigraph
  - [ ] `caddy` — official image, mounts Caddyfile, exposes port 80
  - [ ] `cloudflared` — tunnel container (added in Phase 4)
- [ ] Create `Caddyfile` with reverse proxy routes:
  - [ ] `/sparql*` → `oxigraph:7878`
  - [ ] `/*` → `sveltekit:3000`
- [ ] Create shared Docker network for inter-service communication
- [ ] Test full stack locally: `docker compose -f docker-compose.prod.yml up --build`
- [ ] Verify: web app loads at `http://localhost`, SPARQL queries work through `/sparql`

## Phase 3: Load Data into Oxigraph

- [ ] Ensure the Oxigraph persistent volume is correctly mapped
- [ ] Document how to load the Turtle file into the production Oxigraph:
  - Option A: mount `data/rdf/` into the container and POST on startup
  - Option B: run `just load` pointing at the Docker Oxigraph endpoint
  - Option C: copy the `data/store/` directory from dev into the prod volume
- [ ] Verify SPARQL queries return data through the full Caddy → Oxigraph chain

## Phase 4: Cloudflare Tunnel Setup

- [ ] Create a Cloudflare account (if not already)
- [ ] Register/add a domain to Cloudflare (or plan to use `trycloudflare.com` for testing)
- [ ] Install `cloudflared` on the Windows laptop (or use Docker image)
- [ ] Authenticate: `cloudflared tunnel login`
- [ ] Create tunnel: `cloudflared tunnel create kg-explorer`
- [ ] Create tunnel config file (`cloudflared/config.yml`):
  ```yaml
  tunnel: <TUNNEL_ID>
  credentials-file: /etc/cloudflared/<TUNNEL_ID>.json
  ingress:
    - service: http://caddy:80
  ```
- [ ] Add `cloudflared` service to `docker-compose.prod.yml`:
  - Mount credentials file and config
  - Connect to same Docker network as Caddy
  - `restart: unless-stopped`
- [ ] Create DNS CNAME record: `kg.yourdomain.com` → `<TUNNEL_ID>.cfargotunnel.com`
- [ ] Test: visit `https://kg.yourdomain.com` from an external device

## Phase 5: Windows Laptop Setup

- [ ] Install Docker Desktop for Windows (WSL2 backend)
- [ ] Clone the repo onto the laptop
- [ ] Copy required data files:
  - `data/store/` (Oxigraph database) OR `data/rdf/sioc_graph.ttl` (to reload)
  - Cloudflare tunnel credentials
- [ ] Copy `.env` file with any required environment variables
- [ ] Configure Docker Desktop to start on login
- [ ] Configure Windows power settings: never sleep when plugged in
- [ ] Run `docker compose -f docker-compose.prod.yml up -d --build`
- [ ] Verify everything works end-to-end from an external network

## Phase 6: Quick-Test Alternative (optional, for validating before domain setup)

- [ ] Use `cloudflared tunnel --url http://localhost:80` for a temporary public URL
- [ ] Verify the app and SPARQL endpoint are accessible
- [ ] Use this to validate before committing to a domain/DNS setup

---

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `web/Dockerfile` | Create | Multi-stage Node build for SvelteKit |
| `web/.dockerignore` | Create | Exclude dev artifacts from Docker context |
| `docker-compose.prod.yml` | Create | Full production stack (4 services) |
| `Caddyfile` | Create | Reverse proxy routing rules |
| `cloudflared/config.yml` | Create | Tunnel configuration (template) |
| `web/src/lib/server/sparql.ts` (or similar) | Modify | Use env var for SPARQL endpoint |
| `.env.example` | Modify | Add production env vars |

## Review Checklist (before deploying)

- [ ] SvelteKit builds successfully in Docker
- [ ] Oxigraph data persists across container restarts
- [ ] SPARQL works through Caddy proxy (both SSR and client-side)
- [ ] Cloudflare Tunnel connects and routes traffic
- [ ] Site accessible from external network via HTTPS
- [ ] Containers restart automatically after Docker Desktop restart
- [ ] Windows laptop stays awake when lid is closed (if applicable)
