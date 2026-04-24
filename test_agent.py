#!/usr/bin/env python3
"""
Unit and Integration Tests for Meeting Agent
"""

import json
import pytest
from agent import (
    transcribe_audio,
    extract_action_items,
    send_emails,
    process_tool_call,
)


class TestUnit:
    """Unit tests for individual agent tools"""

    def test_transcribe_audio_returns_string(self):
        """Test transcription returns a non-empty string"""
        result = transcribe_audio("test.mp4")
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Meeting Transcript" in result

    def test_transcribe_audio_contains_speakers(self):
        """Test transcript contains expected speaker names"""
        result = transcribe_audio("test.mp4")
        assert "Sarah" in result
        assert "Jane" in result
        assert "Designer" in result
        assert "PM" in result

    def test_extract_action_items_returns_json(self):
        """Test action extraction returns valid JSON"""
        transcript = "Sarah will ship the auth API by Friday"
        result = extract_action_items(transcript)
        assert isinstance(result, str)
        actions = json.loads(result)
        assert isinstance(actions, list)
        assert len(actions) > 0

    def test_extract_action_items_structure(self):
        """Test extracted actions have required fields"""
        transcript = "Sarah will ship the auth API by Friday"
        result = extract_action_items(transcript)
        actions = json.loads(result)

        for action in actions:
            assert "id" in action
            assert "action" in action
            assert "owner" in action
            assert "deadline" in action
            assert "context" in action

    def test_send_emails_success(self):
        """Test email sending with valid actions"""
        actions = json.dumps([
            {
                "id": "action_1",
                "action": "Ship API",
                "owner": "Sarah",
                "deadline": "Friday",
                "context": "Test"
            }
        ])
        result = send_emails(actions, "test_meeting_001")
        result_data = json.loads(result)

        assert "meeting_id" in result_data
        assert result_data["meeting_id"] == "test_meeting_001"
        assert "total_sent" in result_data
        assert result_data["total_sent"] == 1

    def test_send_emails_multiple_recipients(self):
        """Test email sending with multiple action items"""
        actions = json.dumps([
            {
                "id": "action_1",
                "action": "Task 1",
                "owner": "Sarah",
                "deadline": "Friday",
                "context": "Test"
            },
            {
                "id": "action_2",
                "action": "Task 2",
                "owner": "Jane",
                "deadline": "Thursday",
                "context": "Test"
            }
        ])
        result = send_emails(actions, "test_meeting_002")
        result_data = json.loads(result)

        assert result_data["total_sent"] == 2
        assert len(result_data["results"]) == 2

    def test_send_emails_invalid_json(self):
        """Test email sending handles invalid JSON"""
        result = send_emails("invalid json", "test_meeting_003")
        result_data = json.loads(result)
        assert "error" in result_data

    def test_process_tool_call_transcribe(self):
        """Test tool dispatcher for transcribe"""
        result = process_tool_call("transcribe_audio", {"audio_file": "test.mp4"})
        assert "Meeting Transcript" in result

    def test_process_tool_call_extract(self):
        """Test tool dispatcher for extraction"""
        result = process_tool_call(
            "extract_action_items",
            {"transcript": "Sarah will ship the API"}
        )
        data = json.loads(result)
        assert isinstance(data, list)

    def test_process_tool_call_email(self):
        """Test tool dispatcher for email"""
        actions = json.dumps([{
            "id": "action_1",
            "action": "Test",
            "owner": "Sarah",
            "deadline": "Friday",
            "context": "Test"
        }])
        result = process_tool_call(
            "send_emails",
            {"actions": actions, "meeting_id": "test"}
        )
        data = json.loads(result)
        assert "total_sent" in data

    def test_process_tool_call_unknown_tool(self):
        """Test tool dispatcher with unknown tool"""
        result = process_tool_call("unknown_tool", {})
        data = json.loads(result)
        assert "error" in data
        assert "Unknown tool" in data["error"]


