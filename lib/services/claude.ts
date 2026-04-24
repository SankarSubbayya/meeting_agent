import { Anthropic } from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export interface ActionItem {
  id: string;
  action: string;
  owner: string;
  ownerEmail?: string;
  deadline: string;
  context: string;
  timestamp: string;
  status: 'pending' | 'done';
}

export async function extractActions(transcript: string): Promise<ActionItem[]> {
  try {
    const prompt = `You are a meeting transcription expert. Extract action items from this meeting transcript.

For each action item, identify:
1. The specific task/action
2. Who is responsible (owner)
3. Deadline (if mentioned)
4. Context/reason why
5. Approximate timestamp in the transcript

Return a JSON array of actions. Example format:
[
  {
    "action": "Ship authentication API",
    "owner": "Sarah",
    "deadline": "Friday",
    "context": "Required for customer launch",
    "timestamp": "0:15"
  }
]

TRANSCRIPT:
${transcript}

Return ONLY valid JSON array, no additional text.`;

    const message = await client.messages.create({
      model: 'claude-opus-4-1-20250805',
      max_tokens: 2000,
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
    });

    const content = message.content[0];
    if (content.type !== 'text') {
      throw new Error('Unexpected response type');
    }

    // Parse JSON response
    let actions = JSON.parse(content.text);

    // Transform to ActionItem format
    actions = actions.map((action: any, idx: number) => ({
      id: `action_${idx + 1}`,
      action: action.action,
      owner: action.owner,
      deadline: action.deadline || 'No deadline',
      context: action.context || '',
      timestamp: action.timestamp || '',
      status: 'pending' as const,
    }));

    console.log(`[Claude] Extracted ${actions.length} action items`);
    return actions;
  } catch (error) {
    console.error('Action extraction error:', error);
    throw new Error('Failed to extract actions');
  }
}
