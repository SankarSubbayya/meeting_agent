# API keys and secrets (meeting agents backend)

Use a `.env` file locally (never commit secrets). In production, use AWS Secrets Manager or similar.

## Required for the split you chose

### Read path — Fireflies GraphQL API

| Variable | Purpose |
|----------|---------|
| `FIREFLIES_API_KEY` | API key from Fireflies (Integrations → Fireflies API). Sent as `Authorization: Bearer …`. |
| `FIREFLIES_GRAPHQL_URL` | Defaults to `https://api.fireflies.ai/graphql`. |
| `FIREFLIES_TIMEOUT_SECONDS` | HTTP timeout for GraphQL calls (default 60). |

Docs: [Fireflies API](https://docs.fireflies.ai/getting-started/quickstart).

### Orchestration — Guild.ai

| Variable | Purpose |
|----------|---------|
| `GUILD_API_BASE` | Guild API base URL (from Guild docs / your deployment). |
| `GUILD_API_KEY` | API key or token to start workflows and pass context from your backend. |

*(Exact names depend on Guild’s API; adjust after you read their auth docs.)*

### Action path — Google (Gmail, Drive, Docs)

| Variable | Purpose |
|----------|---------|
| `GOOGLE_CLIENT_ID` | OAuth 2.0 Web/Desktop app client ID (Google Cloud Console). |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret. |
| `GOOGLE_REFRESH_TOKEN` | Refresh token for the mailbox / Drive you send from (obtained once via OAuth consent). |

**Alternative:** a **service account** JSON path (`GOOGLE_APPLICATION_CREDENTIALS`) if you use domain-wide delegation for Workspace—different setup, no refresh token in `.env`.

### Action path — WhatsApp Business (Cloud API)

| Variable | Purpose |
|----------|---------|
| `WHATSAPP_ACCESS_TOKEN` | Permanent or long-lived system user token from Meta. |
| `WHATSAPP_PHONE_NUMBER_ID` | Phone number ID for the WhatsApp sender. |
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | WABA ID (often needed for templates / analytics APIs). |

### Action path — TinyFish (optional web fallback)

| Variable | Purpose |
|----------|---------|
| `TINYFISH_API_KEY` | TinyFish API key. |
| `TINYFISH_BASE_URL` | Defaults to TinyFish API host if they give you a custom base. |

## Strongly recommended

### Redis

| Variable | Purpose |
|----------|---------|
| `REDIS_URL` | e.g. `redis://localhost:6379/0` — idempotency, transcript cache, rate limits. |

## Optional (if the backend calls an LLM directly)

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | If you add a local planner or fallback model. |
| `ANTHROPIC_API_KEY` | Same, for Claude. |

If **all** reasoning runs inside Guild only, you may omit these on the backend.

---

## Minimum set to ship a vertical slice

1. `FIREFLIES_API_KEY` — fetch transcripts (`/tools/read/fireflies/transcript`, `/meetings/ingest`)
2. `GUILD_*` — run the agent workflow after meeting is normalized  
3. `GOOGLE_*` OR WhatsApp set — at least one real “do something” action  
4. `REDIS_URL` — dedupe / cache  

TinyFish keys only when you add the first web-only tool.