class TestIntegration:
    """Integration tests for full pipeline"""

    def test_full_pipeline_flow(self):
        """Test complete meeting processing pipeline"""
        # Step 1: Transcribe
        transcript = transcribe_audio("meeting.mp4")
        assert transcript
        assert "Meeting Transcript" in transcript

        # Step 2: Extract actions
        actions_json = extract_action_items(transcript)
        actions = json.loads(actions_json)
        assert len(actions) > 0
        assert all("id" in a for a in actions)
        assert all("owner" in a for a in actions)

        # Step 3: Send emails
        email_result = send_emails(actions_json, "meeting_001")
        email_data = json.loads(email_result)
        assert email_data["total_sent"] == len(actions)

    def test_action_owner_email_mapping(self):
        """Test that action owners map to correct email addresses"""
        actions = json.dumps([
            {"id": "1", "action": "Task", "owner": "Sarah", "deadline": "Fri", "context": ""},
            {"id": "2", "action": "Task", "owner": "Jane", "deadline": "Thu", "context": ""},
        ])
        result = send_emails(actions, "test_001")
        data = json.loads(result)

        emails = [r["to"] for r in data["results"]]
        assert "sarah@company.com" in emails
        assert "jane@company.com" in emails

    def test_end_to_end_with_mock_meeting(self):
        """Test complete flow with realistic meeting data"""
        # Simulate the exact flow the agent would take
        meeting_id = "e2e_test_001"

        # Step 1: Get transcript
        transcript = transcribe_audio("meeting.mp4")

        # Step 2: Extract actions from transcript
        actions_str = extract_action_items(transcript)
        actions = json.loads(actions_str)

        # Verify we have real actions
        assert len(actions) >= 6
        assert any(a["owner"] == "Sarah" for a in actions)
        assert any(a["owner"] == "Jane" for a in actions)

        # Step 3: Send emails
        email_result = send_emails(actions_str, meeting_id)
        email_data = json.loads(email_result)

        # Verify all actions were emailed
        assert email_data["total_sent"] == len(actions)
        assert email_data["meeting_id"] == meeting_id

        # Verify each action has results
        for result in email_data["results"]:
            assert "to" in result
            assert "@company.com" in result["to"]
            assert result["status"] == "sent"

    def test_data_consistency_across_pipeline(self):
        """Test that data is preserved and consistent through pipeline"""
        meeting_id = "consistency_test"

        # Get original transcript
        transcript = transcribe_audio("test.mp4")
        original_length = len(transcript)

        # Extract actions
        actions_str = extract_action_items(transcript)
        actions = json.loads(actions_str)
        action_count = len(actions)

        # Send emails
        email_result = send_emails(actions_str, meeting_id)
        email_data = json.loads(email_result)

        # Verify counts match through pipeline
        assert email_data["total_sent"] == action_count
        # Verify transcript was used (not lost)
        assert original_length > 0

    def test_multiple_sequential_meetings(self):
        """Test processing multiple meetings sequentially"""
        meeting_ids = ["meeting_1", "meeting_2", "meeting_3"]
        results = []

        for meeting_id in meeting_ids:
            # Full pipeline for each meeting
            transcript = transcribe_audio(f"{meeting_id}.mp4")
            actions_str = extract_action_items(transcript)
            email_result = send_emails(actions_str, meeting_id)
            email_data = json.loads(email_result)

            results.append(email_data)

        # Verify all meetings processed
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result["meeting_id"] == meeting_ids[i]
            assert result["total_sent"] > 0


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_extract_with_empty_transcript(self):
        """Test extraction with empty transcript"""
        result = extract_action_items("")
        data = json.loads(result)
        # Should still return valid JSON (might be empty or mock data)
        assert isinstance(data, list)

    def test_send_emails_with_empty_actions(self):
        """Test email sending with empty action list"""
        result = send_emails("[]", "test_empty")
        data = json.loads(result)
        assert data["total_sent"] == 0

    def test_send_emails_malformed_json(self):
        """Test email sending with malformed JSON"""
        result = send_emails("{invalid}", "test")
        data = json.loads(result)
        assert "error" in data

    def test_special_characters_in_action(self):
        """Test handling special characters in action items"""
        actions = json.dumps([{
            "id": "1",
            "action": "Review \"security patch\" & update docs",
            "owner": "Sarah O'Brien",
            "deadline": "Friday",
            "context": "Test (urgent)"
        }])
        result = send_emails(actions, "test_special")
        data = json.loads(result)
        assert data["total_sent"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
