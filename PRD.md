# Meeting Agent — Product Requirements Document

**Version:** 1.0  
**Date:** April 24, 2026  
**Team:** SankarSubbayya + Team  
**Hackathon:** Ship to Production 2026 — Context Engineering Challenge

---

## Executive Summary

**Meeting Agent** is an autonomous AI agent that listens to Google Meet recordings, extracts action items and decisions, and automatically executes them by sending targeted emails and messages to team members. No manual follow-up needed.

**Primary Value:** Turn meeting recordings into automatic follow-up actions.

**Time to Ship:** 4 hours (MVP)  
**Target Users:** Product teams, engineering teams, project managers, founders

---

## Problem Statement

### Current State
- Meetings happen → action items are discussed verbally
- Someone *should* send follow-ups → nobody does
- Decisions get lost → team doesn't know what they committed to
- No audit trail of who said what
- Follow-up emails are manual, repetitive, error-prone

### Consequences
- Missed deadlines (nobody knew they committed)
- Duplicated work (people do the same thing)
- Dropped action items (no accountability)
- Time wasted re-explaining decisions

---

## Solution Overview

**Meeting Agent** automates the entire follow-up process:

1. **Upload Google Meet recording** (MP4 or provide meeting URL)
2. **Vapi transcribes** the audio to text
3. **Claude AI extracts:**
   - Action items ("ship API by Friday")
   - Owner assignments ("Sarah owns this")
   - Deadlines ("by Friday")
   - Context ("because customer needs it")
4. **Agent automatically sends emails** to assigned people
5. **Publishes cited.md** with full transcript + actions
6. **Dashboard** shows action status (pending, done, overdue)

---

## Product Features

### Core Features (MVP)

#### 1. Google Meet Upload
- [ ] Upload MP4 file from Google Meet export
- [ ] Or paste Google Meet recording URL
- [ ] File size limit: 100MB
- [ ] Supported formats: MP4, WAV, WebM

#### 2. Audio Transcription (Vapi)
- [ ] Real-time transcription via Vapi
- [ ] Speaker identification (if available)
- [ ] Timestamp for each action item
- [ ] Confidence scores for transcription

#### 3. Action Extraction (Claude)
- [ ] Extract action items from transcript
- [ ] Identify owners/assignees
- [ ] Extract deadlines
- [ ] Extract context/reasoning
- [ ] Output: Structured JSON with actions

**Example extracted actions:**
```json
[
  {
    "action": "Ship authentication API",
    "owner": "Sarah",
    "deadline": "2026-04-25",
    "context": "Required for customer launch",
    "transcript_timestamp": "0:05:30"
  },
  {
    "action": "Database migration testing",
    "owner": "Jane",
    "deadline": "2026-04-26",
    "context": "Before API ships",
    "transcript_timestamp": "0:12:45"
  }
]
```

#### 4. Auto-Send Emails
- [ ] Generate personalized email per action
- [ ] Include deadline
- [ ] Link to meeting transcript
- [ ] "React ✅ when complete" button
- [ ] Send via Gmail/SendGrid
- [ ] Track delivery status

**Example email:**
```
Subject: Action from Meeting — Auth API Due Friday

Hi Sarah,

Per our meeting today, you're shipping the authentication API by Friday, April 25.

This is needed for the customer launch.

Please reply ✅ when complete.

Meeting transcript: [link to cited.md]
```

#### 5. Cited.md Report
- [ ] Full meeting transcript
- [ ] Extracted action items
- [ ] Who is assigned what
- [ ] Deadlines
- [ ] Context/reasoning for each action
- [ ] Status (pending/done/overdue)

