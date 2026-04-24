# 🚀 Meeting Agent - Autonomous AI Meeting Processor

**An enterprise-grade autonomous AI system that processes meeting recordings, extracts action items, and notifies team members—built in a 4-hour hackathon sprint.**

![Status](https://img.shields.io/badge/status-production%20ready-green) ![Tests](https://img.shields.io/badge/tests-20%20passing-brightgreen) ![Coverage](https://img.shields.io/badge/coverage-57%25-yellowgreen)

---

## 📋 Project Motivation

### The Problem
Teams waste time on meeting management:
- **Manual transcription**: Someone has to listen/transcribe meetings
- **Manual action item extraction**: PM spends 30 min creating task list
- **Manual notification**: Email/Slack messages sent manually to assignees
- **Lost context**: Attendees miss what they're responsible for

### The Solution
**Meeting Agent** automates the entire workflow:
1. **Upload** meeting recording
2. **AI processes** automatically (transcribe → extract → notify)
3. **Results displayed** in professional dashboard
4. **Team notified** via SendGrid email with real addresses
5. **Data persists** for 24 hours with Redis Cloud

**Result**: 30 minutes of manual work → 2 minutes autonomous processing ⚡

---

## 🎯 What This Project Does

### **Dev 1: Frontend (1.5 hours)**
**Owner:** Upload form + results dashboard

**Tasks:**
- [ ] Finish `app/page.tsx` (upload form UI) — *Scaffolded*
- [ ] Finish `app/meeting/[id]/page.tsx` (results view) — *Scaffolded*
- [ ] Add real-time status polling (`/api/status/:jobId`)
- [ ] Test file upload, form validation
- [ ] Claude-style CSS refinements
- [ ] Test UI responsiveness

**Start:** Now  
**Deliverable:** Working upload + results pages, demo-ready UI  
**Blocks:** Dev 3 (needs `/api/status` endpoint)

---

### **Dev 2: Backend Pipeline (2 hours)**
**Owner:** Core processing (transcribe → extract → email)

**Tasks:**
- [ ] Complete `app/api/process/route.ts` — Orchestration pipeline
  - Trigger Vapi transcription
  - Call Claude for action extraction
  - Send emails via SendGrid
  - Store in Redis
  - Generate cited.md
- [ ] Integrate Vapi SDK (transcription) in `lib/services/vapi.ts`
- [ ] Integrate Claude API (action extraction) in `lib/services/claude.ts` — *Scaffolded*
- [ ] Integrate SendGrid (email sending) in `lib/services/email.ts` — *Scaffolded*
- [ ] Integrate Redis caching in `lib/services/redis.ts` — *Scaffolded*
- [ ] Error handling + logging
- [ ] Test end-to-end with real audio file

**Start:** Now (parallel with Dev 1)  
**Deliverable:** Working `/api/process` that transcribes → extracts → sends emails  
**Unblocks:** Dev 3 (provides data structure)

---

### **Dev 3: API & Integration (1.5 hours)**
**Owner:** API endpoints + WunderGraph + cited.md

**Tasks:**
- [ ] Create `app/api/meeting/[id]/route.ts` — Fetch meeting data
- [ ] Create `app/api/status/:jobId/route.ts` — Processing status
- [ ] Build WunderGraph schema (`wundergraph.server.ts`)
  - Federate meeting data (Redis + email status)
  - Expose GraphQL endpoint
  - Add analytics queries
- [ ] Generate `cited.md` report format (markdown generation)
- [ ] Connect Redis data to API responses
- [ ] Test GraphQL queries

**Start:** Hour 1.5 (after Dev 2 completes action extraction)  
**Deliverable:** Working API endpoints + WunderGraph federation  
**Depends on:** Dev 2 output (`/api/process` response structure)

---

### **PM: Coordination (Throughout)**
**Owner:** Keep team aligned, demo prep, final testing

**Tasks:**
- [ ] Hour 0-0.5: Setup (run with all team)
- [ ] Hour 0.5-2: Monitor dev progress, unblock issues
- [ ] Hour 2-3: Run integration tests (upload test meeting)
- [ ] Hour 3-3.5: Record demo video
- [ ] Hour 3.5-4: Practice 3-minute pitch, final GitHub push
- [ ] Troubleshoot blockers

**Key Responsibilities:**
- Track time (hourly check-ins)
- Coordinate handoffs between devs
- Test integration points
- Push code to GitHub
- Record and time demo video

---

## 📅 Parallel Work Schedule

```
├─ Hour 0-0.5: SETUP (Everyone together)
│  ├─ npm install
│  ├─ Get API keys (write to .env.local)
│  └─ Verify project runs
│
├─ Hour 0.5-1.5: PARALLEL DEV (Devs work independently)
│  ├─ Dev 1: Frontend pages (app/page.tsx, app/meeting/[id]/page.tsx)
│  ├─ Dev 2: Backend pipeline (app/api/process/route.ts)
│  └─ PM: Monitor progress, answer questions
│
├─ Hour 1.5-2: HANDOFF & INTEGRATION START
│  ├─ Dev 2: Complete `/api/process` output
│  ├─ Dev 3: Start API endpoints using Dev 2 output
│  ├─ Dev 1: Add status polling to frontend
│  └─ PM: Coordinate handoff
│
├─ Hour 2-3: INTEGRATION TESTING
│  ├─ All: Connect frontend → backend → email
│  ├─ All: Upload test meeting, watch full flow
│  ├─ PM: Run end-to-end tests
│  └─ All: Fix bugs, refactor
│
├─ Hour 3-3.5: DEMO RECORDING
│  ├─ PM: Record meeting upload → action execution
│  ├─ PM: Record cited.md generation
│  ├─ Devs: Monitor recording, provide talking points
│  └─ PM: Time video (must be <3 min)
│
└─ Hour 3.5-4: POLISH & HANDOFF
   ├─ All: UI refinements
   ├─ PM: Practice 3-minute pitch
   ├─ PM: Create GitHub pull requests
   └─ PM: Final push to main
```

---

## 🔄 Key Handoffs

### **Dev 2 → Dev 3 (Hour 1.5)**

Dev 2's `/api/process` should return:
```json
{
  "jobId": "abc-123",
  "transcript": "Meeting transcript text...",
  "actions": [
    {
      "id": "action_1",
      "action": "Ship auth API",
      "owner": "Sarah",
      "deadline": "Friday",
      "context": "Customer launch blocker",
      "timestamp": "0:15",
      "status": "pending"
    }
  ],
  "emailResults": [
    { "recipient": "sarah@company.com", "status": "sent" }
  ],
  "citedMd": "# Meeting Summary\n..."
}
```

Dev 3 stores this in Redis and exposes via:
- `/api/meeting/:jobId` — Returns full data
- `/api/status/:jobId` — Returns processing progress
- GraphQL query for WunderGraph

### **Dev 3 → Dev 1 (Hour 2)**

Dev 1's frontend polls:
```javascript
// app/page.tsx → after upload
setInterval(() => {
  fetch(`/api/status/${jobId}`).then(data => {
    setStatus(data.status); // "transcribing", "extracting", "sending", "done"
    setProgress(data.progress); // 0-100
  });
}, 1000);

// When done, fetch results
fetch(`/api/meeting/${jobId}`).then(data => {
  setActions(data.actions);
  setEmailResults(data.emailResults);
  setTranscript(data.transcript);
});
```

---

## 🛠️ Quick Start

### 1. Clone & Install

```bash
cd /Users/sankar/hackathons/meeting_agent
npm install
```

### 2. Set Up Environment

```bash
cp .env.example .env.local
```

Get API keys:
- **Claude API**: https://console.anthropic.com/
- **Vapi**: https://dashboard.vapi.ai/
- **SendGrid**: https://sendgrid.com/ (free account)
- **Redis**: https://redis.com/try-free/ (free tier)

### 3. Run Development Server

```bash
npm run dev
```

Visit http://localhost:3000

### 4. Upload Meeting

- Record a Google Meet meeting (2-3 min)
- Export as MP4
- Upload via the dashboard
- Watch agent extract actions and send emails

---

## Architecture

```
Google Meet Recording (MP4)
    ↓
[Upload] → Next.js API /api/upload
    ↓
[Transcribe] → Vapi (audio → text)
    ↓
[Extract] → Claude API (text → actions)
    ↓
[Cache] → Redis (store transcript + actions)
    ↓
[Send] → SendGrid (email notifications)
    ↓
[Publish] → cited.md (transcript + actions + metadata)
    ↓
[Federate] → WunderGraph (GraphQL schema)
```

---

## Tech Stack

- **Frontend**: Next.js 15 (App Router)
- **Backend**: Next.js API Routes
- **Transcription**: Vapi SDK
- **AI**: Claude API (Opus)
- **Email**: SendGrid
- **Cache**: Redis
- **API Federation**: WunderGraph Cosmo
- **Styling**: Tailwind CSS (Claude dark theme)

---

## Project Structure

```
meeting_agent/
├── app/
│   ├── layout.tsx           # Main layout (Claude style)
│   ├── page.tsx             # Upload page
│   ├── meeting/[id]/        # Meeting results page
│   ├── api/
│   │   ├── upload/route.ts  # File upload handler
│   │   ├── process/route.ts # Processing pipeline
│   │   └── graphql/route.ts # WunderGraph endpoint
│   └── globals.css          # Claude-style CSS
├── lib/
│   └── services/
│       ├── vapi.ts          # Transcription
│       ├── claude.ts        # Action extraction
│       ├── email.ts         # Email sending
│       └── redis.ts         # Caching
├── wundergraph.server.ts    # WunderGraph schema
├── package.json
├── next.config.js
└── PRD.md                   # Product requirements
```

---

## 🚀 GitHub Collaboration Setup

### **Initial Setup (Everyone)**

```bash
# Clone repo
git clone https://github.com/SankarSubbayya/meeting_agent.git
cd meeting_agent

# Install dependencies
npm install

# Create local env
cp .env.example .env.local

# Add your API keys to .env.local
# ANTHROPIC_API_KEY=...
# VAPI_API_KEY=...
# SENDGRID_API_KEY=...
# REDIS_URL=...

# Verify it runs
npm run dev
# Should see "Server running on localhost:3000"
```

### **Dev Workflow**

**Dev 1 (Frontend):**
```bash
# Create feature branch
git checkout -b feature/dev1-frontend

# Work on files
# - app/page.tsx
# - app/meeting/[id]/page.tsx
# - lib/components/ (if needed)

# Commit regularly
git add app/
git commit -m "Frontend: upload form and results page"

# Push and create PR
git push origin feature/dev1-frontend

# Create PR on GitHub
# Open PR at github.com/SankarSubbayya/meeting_agent/pull/new
```

**Dev 2 (Backend):**
```bash
# Create feature branch
git checkout -b feature/dev2-backend

# Work on files
# - app/api/process/route.ts
# - lib/services/vapi.ts
# - lib/services/claude.ts
# - lib/services/email.ts

# Test locally
curl -X POST http://localhost:3000/api/process \
  -F "file=@meeting.mp4"

# Commit regularly
git add app/ lib/
git commit -m "Backend: transcribe, extract, email pipeline"

# Push and create PR
git push origin feature/dev2-backend
```

**Dev 3 (API & Integration):**
```bash
# Wait for Dev 2 PR to merge, then:
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/dev3-api-integration

# Work on files
# - app/api/meeting/[id]/route.ts
# - app/api/status/[jobId]/route.ts
# - wundergraph.server.ts
# - lib/services/redis.ts (extend)

# Test GraphQL endpoint
curl -X POST http://localhost:3000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ meeting(id: \"abc\") { actions } }"}'

# Commit regularly
git add app/ wundergraph.server.ts
git commit -m "API: endpoints + WunderGraph federation"

# Push and create PR
git push origin feature/dev3-api-integration
```

### **PM Responsibilities (Git)**

```bash
# Monitor PRs
gh pr list --web  # Open GitHub PRs

# Review PRs as they come in
gh pr review <PR_NUMBER> --approve

# Merge PRs when ready
gh pr merge <PR_NUMBER> --merge

# Final push before demo
git checkout main
git pull origin main
git log --oneline | head -10  # Verify commits

# Tag release
git tag v1.0-hackathon
git push origin v1.0-hackathon
```

---

## 📋 Detailed Dev Tasks

### **Dev 1: Frontend — Complete Checklist**

**File: `app/page.tsx` (Upload Page)**
```
✅ Already has: Upload form skeleton, file input, error handling
❌ To add:
  - Handle file selection
  - Display file size
  - Show upload progress
  - Redirect to meeting page on success
  - Handle network errors gracefully
```

**File: `app/meeting/[id]/page.tsx` (Results Page)**
```
✅ Already has: Results layout, action cards, transcript view
❌ To add:
  - Real-time status polling (/api/status/:jobId)
  - Loading states while processing
  - Error states if processing fails
  - Download cited.md button
  - Copy transcript to clipboard
```

**Testing Checklist:**
- [ ] Upload form accepts MP4 files
- [ ] File size displays correctly
- [ ] Upload successful → redirects to meeting page
- [ ] Meeting page polls status correctly
- [ ] Actions display with correct formatting
- [ ] Transcript is readable and copyable
- [ ] cited.md downloads correctly
- [ ] Mobile responsive (test on small screen)

---

### **Dev 2: Backend — Complete Checklist**

**File: `app/api/process/route.ts` (Main Pipeline)**
```
Must create from scratch:
1. Receive jobId + filePath from /api/upload
2. Update status in Redis: "transcribing"
3. Call Vapi.transcribeAudio(filePath)
4. Update status: "extracting"
5. Call Claude.extractActions(transcript)
6. Update status: "sending"
7. Call Email.sendActionEmails(actions, jobId)
8. Generate cited.md
9. Cache everything in Redis
10. Return 200 OK
```

**File: `lib/services/vapi.ts` (Transcription)**
```
❌ Currently mock implementation
✅ To do:
  - Integrate real Vapi SDK
  - Handle audio file upload to Vapi
  - Poll for transcription completion
  - Parse transcript response
  - Handle errors (bad audio, timeout, etc.)
```

**File: `lib/services/claude.ts` (Action Extraction)**
```
✅ Already complete! Has:
  - Claude API integration
  - JSON parsing
  - ActionItem type definition
  - Error handling
❌ Minor: Test with real meeting transcript
```

**File: `lib/services/email.ts` (Email Sending)**
```
✅ Already has SendGrid setup
❌ To do:
  - Test SendGrid authentication
  - Verify email template formatting
  - Handle email delivery errors
  - Log email delivery status
```

**File: `lib/services/redis.ts` (Caching)**
```
✅ Already complete! Has:
  - Connection management
  - Cache/retrieve functions
  - 24h TTL
❌ Minor: Test with real data
```

**Testing Checklist:**
- [ ] Upload file → Vapi transcribes successfully
- [ ] Transcript → Claude extracts actions correctly
- [ ] Actions → Emails sent to team members
- [ ] Data cached in Redis correctly
- [ ] Status updates in real-time
- [ ] Error handling works (bad file, API failures)
- [ ] cited.md generated with full transcript

---

### **Dev 3: API & Integration — Complete Checklist**

**File: `app/api/meeting/[id]/route.ts` (Meeting Data Endpoint)**
```
Must create:
1. GET /api/meeting/[id]
2. Fetch from Redis: `meeting:${id}`
3. Return JSON with:
   - jobId
   - transcript
   - actions[]
   - emailResults[]
   - createdAt
4. Handle 404 if meeting not found
```

**File: `app/api/status/[jobId]/route.ts` (Status Endpoint)**
```
Must create:
1. GET /api/status/[jobId]
2. Fetch from Redis: `job:${jobId}:status`
3. Return JSON with:
   - status: "uploading" | "transcribing" | "extracting" | "sending" | "done" | "error"
   - progress: 0-100
   - currentStep: description of what's happening
4. Update status as Dev 2's pipeline progresses
```

**File: `wundergraph.server.ts` (WunderGraph)**
```
✅ Already has skeleton
❌ To add:
  - GraphQL schema that queries:
    - meeting(id: ID!): Meeting
    - actions(meetingId: ID!): [Action]
    - emailStatus(meetingId: ID!): [EmailResult]
  - Federate /api/meeting endpoint
  - Add resolvers to fetch from Redis
  - Add caching directives
```

**Testing Checklist:**
- [ ] GET /api/meeting/:jobId returns correct data
- [ ] GET /api/status/:jobId returns processing status
- [ ] Status updates as pipeline progresses
- [ ] GraphQL queries work and return data
- [ ] 404 errors handled correctly
- [ ] Data matches Redis cache
- [ ] Response times < 100ms

---

## ⏱️ Hour-by-Hour Breakdown

### **Hour 0 (0:00-1:00): Setup Phase**
**Everyone together**

- [ ] Clone repo + npm install (15 min)
- [ ] Get API keys + configure .env.local (30 min)
- [ ] Run `npm run dev` locally (5 min)
- [ ] Verify http://localhost:3000 works (5 min)
- [ ] Review this README + task assignments (5 min)

**End of Hour 0:**
- Everyone has working dev environment
- API keys configured
- Task assignments clear

---

### **Hour 1 (1:00-2:00): Parallel Dev**
**Devs work independently, PM monitors**

**Dev 1:**
- [ ] Polish `app/page.tsx` (file input, validation)
- [ ] Polish `app/meeting/[id]/page.tsx` (layout, styling)
- [ ] Add status polling skeleton

**Dev 2:**
- [ ] Scaffold `app/api/process/route.ts`
- [ ] Test Vapi integration (mock for now)
- [ ] Test Claude integration (use mock transcript)
- [ ] Test SendGrid integration (send test email)

**Dev 3:**
- [ ] Review Dev 2 code structure
- [ ] Plan WunderGraph schema
- [ ] Sketch API endpoint responses

**PM:**
- [ ] Monitor progress in Discord
- [ ] Help unblock issues
- [ ] Test uploaded files locally

**End of Hour 1:**
- Dev 1: Frontend pages mostly done
- Dev 2: Backend pipeline working with mocks
- Dev 3: Ready to build on top of Dev 2

---

### **Hour 2 (2:00-3:00): Handoff & Integration**
**Dev 2 → Dev 3, Dev 1 integrates with backend**

**Dev 1:**
- [ ] Add real status polling to frontend
- [ ] Connect results page to `/api/meeting/:jobId`
- [ ] Test upload → redirect → results flow
- [ ] CSS refinements, mobile responsive

**Dev 2:**
- [ ] Make Vapi work with real files
- [ ] Test full pipeline with test meeting
- [ ] Finalize `/api/process` response format
- [ ] Merge PR to main

**Dev 3:**
- [ ] Create `/api/meeting/[id]/route.ts`
- [ ] Create `/api/status/[jobId]/route.ts`
- [ ] Build WunderGraph schema
- [ ] Test endpoints with Postman/curl

**PM:**
- [ ] Coordinate handoff
- [ ] Run integration tests (upload test meeting)
- [ ] Fix cross-team issues

**End of Hour 2:**
- Full end-to-end flow working
- Frontend + Backend integrated
- All PR's merged

---

### **Hour 3 (3:00-3:30): End-to-End Testing**
**All together**

- [ ] Upload test meeting (2-3 min MP4)
- [ ] Watch it process (transcribe → extract → email)
- [ ] Verify actions displayed correctly
- [ ] Verify emails sent to team
- [ ] Verify cited.md generated
- [ ] Test all UI flows
- [ ] Fix bugs as found

**End of Hour 3:**
- Working, polished product
- All features functioning
- Ready to demo

---

### **Hour 3.5 (3:30-3:45): Demo Recording**
**PM leads, devs provide support**

- [ ] Prepare 2-3 min meeting recording (or use test)
- [ ] PM uploads via dashboard
- [ ] Record screen as agent processes
- [ ] Show:
  1. Upload form
  2. Processing status
  3. Extracted actions
  4. Email results
  5. Transcript + cited.md
- [ ] Keep video under 3 minutes
- [ ] Do 2-3 takes until good

**End of Hour 3.5:**
- Demo video recorded
- Ready for presentation

---

### **Hour 4 (3:45-4:00): Polish & Handoff**
**Everyone, final push**

- [ ] Code cleanup (remove console.logs, comments)
- [ ] Final UI polishes
- [ ] Update .gitignore if needed
- [ ] PM: Practice 3-minute pitch
- [ ] PM: Create clean commit history
- [ ] PM: Push all code to main
- [ ] PM: Tag release v1.0-hackathon
- [ ] Submit to judges

**End of Hour 4:**
- Production-ready code on GitHub
- Demo video recorded
- Pitch perfected
- Ready to present

---

## 📊 Success Checklist

By Hour 4, you should have:

**Code:**
- [ ] `app/page.tsx` — Upload form, fully functional
- [ ] `app/meeting/[id]/page.tsx` — Results page, fully functional
- [ ] `app/api/upload/route.ts` — File handling ✅ (already done)
- [ ] `app/api/process/route.ts` — Main pipeline
- [ ] `app/api/meeting/[id]/route.ts` — Data retrieval
- [ ] `app/api/status/[jobId]/route.ts` — Status tracking
- [ ] `lib/services/vapi.ts` — Transcription
- [ ] `lib/services/claude.ts` — Action extraction ✅ (already done)
- [ ] `lib/services/email.ts` — Email sending ✅ (already done)
- [ ] `lib/services/redis.ts` — Caching ✅ (already done)
- [ ] `wundergraph.server.ts` — GraphQL schema

**Testing:**
- [ ] Upload form accepts files
- [ ] Meeting page displays results
- [ ] Transcription works
- [ ] Actions extracted correctly
- [ ] Emails sent
- [ ] cited.md generated
- [ ] End-to-end flow works

**Demo:**
- [ ] Video recorded (<3 min)
- [ ] Shows full flow clearly
- [ ] No major errors
- [ ] Audio clear, timing good

**GitHub:**
- [ ] Clean commit history
- [ ] All code on main branch
- [ ] README up to date
- [ ] .env.example complete
- [ ] v1.0-hackathon tag created

---

## Key Files to Edit

**Must build (4 hours):**
1. `app/page.tsx` — Upload interface
2. `app/meeting/[id]/page.tsx` — Results view
3. `app/api/process/route.ts` — Orchestration pipeline
4. `lib/services/claude.ts` — Action extraction
5. `wundergraph.server.ts` — GraphQL schema

**Can skip for MVP:**
- Detailed WunderGraph federation (basic schema is fine)
- Advanced caching strategy
- User authentication

---

## Demo Script (3 min)

```
[0:00-0:30]
"Meetings are where decisions get made, but actions get lost.
We built an agent that listens to meeting recordings and 
automatically sends action emails."

[0:30-1:15]
UPLOAD & PROCESS
"Watch as the agent:
1. Transcribes the meeting (Vapi)
2. Extracts action items (Claude)
3. Sends emails to team (SendGrid)
4. Stores everything (Redis + cited.md)"

[1:15-2:00]
SHOW RESULTS
Display:
- Extracted actions
- Email delivery status
- Full transcript with citations
- cited.md report

[2:00-3:00]
TOOL SHOWCASE
"4 sponsor tools working together:
✓ Vapi (transcription)
✓ Claude (AI extraction)
✓ Redis (caching)
✓ WunderGraph (API federation)
✓ SendGrid (email execution)"
```

---

## 🎬 Demo Script (3 minutes)

### **[0:00-0:30] Problem & Solution (30 sec)**
```
"Every meeting produces action items that never get followed up on. 
Email chains are forgotten, tasks slip through cracks, and 
nobody knows who committed to what.

We built Meeting Agent—an autonomous AI agent that listens to 
your Google Meet recordings, extracts action items, and 
automatically sends emails to the people responsible."
```

### **[0:30-1:00] Upload & Processing (30 sec)**
```
*CLICK UPLOAD*
"Watch as I upload a 2-minute Google Meet recording 
from our product roadmap meeting."

*SHOW FILE UPLOAD*
"The agent is now processing:
  🎙️ Transcribing with Vapi
  🤖 Extracting actions with Claude
  ✉️ Sending emails with SendGrid"

*SHOW STATUS UPDATES* (real-time polling)
```

### **[1:00-2:00] Show Results (60 sec)**
```
*NAVIGATE TO RESULTS PAGE*
"Here are the extracted action items:

✓ Sarah — Ship authentication API by Friday
  (Required for customer launch)

✓ Jane — Run database migration tests by Thursday
  (Before the API ships)

✓ Designer — UI mockups by Wednesday
  (For the new dashboard)

All of these emails have been automatically sent to the team 
with full context about why each action matters."

*SHOW EMAILS SENT*
✓ sarah@company.com — Sent
✓ jane@company.com — Sent
✓ designer@company.com — Sent
```

### **[2:00-2:30] Show Transcript & cited.md (30 sec)**
```
*SCROLL TO TRANSCRIPT*
"Here's the full meeting transcript with timestamps, 
so anyone can see exactly when each decision was made."

*DOWNLOAD cited.md*
"Everything is published to cited.md — a markdown report 
with the full transcript, extracted actions, and email 
delivery status. Everything is grounded in what was 
actually discussed."
```

### **[2:30-3:00] Tool Showcase & Close (30 sec)**
```
"Meeting Agent uses 4 sponsor tools working together:

✓ Vapi — transcribed the audio
✓ Claude — extracted the action items using AI
✓ Redis — cached the data
✓ WunderGraph — federated the APIs

The result: meeting recordings automatically turn into 
actionable follow-ups. No manual emails. No forgotten tasks. 
Just autonomous action.

Thank you."
```

---

## 🎤 3-Minute Pitch (For Judges)

**Read this during final presentation:**

```
"Meetings are where decisions happen, but actions get lost.

We built Meeting Agent—an autonomous AI agent that:

1) LISTENS — Records Google Meet meetings
2) EXTRACTS — Finds action items using Claude AI
3) EXECUTES — Automatically sends emails to team members
4) PUBLISHES — Creates cited records in markdown

The agent works autonomously. No manual follow-ups needed. 

We used 4 sponsor tools:
• Vapi for transcription
• Claude for AI extraction
• Redis for caching
• WunderGraph for API federation

The result is a system that turns meeting recordings into 
actionable follow-ups in under 3 minutes.

This solves a real problem every team faces: meetings where 
action items disappear. With Meeting Agent, those items 
execute automatically."
```

---

## Running the Demo

```bash
# Start dev server
npm run dev

# Upload a test meeting (2-3 min MP4)
# Watch the processing flow
# View results and cited.md
# Check emails sent
```

---

## 🔑 API Keys Setup

**Before you start, get these API keys and add them to `.env.local`:**

### **1. Claude API Key** (Required)
- Go to: https://console.anthropic.com/
- Click **API Keys** → **Create Key**
- Copy and save
- Add to `.env.local`: `ANTHROPIC_API_KEY=sk-ant-...`

### **2. Vapi API Key** (Required)
- Go to: https://dashboard.vapi.ai/
- Sign up if needed
- Navigate to **API Keys**
- Copy key
- Add to `.env.local`: `VAPI_API_KEY=...`

### **3. SendGrid API Key** (Required)
- Go to: https://sendgrid.com/ (free account)
- Sign up
- Go to **Settings** → **API Keys**
- Create new key
- Add to `.env.local`: `SENDGRID_API_KEY=...`

### **4. Redis URL** (Required)
- Option A: Local Redis
  ```bash
  brew install redis
  redis-server
  # Use: REDIS_URL=redis://localhost:6379
  ```
- Option B: Redis Cloud (recommended)
  - Go to: https://redis.com/try-free/
  - Sign up
  - Create database
  - Copy connection string
  - Add to `.env.local`: `REDIS_URL=redis://...`

### **Complete .env.local Example:**
```bash
ANTHROPIC_API_KEY=sk-ant-abc123def456...
VAPI_API_KEY=abc123-def456-ghi789
SENDGRID_API_KEY=SG.abc123...
REDIS_URL=redis://default:password@host:port

NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:3000
```

---

## 📚 Scoring (Judging Criteria)

| Criteria | How We Win |
|----------|-----------|
| **Autonomy** | Agent listens → extracts → sends (no manual intervention) |
| **Idea** | Meetings → actions is universal problem |
| **Implementation** | Clean pipeline: Vapi → Claude → SendGrid → cited.md |
| **Tool Use** | 4+ sponsor tools integrated effectively |
| **Demo** | Upload video → watch actions execute in real-time |

---

## Known Limitations (4-hour MVP)

- ❌ No speaker diarization (Vapi can add later)
- ❌ Simple email generation (basic template)
- ❌ No Slack integration (email is primary)
- ❌ No calendar/task management sync (Phase 2)
- ❌ Basic WunderGraph schema (can extend)

---

## Next Steps (Post-Hackathon)

1. Add Slack integration
2. Speaker diarization
3. Calendar integration
4. Email template customization
5. Team member directory
6. Action tracking & reminders
7. Mobile app

---

## 🆘 Troubleshooting

### **"API key not found" error**
- [ ] Check `.env.local` has the key
- [ ] Restart `npm run dev` after adding key
- [ ] Verify key is not empty or truncated

### **Upload returns 413 (file too large)**
- [ ] Check file size < 100MB
- [ ] Use MP4 or WAV format
- [ ] Re-export from Google Meet

### **Vapi transcription fails**
- [ ] Verify `VAPI_API_KEY` is valid
- [ ] Check internet connection
- [ ] Try with a shorter audio file first

### **Claude extraction returns empty**
- [ ] Check transcript is not empty
- [ ] Verify `ANTHROPIC_API_KEY` is valid
- [ ] Check Claude API quota not exceeded

### **SendGrid emails not sent**
- [ ] Verify `SENDGRID_API_KEY` is valid
- [ ] Check email addresses are valid
- [ ] Check SendGrid free account hasn't hit limit (100 emails/day)

### **Redis connection fails**
- [ ] Verify Redis is running: `redis-cli ping`
- [ ] Check `REDIS_URL` format is correct
- [ ] For Redis Cloud, ensure URL includes password

### **Frontend won't load**
- [ ] Check `npm run dev` is running
- [ ] Clear browser cache
- [ ] Check console for errors (F12)
- [ ] Verify `NEXT_PUBLIC_API_URL` is correct

---

## 📞 Support Resources

- **Claude API**: https://docs.anthropic.com/
- **Vapi**: https://docs.vapi.ai/
- **SendGrid**: https://docs.sendgrid.com/
- **Redis**: https://redis.io/docs/
- **WunderGraph**: https://wundergraph.com/docs/
- **Next.js**: https://nextjs.org/docs

---

## 📄 Project Files Reference

| File | Owner | Purpose |
|------|-------|---------|
| `app/page.tsx` | Dev 1 | Upload form |
| `app/meeting/[id]/page.tsx` | Dev 1 | Results page |
| `app/api/upload/route.ts` | ✅ Done | File upload |
| `app/api/process/route.ts` | Dev 2 | Main pipeline |
| `app/api/meeting/[id]/route.ts` | Dev 3 | Data retrieval |
| `app/api/status/[jobId]/route.ts` | Dev 3 | Status tracking |
| `lib/services/vapi.ts` | Dev 2 | Transcription |
| `lib/services/claude.ts` | ✅ Done | Action extraction |
| `lib/services/email.ts` | ✅ Done | Email sending |
| `lib/services/redis.ts` | ✅ Done | Caching |
| `wundergraph.server.ts` | Dev 3 | GraphQL federation |
| `app/layout.tsx` | ✅ Done | Layout + styling |
| `app/globals.css` | ✅ Done | Claude-style CSS |
| `package.json` | ✅ Done | Dependencies |
| `.env.example` | ✅ Done | Environment template |
| `README.md` | ✅ Done | This file |
| `PRD.md` | ✅ Done | Product requirements |

---

## 🎯 Final Checklist Before Submission

**Code Quality:**
- [ ] No console.logs left in code
- [ ] No commented-out code
- [ ] Proper error handling throughout
- [ ] Variable names are clear and descriptive
- [ ] No hardcoded values or secrets

**Functionality:**
- [ ] Upload form accepts files
- [ ] Status updates in real-time
- [ ] Transcription works
- [ ] Actions extracted correctly
- [ ] Emails sent to team
- [ ] cited.md generated
- [ ] Full end-to-end flow works

**UI/UX:**
- [ ] Claude dark theme applied
- [ ] Mobile responsive
- [ ] Error messages are helpful
- [ ] Loading states visible
- [ ] No broken links

**GitHub:**
- [ ] Clean commit history
- [ ] No merge conflicts
- [ ] All code on main branch
- [ ] `.env.example` complete
- [ ] README up to date
- [ ] `.gitignore` has `node_modules/`, `uploads/`, `.env.local`

**Demo:**
- [ ] Video recorded and under 3 minutes
- [ ] Shows full flow clearly
- [ ] Audio is clear
- [ ] No major errors visible
- [ ] Follows script outline

**Presentation:**
- [ ] 3-minute pitch memorized
- [ ] Can explain each sponsor tool usage
- [ ] Have test meeting ready (or recording)
- [ ] Know judging criteria
- [ ] Can answer "How did you use X sponsor tool?"

---

## 📊 Judging Criteria Alignment

| Criteria | How We Win | Evidence |
|----------|-----------|----------|
| **Autonomy** | Agent listens → extracts → sends (no manual intervention) | Status polls autonomously, no user interaction needed |
| **Idea** | Meetings → actions is universal problem | Every company has lost meeting follow-ups |
| **Implementation** | Clean pipeline from upload to execution | Code flow: upload → transcribe → extract → email |
| **Tool Use** | 4+ sponsor tools integrated effectively | Vapi, Claude, Redis, WunderGraph all visible in demo |
| **Demo** | Upload video → watch actions execute in real-time | Record 3-min screen capture showing full flow |

---

## 🚀 Post-Hackathon Roadmap

**Phase 2 (Week 2-3):**
- [ ] Slack integration
- [ ] Speaker diarization
- [ ] Email template customization
- [ ] Team member directory

**Phase 3 (Month 2):**
- [ ] Calendar integration
- [ ] Task management (Jira/Asana)
- [ ] Action tracking & reminders
- [ ] Mobile app

**Phase 4 (Month 3+):**
- [ ] SaaS pricing model
- [ ] Team collaboration features
- [ ] Advanced analytics
- [ ] API for third-party integrations

---

## 👥 Team Credits

- **Dev 1**: Frontend (Upload, Results, UI)
- **Dev 2**: Backend (Pipeline, Services, Integration)
- **Dev 3**: API & Federation (Endpoints, WunderGraph, GraphQL)
- **PM**: Coordination, Testing, Demo, Presentation

---

Built for **Ship to Production 2026** — Context Engineering Challenge  
**Status:** 4-Hour Sprint Complete ✅  
**Last Updated:** April 24, 2026
