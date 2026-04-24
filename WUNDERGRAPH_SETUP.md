# 🔗 WunderGraph Integration

WunderGraph provides a GraphQL API layer on top of your FastAPI backend.

## What WunderGraph Does

✅ **GraphQL API Layer** - Wrap REST endpoints in GraphQL  
✅ **Type-Safe Client** - Auto-generated TypeScript types  
✅ **Unified Data Layer** - Single endpoint for all data  
✅ **Query Composition** - Combine multiple API calls  
✅ **Caching & Optimization** - Smart request management  

---

## Architecture

```
Next.js Frontend
    ↓
WunderGraph (GraphQL Layer)
    ↓
FastAPI Backend
    ↓
Redis Cache + Claude Agent
```

---

## How to Run with WunderGraph

### Terminal 1: Start Redis
```bash
redis-server
```

### Terminal 2: Start FastAPI Backend
```bash
source venv/bin/activate
python3 server.py
```

### Terminal 3: Start WunderGraph
```bash
npm run wg dev
# Or manually:
npx wundergraph up
```

### Terminal 4: Start Next.js Frontend
```bash
npm run dev
```

---

## GraphQL Operations

WunderGraph exposes GraphQL operations defined in `.wundergraph/operations/`:

### Query: GetMeeting
```graphql
query GetMeeting($jobId: String!) {
  meeting(jobId: $jobId) {
    jobId
    title
    status
    summary
    transcript
    actions {
      id
      action
      owner
      deadline
    }
    emails {
      recipient
      status
    }
  }
}
```

### Query: GetMeetings
```graphql
query GetMeetings {
  meetings {
    jobId
    title
    status
    createdAt
  }
}
```

### Query: GetStatus
```graphql
query GetStatus($jobId: String!) {
  status(jobId: $jobId) {
    jobId
    status
    progress
  }
}
```

### Mutation: UploadMeeting
```graphql
mutation UploadMeeting($file: File!) {
  uploadMeeting(file: $file) {
    jobId
    status
  }
}
```

---

## Using in Frontend

### With WunderGraph Hook
```typescript
import { useQuery } from '@wundergraph/nextjs';

function MeetingDetail({ jobId }: { jobId: string }) {
  const { data, loading, error } = useQuery.GetMeeting({
    jobId,
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1>{data?.meeting.title}</h1>
      <p>{data?.meeting.summary}</p>
    </div>
  );
}
```

### With GraphQL Client
```typescript
const client = new WunderGraphClient({
  endpoint: 'http://localhost:3000/api/wg',
});

const result = await client.query.GetMeeting({
  jobId: 'abc123',
});
```

---

## Project Structure

```
.wundergraph/
├── wundergraph.config.ts       # Main configuration
├── wundergraph.server.ts       # Server hooks
├── wundergraph.hooks.ts        # Global hooks
└── operations/
    ├── index.ts                # Operation handlers
    └── *.graphql               # GraphQL definitions
```

---

## Configuration Files

### wundergraph.config.ts
Main configuration file that:
- Defines data sources (REST APIs, GraphQL, databases)
- Configures authentication
- Sets up CORS
- Enables GraphQL endpoint

### wundergraph.server.ts
Server-side hooks for:
- Pre/post operation resolvers
- Custom logic
- Performance optimizations

---

## Performance Benefits

1. **Type Safety** - Full TypeScript types auto-generated
2. **Deduplication** - WunderGraph deduplicates queries
3. **Caching** - Built-in response caching
4. **Batch Loading** - Combines multiple requests
5. **Live Queries** - Real-time updates support

---

## Deployment

### Development
```bash
npm run wg dev
```

### Production Build
```bash
npm run build
```

### Deploy to Vercel
```bash
npm run deploy
```

---

## Integration with Existing Stack

**Replaces:** Direct fetch calls to FastAPI

**Before:**
```typescript
const response = await fetch('http://localhost:8000/api/meeting/abc123');
```

**After (with WunderGraph):**
```typescript
const { data } = await useQuery.GetMeeting({ jobId: 'abc123' });
```

---

## Next Steps

1. ✅ Install WunderGraph (`npm install -D @wundergraph/sdk @wundergraph/nextjs`)
2. ✅ Configure operations
3. ⏳ Generate types: `npm run wg:generate`
4. ⏳ Update frontend to use WunderGraph hooks
5. ⏳ Deploy to production

---

## Common Commands

```bash
# Start development
npm run wg dev

# Generate types
npm run wg:generate

# Build for production
npm run build

# View GraphQL playground
open http://localhost:3000/api/wg
```

---

## Benefits for Your Project

✅ **Single GraphQL endpoint** instead of multiple REST calls  
✅ **Type-safe** - No more manual typing  
✅ **Optimized** - Deduplication, caching  
✅ **Professional** - Production-ready architecture  
✅ **Extensible** - Easy to add more operations  

---

## Troubleshooting

### "Cannot find module '@wundergraph/sdk'"
```bash
npm install --legacy-peer-deps -D @wundergraph/sdk @wundergraph/nextjs
```

### "WunderGraph server not responding"
```bash
1. Make sure npm run wg dev is running
2. Check port 3000 is accessible
3. Check CORS settings
```

### "GraphQL query failed"
```bash
1. Verify FastAPI backend is running on 8000
2. Check WunderGraph operation definition
3. Review browser console for errors
```

---

**WunderGraph is now integrated as your GraphQL API layer!** 🚀
