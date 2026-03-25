# Self-Hosting Plan: Knowledge Graph Explorer

## Goal

Host the Oxigraph triplestore and SvelteKit web app on a Windows laptop, exposed to the internet via Cloudflare Tunnel, with Caddy as a reverse proxy. All services orchestrated with Docker Compose.

## Architecture

```
Internet
  │
  ▼
Cloudflare Tunnel (cloudflared)
  │
  ▼
Caddy (reverse proxy, port 80/443 inside container)
  ├── /         → SvelteKit app (port 3000)
  └── /sparql   → Oxigraph (port 7878)
  │
  ▼  (all in Docker Compose on Windows laptop)
┌─────────────────────────────────────────┐
│  docker-compose.prod.yml                │
│                                         │
│  ┌───────────┐  ┌──────────┐            │
│  │ oxigraph  │  │ sveltekit│            │
│  │ :7878     │  │ :3000    │            │
│  └───────────┘  └──────────┘            │
│  ┌───────────┐  ┌──────────────┐        │
│  │   caddy   │  │ cloudflared  │        │
│  │ :80/:443  │  │ (tunnel)     │        │
│  └───────────┘  └──────────────┘        │
└─────────────────────────────────────────┘
```

## Key Decisions

### Why Docker Compose for everything?
- Single `docker compose up -d` starts the entire stack
- Works identically on Windows (via Docker Desktop) and Linux
- No need to install Node.js, pnpm, or Caddy natively on Windows
- Easy to tear down, rebuild, and version control

### Why Caddy?
- Automatic HTTPS (via Cloudflare DNS challenge or tunnel)
- Simple config (Caddyfile is ~10 lines)
- Built-in reverse proxy with health checks

### Why Cloudflare Tunnel?
- No port forwarding on the router
- No exposing home IP
- Free tier is sufficient
- Automatic HTTPS termination at Cloudflare edge
- Stable subdomain on your own domain (or `*.trycloudflare.com` for quick testing)

### SvelteKit adapter-node
- Already configured (`@sveltejs/adapter-node`)
- Produces a standalone Node.js server
- We'll build a Docker image for it with a multi-stage Dockerfile

## Components to Create

### 1. `web/Dockerfile`
Multi-stage build:
- Stage 1: `node:22-alpine` — install deps with pnpm, build the app
- Stage 2: `node:22-alpine` — copy only the built output, run with `node build`

### 2. `docker-compose.prod.yml` (project root)
Services:
- **oxigraph** — same as existing, but on internal network only (no host port binding needed)
- **sveltekit** — built from `web/Dockerfile`, connects to oxigraph on internal Docker network
- **caddy** — official Caddy image, mounts `Caddyfile`, exposes ports 80/443
- **cloudflared** — official `cloudflare/cloudflared` image, runs the tunnel

### 3. `Caddyfile` (project root)
- Route `/sparql*` → `oxigraph:7878`
- Route `/*` → `sveltekit:3000`
- Since Cloudflare Tunnel handles TLS termination, Caddy listens on `:80` internally

### 4. SvelteKit env configuration
- The app currently makes SPARQL queries to Oxigraph — in production, it needs to target `http://oxigraph:7878` (Docker internal DNS) for server-side queries
- Client-side queries need to go through the Caddy proxy at `/sparql`
- May need a `PUBLIC_SPARQL_ENDPOINT` or similar env var

## Cloudflare Tunnel Setup (manual, documented steps)

1. Create a Cloudflare account (free)
2. Add a domain (or use `trycloudflare.com` for testing)
3. Install `cloudflared` or use the Docker image
4. `cloudflared tunnel login` — authenticates with Cloudflare
5. `cloudflared tunnel create kg-explorer` — creates the tunnel
6. Configure tunnel to point at `http://caddy:80`
7. Create DNS CNAME record pointing to the tunnel
8. Credentials file gets mounted into the Docker container

## Windows-Specific Considerations

- **Docker Desktop for Windows** — required, uses WSL2 backend
- **File paths** — Docker volumes use Linux paths inside containers; Windows paths for host mounts need forward slashes or WSL paths
- **Sleep prevention** — configure Windows power settings to prevent sleep when plugged in (Settings > Power & Sleep > Never)
- **Startup** — Docker Desktop can be set to start on Windows login; containers with `restart: unless-stopped` will auto-start
- **Firewall** — no inbound ports needed (Cloudflare Tunnel is outbound-only)

## Network Flow

1. User visits `https://kg.yourdomain.com`
2. Cloudflare routes through the tunnel to `cloudflared` container
3. `cloudflared` forwards to `caddy:80`
4. Caddy routes:
   - `/sparql` → `oxigraph:7878/sparql` (SPARQL endpoint)
   - Everything else → `sveltekit:3000`
5. SvelteKit SSR makes server-side SPARQL queries directly to `oxigraph:7878`
6. Client-side JS makes SPARQL queries to `/sparql` (relative URL → Caddy → Oxigraph)
