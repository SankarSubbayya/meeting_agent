# AWS ship to prod hackathon — meeting agents

Backend service for **meeting → agent actions**: Fireflies GraphQL API for transcripts, Guild.ai workflow trigger, Redis caching/idempotency, Gmail/Drive, WhatsApp (policy + opt-in), TinyFish fallback.

## Quick start

1. Start Redis: `docker compose up -d`  
2. Follow [backend/README.md](backend/README.md) to run the API.

## Docs

- [docs/API_KEYS.md](docs/API_KEYS.md) — environment variables and secrets  
- [docs/BACKEND_SCAFFOLD.md](docs/BACKEND_SCAFFOLD.md) — early scaffold notes (may be partially outdated)

## Architecture

Read path uses **your API** → **Fireflies** (`https://api.fireflies.ai/graphql`). Actions go through **Google / Meta / TinyFish** APIs. Guild is triggered after ingest when configured.
