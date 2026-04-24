# Meeting agents API

Implements the **split** architecture:

- **Read tools** (`/tools/read/fireflies/transcript`): Fireflies GraphQL transcript fetch with Redis cache + rate limit.
- **Action tools** (`/tools/actions/*`): Gmail/Drive (Google OAuth), WhatsApp Cloud (policy + opt-in), TinyFish async job + Redis pointer.
- **Meetings** (`/meetings/ingest`): durable SQLite row from Fireflies transcript + optional Guild workflow trigger.
- **Admin** (`/admin/whatsapp/opt-in/{wa_id}`): set Redis opt-in for WhatsApp sends.

## Run locally

```bash
docker compose up -d redis   # from repo root
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Auth

All tool routes require header: `X-Internal-API-Key: <INTERNAL_API_KEY>`.

Optional capability gate for Guild tool registration: `X-Agent-Capabilities: gmail:send,fireflies:transcript,...`  
If omitted, all capabilities are allowed (dev-friendly). If present, each route checks its token.

Correlation id: `X-Correlation-Id` (optional; generated if missing).

## Fireflies

Set `FIREFLIES_API_KEY` (see [Fireflies docs](https://docs.fireflies.ai/fundamentals/authorization)). Optional overrides: `FIREFLIES_GRAPHQL_URL`, `FIREFLIES_TIMEOUT_SECONDS`.

## Environment

See [.env.example](.env.example) and [../docs/API_KEYS.md](../docs/API_KEYS.md).
