# 🤖 Meeting Agent - Autonomous Meeting Processing

An autonomous Python agent that processes meeting recordings and extracts action items using Claude's tool-use capabilities.

## How It Works

The agent autonomously:
1. **Transcribes** the meeting audio
2. **Extracts** action items with owners and deadlines
3. **Sends emails** to team members with their assignments

The agent uses Claude's reasoning to orchestrate each step, making intelligent decisions about the workflow.

## Quick Start

### 1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Up API Key
Make sure `ANTHROPIC_API_KEY` is in your `.env` file:
```bash
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

### 3. Run the Agent
```bash
source venv/bin/activate
python3 agent.py
```

## Features

✅ **Autonomous Decision Making** - Claude decides workflow steps  
✅ **Tool Use** - Transcription, extraction, email sending  
✅ **Structured Output** - JSON action items with owner/deadline  
✅ **Agent Reasoning** - Shows Claude's thought process  
✅ **Mock Services** - No external API setup needed for demo  

## Example Output

```
🤖 Starting Meeting Agent for sample_meeting.mp4
==================================================

[Agent] Stop reason: tool_use
[Agent Reasoning]: I'll process this meeting recording step by step...

[Agent] Using tool: transcribe_audio
[Agent] Using tool: extract_action_items  
[Agent] Using tool: send_emails

✅ Meeting processing complete! (6 action items extracted, 6 emails sent)
```

## Integration with Next.js

To integrate with the existing Next.js app:

1. Call this agent from `/api/upload` endpoint after file is saved
2. Agent processes and caches results in Redis
3. Frontend polls `/api/status/[jobId]` for progress

## Real Integration (Post-Hackathon)

Replace mock functions with:
- **transcribe_audio**: Call Vapi API
- **extract_action_items**: Call Claude API with transcript
- **send_emails**: Call SendGrid API

See `agent.py` lines 70-130 for mock implementations.
