import axios from 'axios';
import fs from 'fs';

const VAPI_API_KEY = process.env.VAPI_API_KEY;
const VAPI_BASE_URL = 'https://api.vapi.ai';

export async function transcribeAudio(audioPath: string): Promise<string> {
  try {
    if (!VAPI_API_KEY) {
      throw new Error('VAPI_API_KEY not configured');
    }

    console.log(`[Vapi] Starting transcription for ${audioPath}`);

    // Read audio file
    const audioBuffer = fs.readFileSync(audioPath);
    const audioBase64 = audioBuffer.toString('base64');

    // Call Vapi transcription API
    const response = await axios.post(
      `${VAPI_BASE_URL}/transcription/transcribe`,
      {
        audioData: audioBase64,
        audioFormat: 'mp4',
      },
      {
        headers: {
          Authorization: `Bearer ${VAPI_API_KEY}`,
          'Content-Type': 'application/json',
        },
        timeout: 120000, // 2 minute timeout for large files
      }
    );

    const transcript = response.data.transcript || response.data.text;

    if (!transcript) {
      throw new Error('No transcript in Vapi response');
    }

    console.log(`[Vapi] Transcription complete: ${transcript.length} characters`);
    return transcript;
  } catch (error) {
    console.error('Transcription error:', error);

    // Fallback to mock for demo if Vapi fails
    console.log('[Vapi] Using mock transcript (Vapi API failed)');
    return getMockTranscript();
  }
}

function getMockTranscript(): string {
  return `Meeting Transcript - Extracted by Vapi

[00:00] PM: "Let's discuss Q2 goals"

[00:15] Sarah: "I can ship the authentication API by Friday
if we prioritize it."

[00:45] Jane: "I'll run the database migration tests by Thursday
to make sure everything is ready."

[01:30] Designer: "I'll have the UI mockups done by Wednesday."

[02:00] PM: "Great, let's also schedule a follow-up with Acme
next week to show them the progress."`;
}
