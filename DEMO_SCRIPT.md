# 🎬 Meeting Agent - 3-Minute Demo Script

**Total Runtime: 3:00 minutes**  
**Recording: Screen capture + voice-over**

---

## 📹 Recording Setup

**Before you start:**
1. Open http://localhost:3003 in browser
2. Have `transcript1.txt` ready to upload
3. Use screen recording tool (QuickTime on Mac, built-in on Windows)
4. Record at 1080p if possible
5. Enable microphone for voice-over

---

## 🎯 Demo Timeline

### **[0:00-0:30] Problem Statement (30 seconds)**

**VISUALS:** Show title slide or blank desktop  
**VOICEOVER (read naturally, conversational tone):**

```
"Every meeting produces action items that nobody remembers.

Email chains get lost. Tasks fall through the cracks. 
And nobody knows who actually committed to what.

We built Meeting Agent—an autonomous AI system that 
listens to meeting recordings and automatically extracts 
action items and sends emails to the team.

No manual follow-ups. No forgotten tasks. Just autonomous execution."
```

**ACTION:** 
- Show 3-second title: "Meeting Agent"
- Show problem statement text
- Transition to application

---

### **[0:30-1:00] Demo: Upload & Processing (30 seconds)**

**VISUALS:** Switch to http://localhost:3003  
**VOICEOVER:**

```
"Let me show you how it works. 

I'm going to upload a meeting recording."
```

**ACTIONS:**
1. **[0:30]** Show dashboard with "+ New Live Session" button
2. **[0:35]** Click "+ New Live Session" button
3. **[0:38]** Select `transcript1.txt` from file dialog
4. **[0:42]** Watch file upload
5. **[0:45]** Show loading spinner/processing state

**VOICEOVER (continue):**
```
"The system is now:
  🎙️ Reading the transcript
  🤖 Extracting action items with Claude AI
  ✉️ Sending emails with SendGrid
  💾 Caching everything in Redis"
```

**ACTIONS:**
6. **[0:55]** Wait for processing to complete (or show pre-recorded results)
7. **[1:00]** Results page loads automatically

---

### **[1:00-2:00] Results Page Tour (60 seconds)**

**PAGE:** Meeting results page at `/meeting/[jobId]`

**VOICEOVER:**
```
"Here's what the system extracted from the meeting:

The transcript shows that during a vendor sync meeting, 
Sam committed to sending an email to Ananta about 
compliance forms for the cloud storage migration.

Look at what the AI extracted:"
```

**ACTIONS:**
1. **[1:00-1:15]** Show meeting title and executive summary
   - Title: "Meeting - transcript1.txt"
   - Summary: Scroll to show summary text

2. **[1:15-1:30]** Scroll to Action Items section
   - Show extracted action items
   - Highlight: owner, deadline, action description

**VOICEOVER (continue):**
```
"The AI identified the key action: 
  ✓ Send email to Ananta 
  ✓ About compliance forms
  ✓ High priority
  ✓ Due Friday

And it automatically extracted the email address: 
anantaverma20@gmail.com"
```

3. **[1:30-1:45]** Show email notifications section
   - Show "anantaverma20@gmail.com: Sent ✓"
   - Show response code or delivery status

**VOICEOVER (continue):**
```
"The email has been sent. 

Ananta will receive a notification with the action item, 
the deadline, and full context from the meeting."
```

4. **[1:45-2:00]** Scroll down to show Raw Transcript
   - Show full meeting transcript
   - Point out where the email address appears: "[01:42] Sam: I will send an email to Ananta at anantaverma20@gmail.com"

**VOICEOVER (continue):**
```
"Here's the full transcript with timestamps. 
Everything is grounded in what was actually discussed."
```

---

### **[2:00-2:45] Technical Deep Dive (45 seconds)**

**VISUALS:** Switch to show architecture diagram or code

**VOICEOVER:**
```
"Meeting Agent integrates 7 sponsor tools that work together 
seamlessly:

1️⃣ Claude API (Anthropic)
   → Reads the transcript and extracts action items
   → Identifies owners and email addresses
   → Provides intelligent reasoning

2️⃣ SendGrid
   → Sends real emails to extracted addresses
   → Delivers notification with action details

3️⃣ Redis Cloud
   → Caches all data with 24-hour expiration
   → Persists information across sessions

4️⃣ WunderGraph
   → Provides a GraphQL API layer
   → Enables type-safe queries from frontend

5️⃣ FastAPI
   → Powers the backend REST API
   → Handles file uploads and processing

6️⃣ Next.js + React
   → Modern, responsive frontend
   → Professional dashboard interface

7️⃣ Pytest
   → 20 tests verify everything works
   → 57% code coverage
   → All tests passing ✅
"
```

**ACTIONS:**
1. **[2:00-2:15]** Show architecture diagram
   - Click or transition to show system diagram
   - Highlight: Frontend → Backend → Claude → SendGrid

