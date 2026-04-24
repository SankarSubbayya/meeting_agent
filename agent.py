#!/usr/bin/env python3
"""
Meeting Agent - Autonomous agent using Claude + tool_use
Processes meeting recordings: transcribe → extract actions → send emails
"""

import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")

client = Anthropic(api_key=api_key)
MODEL_ID = "claude-opus-4-7"

# Define tools for the agent
tools = [
    {
        "name": "transcribe_audio",
        "description": "Transcribe audio from a meeting recording",
        "input_schema": {
            "type": "object",
            "properties": {
                "audio_file": {
                    "type": "string",
                    "description": "Path to the audio file or meeting ID"
                }
            },
            "required": ["audio_file"]
        }
    },
    {
        "name": "extract_action_items",
        "description": "Extract action items from meeting transcript",
        "input_schema": {
            "type": "object",
            "properties": {
                "transcript": {
                    "type": "string",
                    "description": "Meeting transcript text"
                }
            },
            "required": ["transcript"]
        }
    },
    {
        "name": "send_emails",
        "description": "Send action items to responsible parties via email",
        "input_schema": {
            "type": "object",
            "properties": {
                "actions": {
                    "type": "string",
                    "description": "JSON string of action items to send"
                },
                "meeting_id": {
                    "type": "string",
                    "description": "Meeting ID for reference"
                }
            },
            "required": ["actions", "meeting_id"]
        }
    }
]

def transcribe_audio(audio_file: str) -> str:
    """Mock transcription - in production, calls Vapi or other service"""
    mock_transcript = """Meeting Transcript - Q2 Goals Planning

[00:00] PM: "Let's discuss Q2 goals and priorities"

[00:15] Sarah: "I can ship the authentication API by Friday if we prioritize it."

[00:45] Jane: "I'll run the database migration tests by Thursday to make sure everything is ready."

[01:30] Designer: "I'll have the UI mockups done by Wednesday."

[02:00] PM: "Great, let's also schedule a follow-up with Acme next week to show them the progress."

[02:30] Sarah: "I can prepare a demo of the new features."

[03:00] Jane: "I'll document the migration steps by Monday."
"""
    print(f"[Tool] Transcribing {audio_file}...")
    return mock_transcript

def extract_action_items(transcript: str) -> str:
    """Mock extraction - in production, calls Claude API"""
    actions = [
        {
            "id": "action_1",
            "action": "Ship authentication API",
            "owner": "Sarah",
            "deadline": "Friday",
            "context": "Q2 priority - requires prioritization"
        },
        {
            "id": "action_2",
            "action": "Run database migration tests",
            "owner": "Jane",
            "deadline": "Thursday",
            "context": "Ensure everything is ready for deployment"
        },
        {
            "id": "action_3",
            "action": "Complete UI mockups",
            "owner": "Designer",
            "deadline": "Wednesday",
            "context": "Needed for development to begin"
        },
        {
            "id": "action_4",
            "action": "Schedule follow-up with Acme",
            "owner": "PM",
            "deadline": "Next week",
            "context": "Show progress on new features"
        },
        {
            "id": "action_5",
            "action": "Prepare demo of new features",
            "owner": "Sarah",
            "deadline": "Friday",
            "context": "For Acme follow-up meeting"
        },
        {
            "id": "action_6",
            "action": "Document migration steps",
            "owner": "Jane",
            "deadline": "Monday",
            "context": "For team reference and deployment"
        }
    ]
    print(f"[Tool] Extracted {len(actions)} action items")
    return json.dumps(actions)

def send_emails(actions: str, meeting_id: str) -> str:
    """Send action items via email using SendGrid API"""
    try:
        actions_data = json.loads(actions)
        email_results = []
        sendgrid_key = os.getenv("SENDGRID_API_KEY")

        if sendgrid_key:
            # Use real SendGrid API
            sg = SendGridAPIClient(sendgrid_key)
            for action in actions_data:
                owner = action.get("owner", "unknown")
                recipient_email = f"{owner.lower()}@company.com"

                try:
                    mail = Mail(
                        from_email="noreply@execuai.com",
                        to_emails=recipient_email,
                        subject=f"Action Item: {action.get('action')}",
                        html_content=f"""
                        <h3>{action.get('action')}</h3>
                        <p><strong>Deadline:</strong> {action.get('deadline')}</p>
                        <p><strong>Meeting ID:</strong> {meeting_id}</p>
                        """
                    )
                    response = sg.send(mail)
                    email_results.append({
                        "to": recipient_email,
                        "status": "sent" if response.status_code == 202 else "failed",
                        "action_id": action.get("id"),
                        "action": action.get("action"),
                        "response_code": response.status_code
                    })
                    print(f"[SendGrid] Email sent to {recipient_email} (code: {response.status_code})")
                except Exception as e:
                    email_results.append({
                        "to": recipient_email,
                        "status": "failed",
                        "action_id": action.get("id"),
                        "action": action.get("action"),
                        "error": str(e)
                    })
                    print(f"[SendGrid] Failed to send email to {recipient_email}: {e}")
        else:
            # Fallback to mock if no API key
            for action in actions_data:
                owner = action.get("owner", "unknown")
                email_results.append({
                    "to": f"{owner.lower()}@company.com",
                    "status": "sent (mock)",
                    "action_id": action.get("id"),
                    "action": action.get("action")
                })
            print("[Tool] Using mock email sending (no SENDGRID_API_KEY)")

        print(f"[Tool] Processed {len(email_results)} action items for email")
        return json.dumps({
            "meeting_id": meeting_id,
            "total_sent": len(email_results),
            "results": email_results
        })
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON for actions"})

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """Execute tool based on agent request"""
    if tool_name == "transcribe_audio":
        return transcribe_audio(tool_input["audio_file"])
    elif tool_name == "extract_action_items":
        return extract_action_items(tool_input["transcript"])
    elif tool_name == "send_emails":
        return send_emails(tool_input["actions"], tool_input["meeting_id"])
    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

def run_meeting_agent(meeting_file: str, meeting_id: str = "meeting_001"):
    """Run the autonomous meeting agent"""
    print(f"\n🤖 Starting Meeting Agent for {meeting_file}")
    print("=" * 50)

    messages = [
        {
            "role": "user",
            "content": f"""Process this meeting recording and extract action items:

Meeting file: {meeting_file}
Meeting ID: {meeting_id}

Please:
1. Transcribe the audio
2. Extract action items from the transcript
3. Send the action items to team members via email

Think through each step and use the available tools."""
        }
    ]

    # Agent loop
    while True:
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        print(f"\n[Agent] Stop reason: {response.stop_reason}")

        # Process response content
        for block in response.content:
            if hasattr(block, 'text'):
                print(f"\n[Agent Reasoning]:\n{block.text}")
            elif block.type == "tool_use":
                print(f"\n[Agent] Using tool: {block.name}")
                print(f"Input: {json.dumps(block.input, indent=2)}")

        # Check if we're done
        if response.stop_reason == "end_turn":
            print("\n✅ Agent completed processing")
            break

        # Process tool calls
        if response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    tool_result = process_tool_call(block.name, block.input)
                    print(f"[Tool Result]: {tool_result[:200]}...")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": tool_result
                    })

            # Add assistant response and tool results to messages
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            # No more tool calls
            break

    print("\n" + "=" * 50)
    print("🎉 Meeting processing complete!")

if __name__ == "__main__":
    # Run the agent
    run_meeting_agent("sample_meeting.mp4")
