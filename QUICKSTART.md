# 🚀 Quick Start - Meeting Agent Demo

Get the demo running in 2 minutes.

## Prerequisites

- Python 3.8+
- `ANTHROPIC_API_KEY` in `.env` file

## Setup (One-Time)

```bash
# 1. Navigate to project
cd /Users/sankar/hackathons/meeting_agent

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify API key
echo $ANTHROPIC_API_KEY
# Should display your key (not empty)
```

## Run Demo (One Command)

```bash
./run_demo.sh
```

This will:
1. ✅ Run autonomous agent (processes meeting)
2. ✅ Run test suite (20 tests)
3. ✅ Show code coverage (57%)

**Total time: ~2 minutes**

---

## Individual Commands

### Run Just the Agent
```bash
source venv/bin/activate
python3 agent.py
```

**Output:**
- Shows agent reasoning
- Transcribes meeting
- Extracts 6 action items
- Sends emails to team
- Provides summary

### Run Just Tests
```bash
source venv/bin/activate
pytest test_agent.py -v
```

**Output:**
- 20 tests all passing
- Execution time: 0.2s

### Run Tests with Coverage
```bash
source venv/bin/activate
pytest test_agent.py --cov=agent --cov-report=term-missing
```

**Output:**
- Code coverage: 57%
- Missing lines identified

---

## What You'll See

### Agent Output
```
🤖 Starting Meeting Agent for sample_meeting.mp4
==================================================

[Agent Reasoning]:
I'll process this meeting recording step by step...

[Agent] Using tool: transcribe_audio
[Tool Result]: Meeting Transcript - Q2 Goals Planning...

[Agent] Using tool: extract_action_items
[Tool Result]: [{"id": "action_1", "action": "Ship API"...}]

[Agent] Using tool: send_emails
[Tool Result]: {"meeting_id": "meeting_001", "total_sent": 6...}

✅ Meeting processing complete for meeting_001

### 📋 Action Items Extracted (6 total)
| # | Owner | Action | Deadline |
|---|-------|--------|----------|
| 1 | Sarah | Ship authentication API | Friday |
| 2 | Jane | Run database migration tests | Thursday |
...

🎉 Meeting processing complete!
```

### Test Output
```
============================== test session starts ==============================
test_agent.py::TestUnit::test_transcribe_audio_returns_string PASSED     [  5%]
test_agent.py::TestUnit::test_transcribe_audio_contains_speakers PASSED  [ 10%]
...
test_agent.py::TestErrorHandling::test_special_characters_in_action PASSED [100%]

============================== 20 passed in 0.23s ==============================
```

---

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# If empty, set it
export ANTHROPIC_API_KEY="your-key-here"

# Or add to .env
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

### "venv: command not found"
```bash
# Try python3 -m venv instead
python3 -m venv venv
```

### "Module not found"
```bash
# Reinstall requirements
source venv/bin/activate
pip install -r requirements.txt
```

### "Tests fail"
```bash
# Run single test to debug
pytest test_agent.py::TestUnit::test_transcribe_audio_returns_string -v
```

---

## Architecture

```
User Request
    ↓
Python Agent (agent.py)
    ↓
Claude + Tool-Use
    ├─→ Tool 1: transcribe_audio()
    ├─→ Tool 2: extract_action_items()
    └─→ Tool 3: send_emails()
    ↓
Results + Reasoning
```

---

## Demo Script Contents

**run_demo.sh** runs three commands in sequence:

```bash
# 1. Run agent
python3 agent.py

# 2. Run tests
pytest test_agent.py -v --tb=short

# 3. Show coverage
pytest test_agent.py --cov=agent --cov-report=term-missing
```

---

## File Structure

```
meeting_agent/
├── agent.py              # Autonomous agent (main demo)
├── test_agent.py         # Test suite (20 tests)
├── requirements.txt      # Dependencies
├── run_demo.sh          # Demo script (one command)
├── QUICKSTART.md        # This file
├── DEMO.md              # Detailed demo guide
├── AGENT_README.md      # Agent documentation
└── TEST_SUMMARY.md      # Test coverage details
```

---

## What's Happening

1. **Agent receives**: "Process meeting and extract actions"
2. **Claude analyzes**: "I need to transcribe, then extract, then email"
3. **Claude executes**: Calls tools in intelligent sequence
4. **Claude explains**: Shows reasoning for each decision
5. **Agent completes**: Returns structured results

---

## Key Takeaways

✅ **Autonomous** - Claude makes intelligent decisions  
✅ **Tested** - 20 tests all passing  
✅ **Transparent** - Shows reasoning at each step  
✅ **Scalable** - Handles multiple meetings  
✅ **Production-Ready** - Just swap mock services for real APIs  

---

## Next Steps

Post-hackathon:
1. Replace mock services with real Vapi, SendGrid, Claude APIs
2. Add specialized agents (Fireflies, Summarizer, Gmail, Notion, etc.)
3. Integrate with Next.js frontend
4. Add database persistence
5. Scale to handle 100+ meetings

---

**Ready to demo?** Run `./run_demo.sh`