**Example format:**
```markdown
# Meeting Notes — Product Roadmap Review
**Date:** April 24, 2026  
**Duration:** 23 minutes  
**Attendees:** Sarah, Jane, PM, Designer

## Transcript
[Full transcript with timestamps]

## Actions Extracted

| Action | Owner | Deadline | Status | Context |
|--------|-------|----------|--------|---------|
| Ship auth API | Sarah | 2026-04-25 | Pending | Customer launch blocker |
| DB migration test | Jane | 2026-04-26 | Pending | Before API ships |
| Design mockups | Designer | 2026-04-27 | Pending | For new dashboard |

## Email Sent To
- sarah@company.com ✅ (2026-04-24 14:30)
- jane@company.com ✅ (2026-04-24 14:30)
- designer@company.com ✅ (2026-04-24 14:30)
```

#### 6. Dashboard
- [ ] Upload meeting recording form
- [ ] Processing status (transcribing → extracting → sending)
- [ ] List of extracted actions
- [ ] Email delivery status
- [ ] Link to cited.md
- [ ] Meeting history (past uploads)

#### 7. Redis Caching
- [ ] Cache transcripts (avoid re-processing)
- [ ] Store action items in Redis
- [ ] Track email send status
- [ ] Session memory across requests

#### 8. WunderGraph Federation (Concept)
- [ ] Schema to federate:
  - Meeting data
  - Action items
  - Email delivery status
  - Team member APIs (optional)
- [ ] Single GraphQL query for all data

---

## User Stories

### User 1: Product Manager
> "As a PM, I want to run a meeting, upload the recording, and automatically send action items to my team so I don't have to send follow-up emails."

**Acceptance Criteria:**
- [ ] Upload Google Meet recording (MP4)
- [ ] Receive email of extracted actions within 2 min
- [ ] Team members get personalized emails with their actions
- [ ] Cited.md shows full transcript + actions

### User 2: Engineer (Action Owner)
> "As an engineer, I want to receive an email telling me what I committed to in the meeting, so I don't forget."

**Acceptance Criteria:**
- [ ] Email includes clear deadline
- [ ] Email includes context (why this is important)
- [ ] Easy to mark as "done"
- [ ] Can link back to meeting transcript

### User 3: Founder (Accountability)
> "As a founder, I want a record of what everyone committed to, so I can track progress."

**Acceptance Criteria:**
- [ ] Cited.md has full transcript + all actions
- [ ] Can see who is assigned what
- [ ] Can see deadlines
- [ ] Can track status (done/overdue)

---

## Success Metrics

### Launch Metrics (Demo)
- [ ] Agent successfully transcribes 2-min meeting
- [ ] Extracts 3-5 action items correctly
- [ ] Sends emails to team members
- [ ] Publishes cited.md
- [ ] Dashboard shows full flow

### MVP Metrics (Working Product)
- [ ] Transcription accuracy: 95%+
- [ ] Action extraction accuracy: 90%+
- [ ] Email delivery: 100%
- [ ] Processing time: <2 min for 30-min meeting
- [ ] Zero false positive actions

---

## Technical Architecture

### Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| **Frontend** | Next.js 15 (App Router) | Upload, dashboard, status tracking |
| **Backend** | Next.js API routes | Process recordings, coordinate agents |
| **Transcription** | Vapi SDK | Audio → Text |
| **AI** | Claude API (Opus) | Extract action items |
| **Email** | SendGrid / Gmail API | Send follow-ups |
| **Caching** | Redis | Store transcripts, sessions |
| **Storage** | Temp file system | Store recording during processing |
| **Output** | Markdown file | Publish cited.md |
| **API Federation** | WunderGraph (concept) | GraphQL schema |

### Data Flow

```
┌─────────────────────────────────────┐
│ Frontend (Next.js)                  │
│ ├─ Upload Google Meet recording     │
│ ├─ Show processing status           │
│ └─ Display actions + cited.md       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Backend (Next.js API Route)         │
│ ├─ Receive file upload              │
│ └─ Coordinate orchestration         │
└──────────────┬──────────────────────┘
               ↓
        ┌──────┴──────┐
        ↓             ↓
   ┌─────────┐   ┌──────────┐
   │  Vapi   │   │ Claude   │
   │Transcribe│  │ Extract  │
   └────┬────┘   └────┬─────┘
        └──────┬──────┘
               ↓
        ┌────────────┐
        │  Redis     │
        │  Cache     │
        └──────┬─────┘
               ↓
        ┌────────────┐
        │ SendGrid   │
        │ Send emails│
        └──────┬─────┘
               ↓
        ┌────────────┐
        │ cited.md   │
        │ Publish    │
        └────────────┘
```

