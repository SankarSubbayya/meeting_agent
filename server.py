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
import redis
from agent import extract_action_items, send_emails, transcribe_audio

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

# Initialize Redis client
try:
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    r = redis.from_url(redis_url, decode_responses=True)
    # Test connection
    r.ping()
    print(f"✅ Redis connected: {redis_url}")
    USE_REDIS = True
except Exception as e:
    print(f"⚠️  Redis not available: {e}")
    print("   Falling back to in-memory storage")
    USE_REDIS = False
    meetings_db = {}

# Note: Tool implementations (transcribe_audio, extract_action_items, send_emails)
# are imported from agent.py to use real Claude API and SendGrid integration

async def run_agent(meeting_id: str, transcript: str):
    """Run agent to process meeting using Claude API"""
    try:
        # Extract action items from transcript (uses Claude API)
        actions_json_str = extract_action_items(transcript)
        actions = json.loads(actions_json_str)

        # Send emails for each action (uses real SendGrid API)
        emails_json_str = send_emails(json.dumps(actions), meeting_id)
        email_result = json.loads(emails_json_str)
        emails = email_result.get("results", [])

        # Generate summary
        summary = f"Extracted {len(actions)} action items from meeting"

        return {
            "transcript": transcript,
            "summary": summary,
            "actions": actions,
            "emails": emails
        }
    except Exception as e:
        print(f"Error running agent: {e}")
        return {
            "transcript": transcript,
            "summary": f"Error processing meeting: {str(e)}",
            "actions": [],
            "emails": [],
            "error": str(e)
        }

def save_meeting_to_db(job_id: str, meeting_data: dict):
    """Save meeting data to Redis or in-memory DB"""
    if USE_REDIS:
        try:
            # Set with 24-hour expiration (86400 seconds)
            r.setex(f"meeting:{job_id}", 86400, json.dumps(meeting_data))
            r.setex(f"meeting:{job_id}:status", 86400, meeting_data.get("status", "processing"))
            print(f"[Redis] Saved meeting {job_id}")
        except Exception as e:
            print(f"[Redis] Error saving: {e}")
            # Fallback to in-memory
            meetings_db[job_id] = meeting_data
    else:
        meetings_db[job_id] = meeting_data

def get_meeting_from_db(job_id: str):
    """Get meeting data from Redis or in-memory DB"""
    if USE_REDIS:
        try:
            data = r.get(f"meeting:{job_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"[Redis] Error getting: {e}")
            return meetings_db.get(job_id)
    else:
        return meetings_db.get(job_id)

def get_all_meetings_from_db():
    """Get all meetings from Redis or in-memory DB"""
    if USE_REDIS:
        try:
            keys = r.keys("meeting:*:status")
            meetings = []
            for key in keys:
                job_id = key.split(":")[1]
                meeting = r.get(f"meeting:{job_id}")
                if meeting:
                    meetings.append(json.loads(meeting))
            return meetings
        except Exception as e:
            print(f"[Redis] Error listing: {e}")
            return list(meetings_db.values())
    else:
        return list(meetings_db.values())

@app.post("/api/upload")
async def upload_meeting(file: UploadFile = File(...)):
    """Upload and process a meeting recording"""
    try:
        # Generate job ID
        job_id = str(uuid.uuid4())

        # Save file info
        filename = file.filename or "meeting.mp4"

        # Create initial meeting record
        meeting_record = {
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

        # Save initial state to Redis/DB
        save_meeting_to_db(job_id, meeting_record)

        # Process the meeting
        transcript = transcribe_audio(filename)
        actions = extract_action_items(transcript)
        emails = send_emails(actions, job_id)

        # Generate summary
        summary = f"The team discussed key deliverables. {len(actions)} action items were identified and assigned to team members."

        # Update meeting record
        meeting_record.update({
            "status": "completed",
            "transcript": transcript,
            "summary": summary,
            "actions": actions,
            "emails": emails
        })

        # Save final state to Redis/DB
        save_meeting_to_db(job_id, meeting_record)

        return JSONResponse({
            "jobId": job_id,
            "status": "processing"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Get processing status"""
    meeting = get_meeting_from_db(job_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return JSONResponse({
        "jobId": job_id,
        "status": meeting["status"],
        "progress": 100 if meeting["status"] == "completed" else 50
    })

@app.get("/api/meeting/{job_id}")
async def get_meeting(job_id: str):
    """Get meeting details and processed results"""
    meeting = get_meeting_from_db(job_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return JSONResponse(meeting)

@app.get("/api/meetings")
async def list_meetings():
    """List all processed meetings"""
    return JSONResponse(get_all_meetings_from_db())

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
