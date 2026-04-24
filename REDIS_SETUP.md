# 🗄️ Redis Setup Guide

Your FastAPI backend is now integrated with Redis for persistent caching!

## What Changed

✅ Meeting data is now stored in Redis (not just memory)  
✅ 24-hour expiration on cached data  
✅ Survives server restarts  
✅ Fallback to in-memory if Redis unavailable  

---

## Quick Start: Run Redis Locally

### Option 1: Homebrew (Mac)
```bash
# Install Redis
brew install redis

# Start Redis server
redis-server

# You should see:
# * Ready to accept connections
```

### Option 2: Docker (Any OS)
```bash
# Start Redis in Docker
docker run -d -p 6379:6379 redis:latest

# Verify it's running
docker ps | grep redis
```

### Option 3: Download from redis.io
Visit https://redis.io/download and follow instructions for your OS.

---

## Verify Redis is Running

```bash
# Test connection
redis-cli ping
# Should return: PONG

# Or curl
curl http://localhost:6379
```

---

## Run Full Demo with Redis

### Terminal 1: Start Redis
```bash
redis-server
# You should see "Ready to accept connections"
```

### Terminal 2: Start FastAPI Backend
```bash
cd /Users/sankar/hackathons/meeting_agent
source venv/bin/activate
python3 server.py
```

**Expected output:**
```
✅ Redis connected: redis://localhost:6379
🚀 Starting Meeting Agent FastAPI Server
```

### Terminal 3: Start Next.js Frontend
```bash
cd /Users/sankar/hackathons/meeting_agent
npm run dev
```

Then open: http://localhost:3000

---

## What Happens with Redis

### Before (In-Memory Only)
```
Upload meeting
  → Process with agent
  → Store in Python dict
  → Server restarts
  → DATA LOST ❌
```

### Now (With Redis)
```
Upload meeting
  → Process with agent
  → Store in Redis with 24h TTL
  → Server restarts
  → DATA PERSISTS ✅
```

---

## Redis Data Structure

Your meetings are stored as:

```
Key: "meeting:{jobId}"
Value: {
  "jobId": "abc123",
  "title": "Meeting - file.mp4",
  "status": "completed",
  "transcript": "...",
  "summary": "...",
  "actions": [...],
  "emails": [...],
  "createdAt": "2026-04-24T..."
}

TTL: 86400 seconds (24 hours)
```

---

## View Redis Data

```bash
# Connect to Redis CLI
redis-cli

# List all keys
KEYS meeting:*

# Get specific meeting
GET meeting:abc123

# Get all meetings
KEYS meeting:*:status
```

---

## Environment Variables

Default: `redis://localhost:6379`

To change, set `REDIS_URL`:
```bash
export REDIS_URL="redis://user:password@host:6379"
```

Or in `.env`:
```
REDIS_URL=redis://localhost:6379
```

---

## Fallback Behavior

If Redis is unavailable:
```
Server starts: ⚠️  Redis not available
                    Falling back to in-memory storage
Data stored: In Python dict (lost on restart)
```

This is intentional - demo works without Redis, but persists better with it.

---

## Monitoring Redis Usage

### Terminal: Monitor Commands
```bash
redis-cli MONITOR
# Shows all commands as they happen
```

### Python: Check Keys
```bash
import redis
r = redis.from_url("redis://localhost:6379", decode_responses=True)
print(r.keys("meeting:*"))  # List all meetings
print(r.dbsize())           # Total keys
```

---

## Troubleshooting

### "Connection refused"
```bash
1. Make sure Redis is running: redis-cli ping
2. Check port: lsof -i :6379
3. Check REDIS_URL env var
```

### "Redis not available" message
```bash
1. Start Redis server: redis-server
2. Restart FastAPI: python3 server.py
```

### Slow queries
```bash
1. Check Redis with: redis-cli INFO
2. Monitor commands: redis-cli MONITOR
3. Clear old data: redis-cli FLUSHDB
```

---

## Clean Up Old Data

```bash
# Delete specific meeting
redis-cli DEL meeting:abc123

# Delete all meetings
redis-cli FLUSHDB

# Check expiration
redis-cli TTL meeting:abc123
```

---

## Data Persistence (Optional)

By default, Redis stores data in memory. To persist to disk:

Edit `/usr/local/etc/redis.conf`:
```
# Uncomment this line
save 900 1
```

Or use Docker with volume:
```bash
docker run -d \
  -p 6379:6379 \
  -v redis-data:/data \
  redis:latest \
  redis-server --appendonly yes
```

---

## Architecture Now

```
┌──────────────────────┐
│  Next.js Frontend    │
│  (localhost:3000)    │
└──────────────────────┘
           ↓
┌──────────────────────┐
│  FastAPI Backend     │
│  (localhost:8000)    │
└──────────────────────┘
           ↓
┌──────────────────────┐
│  Redis Cache         │  ← NEW!
│  (localhost:6379)    │
│  24h TTL             │
└──────────────────────┘
```

---

## Post-Demo

Redis is production-ready! You can:
- ✅ Run multiple backend instances (Redis shared state)
- ✅ Implement session management
- ✅ Add rate limiting
- ✅ Cache API responses
- ✅ Store job queues (with RQ or Celery)

---

## Quick Commands

```bash
# Start Redis
redis-server

# Connect
redis-cli

# Test
ping  # PONG

# Monitor
MONITOR

# Check keys
KEYS meeting:*

# Get meeting
GET meeting:{jobId}

# TTL
TTL meeting:{jobId}

# Clear all
FLUSHDB
```

---

**Redis is now integrated! 🚀**

Run: `redis-server` first, then start your demo.