### API Endpoints

```
POST /api/upload
  - Upload Google Meet recording
  - Returns: job_id

GET /api/status/:job_id
  - Check processing status
  - Returns: {status, progress, actions, emails_sent}

GET /api/actions/:job_id
  - Get extracted actions
  - Returns: JSON array of actions

GET /api/cited/:job_id
  - Get cited.md content
  - Returns: Markdown text

POST /api/mark-done
  - Mark action as complete
  - Returns: updated status
```

---

## User Flows

### Flow 1: Happy Path (Upload → Auto-Execute)
```
1. PM uploads Google Meet recording (MP4)
   ↓
2. Agent shows: "Processing... (0%)"
   ↓
3. Vapi transcribes audio
   ↓
4. Claude extracts: "Sarah → API by Friday", "Jane → DB test"
   ↓
5. Emails sent automatically to Sarah + Jane
   ↓
6. Dashboard shows:
   ✅ Sarah - Auth API (Due 2026-04-25)
   ✅ Jane - DB Test (Due 2026-04-26)
   ↓
7. cited.md published with full transcript
```

### Flow 2: View History
```
1. PM opens dashboard
   ↓
2. Sees list of past meetings
   ↓
3. Clicks meeting → see actions + cited.md
   ↓
4. Can mark actions as done
```

---

## Frontend Design (Claude Style)

### Pages

#### 1. `/` — Upload & Status
```
┌─────────────────────────────────────┐
│  Meeting Agent                 🚀   │
├─────────────────────────────────────┤
│                                     │
│  📹 Upload Google Meet Recording    │
│                                     │
│  [Choose File] or [Paste URL]       │
│                                     │
│  └─ meeting.mp4 (2.3 MB)            │
│                                     │
│  ┌─────────────────────────────────┐│
│  │  Processing... 45%               ││
│  │  📝 Transcribing...              ││
│  │  🤖 Extracting actions...        ││
│  │  ✉️  Sending emails...           ││
│  └─────────────────────────────────┘│
│                                     │
└─────────────────────────────────────┘
```

#### 2. `/meeting/[id]` — Actions & Results
```
┌─────────────────────────────────────┐
│  Meeting: Product Roadmap Review    │
│  April 24, 2026 • 23 min            │
├─────────────────────────────────────┤
│                                     │
│  ✅ Actions Extracted (3)            │
│                                     │
│  1. Auth API Ship                   │
│     👤 Sarah                         │
│     📅 Due Apr 25                    │
│     ⏳ Pending                       │
│                                     │
│  2. DB Migration Test               │
│     👤 Jane                          │
│     📅 Due Apr 26                    │
│     ⏳ Pending                       │
│                                     │
│  3. Design Mockups                  │
│     👤 Designer                      │
│     📅 Due Apr 27                    │
│     ⏳ Pending                       │
│                                     │
│  [View cited.md] [Resend Emails]    │
│                                     │
└─────────────────────────────────────┘
```

#### 3. `/meeting/[id]/transcript` — Full Transcript
```
┌─────────────────────────────────────┐
│  Meeting Transcript                 │
├─────────────────────────────────────┤
│                                     │
│  [00:00] PM: "Let's review Q2 plan" │
│                                     │
│  [00:15] Sarah: "I can ship API by" │
│          "Friday if we have auth"   │
│                                     │
│  [00:45] Jane: "I'll test the DB"   │
│          "migration by Thursday"    │
│                                     │
│  [01:30] Designer: "Mockups ready"  │
│          "by next Wednesday"        │
│                                     │
│  [📄 Download as PDF]               │
│                                     │
└─────────────────────────────────────┘
```

