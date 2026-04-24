#!/usr/bin/env python3
"""
FastAPI Backend for Meeting Agent
Integrates agent with Next.js frontend
"""

import json
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")

client = Anthropic(api_key=api_key)
MODEL_ID = "claude-opus-4-7"

# In-memory storage (for hackathon demo)
meetings_db = {}

# Tool implementations
def transcribe_audio(audio_file: str) -> str:
    """Mock transcription"""
    return """Meeting Transcript - Q3 Goals Planning

[00:00] PM: "Let's discuss Q3 goals and priorities"

[00:15] Sarah: "I can ship the authentication API by Friday if we prioritize it."

[00:45] Jane: "I'll run the database migration tests by Thursday to make sure everything is ready."

[01:30] Designer: "I'll have the UI mockups done by Wednesday."

[02:00] PM: "Great, let's also schedule a follow-up with Acme next week to show them the progress."

[02:30] Sarah: "I can prepare a demo of the new features."

[03:00] Jane: "I'll document the migration steps by Monday."
"""

def extract_action_items(transcript: str) -> list:
    """Mock extraction"""
    return [
        {
            "id": "action_1",
            "action": "Ship authentication API",
            "owner": "Sarah",
            "deadline": "Friday",
            "context": "Q3 priority - requires prioritization",
            "status": "pending"
        },
        {
            "id": "action_2",
            "action": "Run database migration tests",
            "owner": "Jane",
            "deadline": "Thursday",
            "context": "Ensure everything is ready for deployment",
            "status": "pending"
        },
        {
            "id": "action_3",
            "action": "Complete UI mockups",
            "owner": "Designer",
            "deadline": "Wednesday",
            "context": "Needed for development to begin",
            "status": "pending"
        },
        {
            "id": "action_4",
            "action": "Schedule follow-up with Acme",
            "owner": "PM",
            "deadline": "Next week",
            "context": "Show progress on new features",
            "status": "pending"
        },
        {
            "id": "action_5",
            "action": "Prepare demo of new features",
            "owner": "Sarah",
            "deadline": "Friday",
            "context": "For Acme follow-up meeting",
            "status": "pending"
        },
        {
            "id": "action_6",
            "action": "Document migration steps",
            "owner": "Jane",
            "deadline": "Monday",
            "context": "For team reference and deployment",
            "status": "pending"
        }
    ]

def send_emails(actions: list, meeting_id: str) -> list:
    """Mock email sending"""
    results = []
    for action in actions:
        owner = action.get("owner", "unknown")
        results.append({
            "recipient": f"{owner.lower().replace(' ', '.')}@company.com",
            "status": "sent"
        })
    return results

async def run_agent(meeting_id: str, transcript: str):
    """Run agent to process meeting"""
    messages = [
        {
            "role": "user",
            "content": f"""Process this meeting transcript and extract action items:

Meeting ID: {meeting_id}
Transcript: {transcript}

Use your tools to:
1. Confirm the transcript was received
2. Extract action items
3. Send emails to team members"""
        }
    ]

    # For demo, we'll use the mock implementations
    # In production, Claude would call real Vapi, etc.
    actions = extract_action_items(transcript)
    emails = send_emails(actions, meeting_id)

    return {
        "transcript": transcript,
        "actions": actions,
        "emails": emails
    }

@app.post("/api/upload")
async def upload_meeting(file: UploadFile = File(...)):
    """Upload and process a meeting recording"""
    try:
        # Generate job ID
        job_id = str(uuid.uuid4())

        # Save file info
        filename = file.filename or "meeting.mp4"

        # Create initial meeting record
        meetings_db[job_id] = {
            "jobId": job_id,
            "filename": filename,
            "status": "processing",
            "title": f"Meeting - {filename}",
            "transcript": "",
            "summary": "",
            "actions": [],
            "emails": [],
            "createdAt": str(__import__('datetime').datetime.now())
        }

        # Process the meeting
        transcript = transcribe_audio(filename)
        actions = extract_action_items(transcript)
        emails = send_emails(actions, job_id)

        # Generate summary
        summary = f"The team discussed key deliverables. {len(actions)} action items were identified and assigned to team members."

        # Update meeting record
        meetings_db[job_id].update({
            "status": "completed",
            "transcript": transcript,
            "summary": summary,
            "actions": actions,
            "emails": emails
        })

        return JSONResponse({
            "jobId": job_id,
            "status": "processing"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Get processing status"""
    if job_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")

    meeting = meetings_db[job_id]
    return JSONResponse({
        "jobId": job_id,
        "status": meeting["status"],
        "progress": 100 if meeting["status"] == "completed" else 50
    })

@app.get("/api/meeting/{job_id}")
async def get_meeting(job_id: str):
    """Get meeting details and processed results"""
    if job_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")

    meeting = meetings_db[job_id]
    return JSONResponse(meeting)

@app.get("/api/meetings")
async def list_meetings():
    """List all processed meetings"""
    return JSONResponse(list(meetings_db.values()))

@app.get("/health")
async def health():
    """Health check"""
    return JSONResponse({"status": "ok", "service": "meeting-agent"})

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Meeting Agent FastAPI Server")
    print("📍 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