2. **[2:15-2:30]** Show test results (optional)
   - Terminal screenshot showing: `20 passing, 57% coverage`

3. **[2:30-2:45]** Show code metrics
   - GitHub commits: 15+
   - Lines of code: ~2,500
   - Documentation: 8 files

---

### **[2:45-3:00] Closing & Impact (15 seconds)**

**VISUALS:** Back to dashboard or title screen  
**VOICEOVER:**

```
"Meeting Agent transforms how teams handle action items:

✅ Before: 30 minutes of manual work
   - Listen to recording
   - Write down action items
   - Send emails manually
   - Create task list

⚡ After: 2 minutes autonomous processing
   - Upload recording
   - System extracts and notifies
   - Automatic execution

This is the future of meeting management.

Meeting Agent. Autonomous. Intelligent. Productive."
```

**ACTIONS:**
1. Show end screen with project title
2. Show GitHub link: github.com/SankarSubbayya/meeting_agent
3. Show team credits

---

## 🎥 Recording Checklist

- [ ] System is running (backend + frontend)
- [ ] `transcript1.txt` is available for upload
- [ ] Screen resolution is 1080p or higher
- [ ] Audio is clear and at good volume
- [ ] No system notifications showing
- [ ] No console errors visible
- [ ] Microphone is working
- [ ] File is saved locally before uploading to any platform

---

## ⏱️ Timing Breakdown

| Section | Duration | Time |
|---------|----------|------|
| Problem Statement | 30s | 0:00-0:30 |
| Upload & Processing | 30s | 0:30-1:00 |
| Results Page Tour | 60s | 1:00-2:00 |
| Technical Deep Dive | 45s | 2:00-2:45 |
| Closing & Impact | 15s | 2:45-3:00 |
| **TOTAL** | **180s** | **3:00** |

---

## 📝 Script Notes

**Delivery Tips:**
- Speak clearly and naturally (not robotic)
- Maintain consistent pacing
- Pause slightly between sections
- Show enthusiasm about the product
- Make eye contact with camera (if on-screen)
- Avoid filler words ("um", "uh", "like")

**Visual Tips:**
- Use cursor highlights to point at UI elements
- Zoom in if text is too small
- Use smooth scrolling/transitions
- Minimize window chrome (hide taskbar, etc.)
- Show errors gracefully (if any occur)

**Audio Tips:**
- Record in quiet environment
- Use external microphone if possible
- Test audio levels before recording
- Add background music (optional, ~20% volume)
- Do multiple takes until happy with flow

---

## 🎬 How to Record

### **Mac (QuickTime)**
```bash
1. Open QuickTime Player
2. File → New Screen Recording
3. Click "Options" and select microphone
4. Click "Record" and select recording area
5. Demo the app
6. Stop recording (⌘+Ctrl+Esc)
7. Save as MP4
```

### **Windows (Built-in)**
```bash
1. Press Win + G to open Game Bar
2. Click record button (or Win + Alt + R)
3. Demo the app
4. Stop recording
5. Find file in Videos folder
```

### **Online Tool (Loom, Screenflow, etc.)**
```bash
1. Open Loom.com
2. Start recording
3. Select screen + microphone
4. Demo the app
5. Stop recording
6. Download MP4
```

---

## 📤 After Recording

1. **Review the video:**
   - Check timing is ~3:00 minutes
   - Check audio is clear
   - Check all visuals are visible
   - Watch full video once

2. **Edit (if needed):**
   - Trim intro/outro
   - Add title card (0-3 seconds)
   - Add subtitles (optional)
   - Normalize audio levels

3. **Export:**
   - Format: MP4 (H.264)
   - Resolution: 1080p (1920x1080)
   - Bitrate: 5-10 Mbps
   - Frame rate: 30fps

4. **Share:**
   - Upload to GitHub as release
   - Share in presentation
   - Add to README

---

## 🎯 Success Criteria

✅ Video is exactly 3:00 minutes (±5 seconds)  
✅ Problem is clearly explained  
✅ Demo shows upload → processing → results  
✅ All 7 sponsor tools are mentioned  
✅ Audio is clear and professional  
✅ Visuals are smooth and professional  
✅ Call-to-action is clear  
✅ No major errors or glitches  

---

## Alternative: Live Demo

If you prefer a live demo instead of pre-recorded:

1. **Setup (5 min before):**
   - Ensure both services running
   - Load dashboard in browser
   - Have transcript file ready
   - Test network connection

2. **During Presentation:**
   - Share screen with audience
   - Walk through steps naturally
   - Explain as you go
   - Be ready for questions

3. **Fallback:**
   - Have pre-recorded backup video
   - Have screenshots ready
   - Have notes written down

---

**Ready to record? Start with Problem Statement and follow the timeline above! 🎥**