### UI Elements (Claude Style)
- **Clean, minimal sidebar** with meeting history
- **Real-time status updates** with checkmarks
- **Large, readable action cards**
- **Email delivery indicators** (✅ sent, ⏳ pending)
- **One-click actions** (resend, mark done, download)
- **Monospace font** for transcript/code
- **Dark mode by default**

---

## Out of Scope (MVP)

- ❌ Multi-language transcription (Phase 2)
- ❌ Speaker diarization (Phase 2)
- ❌ Sentiment analysis (Phase 2)
- ❌ Slack integration (Phase 2, email is primary)
- ❌ Calendar integration (Phase 3)
- ❌ Jira/task management sync (Phase 3)
- ❌ Custom email templates (Phase 2)
- ❌ Action reminders (Phase 2)

---

## Timeline (4-Hour Sprint)

| Phase | Time | Task | Owner |
|-------|------|------|-------|
| **Setup** | 0-0.5h | API keys, project structure | Team |
| **Frontend** | 0.5-1.5h | Next.js upload form + dashboard | Dev 1 |
| **Transcription** | 1-2h | Vapi integration + audio processing | Dev 2 |
| **Extraction** | 2-3h | Claude API for action extraction | Dev 2 |
| **Email** | 3-3.5h | SendGrid integration + send emails | Dev 1 |
| **Cited.md** | 3-3.5h | Generate markdown report | Dev 2 |
| **Polish & Demo** | 3.5-4h | Test, UI polish, demo script | Team |

---

## Demo (3 Minutes)

### Demo Script
```
[0:00-0:30]
"Every meeting produces action items that get lost. 
We built an agent that listens to the recording 
and automatically sends follow-up emails."

[0:30-1:00]
UPLOAD MEETING
"I'm uploading a 2-minute Google Meet recording 
of our product roadmap meeting."

[1:00-1:30]
SHOW EXTRACTION
"The agent extracted 3 action items:
  ✓ Sarah → Ship auth API (Friday)
  ✓ Jane → DB migration test (Thursday)
  ✓ Designer → Mockups (Wednesday)

These emails were sent automatically."

[1:30-2:00]
SHOW CITED.MD
"Full transcript + actions published to cited.md
 — everything grounded in what was actually discussed."

[2:00-2:30]
TOOL SHOWCASE
"4 sponsor tools working together:
  ✓ Vapi (transcription)
  ✓ Claude (extraction)
  ✓ Redis (caching)
  ✓ WunderGraph (API federation concept)"

[2:30-3:00]
CLOSE
"Meeting Agent turns recordings into automatic follow-ups. 
No manual emails. Just action."
```

---

## Success Criteria for Hackathon

✅ **Must Have (MVP):**
- [ ] Upload Google Meet recording (MP4)
- [ ] Vapi transcribes audio
- [ ] Claude extracts 3+ action items
- [ ] SendGrid sends emails to team
- [ ] Generate cited.md
- [ ] Dashboard shows actions
- [ ] Working 3-min demo

✅ **Should Have (High Impact):**
- [ ] Next.js frontend with Claude style
- [ ] Real-time status updates
- [ ] View full transcript
- [ ] Email delivery tracking
- [ ] Redis caching

✅ **Nice to Have:**
- [ ] Speaker identification
- [ ] Resend emails button
- [ ] Mark actions as done
- [ ] WunderGraph schema

---

## Judging Criteria Alignment

| Criteria | How We Win |
|----------|-----------|
| **Autonomy** | Agent listens to recording → extracts → sends emails (no manual steps) |
| **Idea** | Real problem: follow-ups are lost. Real solution: automate them |
| **Technical Implementation** | Clean pipeline: Vapi → Claude → SendGrid → cited.md |
| **Tool Use** | 4+ sponsor tools (Vapi, Claude, Redis, WunderGraph) |
| **Demo** | Upload recording → watch emails send → show cited.md |

---

## Approval & Sign-Off

| Role | Sign-Off |
|------|----------|
| Product | ☐ |
| Engineering | ☐ |
| Design | ☐ |

---

**Status: READY TO BUILD**

Next step: Start Hour 0 — API key setup + project init
