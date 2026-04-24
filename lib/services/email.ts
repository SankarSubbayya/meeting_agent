import sgMail from '@sendgrid/mail';
import { ActionItem } from './claude';

sgMail.setApiKey(process.env.SENDGRID_API_KEY || '');

interface EmailResult {
  recipient: string;
  status: 'sent' | 'failed';
  message?: string;
}

export async function sendActionEmails(
  actions: ActionItem[],
  meetingId: string
): Promise<EmailResult[]> {
  const results: EmailResult[] = [];

  // Group actions by owner
  const actionsByOwner = actions.reduce(
    (acc, action) => {
      if (!acc[action.owner]) {
        acc[action.owner] = [];
      }
      acc[action.owner].push(action);
      return acc;
    },
    {} as Record<string, ActionItem[]>
  );

  // Send email to each owner
  for (const [owner, ownerActions] of Object.entries(actionsByOwner)) {
    try {
      // For demo: extract email from owner name
      const email = generateEmail(owner);

      const actionsList = ownerActions
        .map(
          (a) =>
            `• ${a.action}
  Deadline: ${a.deadline}
  Context: ${a.context}`
        )
        .join('\n\n');

      const htmlContent = `
<h2>Action Items from Meeting</h2>
<p>Hi ${owner},</p>
<p>Per our meeting, here are your action items:</p>
<pre>${actionsList}</pre>
<p>
  <a href="${process.env.NEXT_PUBLIC_API_URL}/meeting/${meetingId}">
    View full transcript & meeting notes
  </a>
</p>
<p>Please reply with ✅ when complete.</p>
`;

      await sgMail.send({
        to: email,
        from: 'meeting-agent@example.com',
        subject: `Action Items from Meeting`,
        html: htmlContent,
      });

      results.push({
        recipient: email,
        status: 'sent',
      });

      console.log(`[Email] Sent to ${email}`);
    } catch (error) {
      console.error(`[Email] Failed to send to ${owner}:`, error);
      results.push({
        recipient: owner,
        status: 'failed',
        message: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  return results;
}

function generateEmail(name: string): string {
  // Simple email generation from name (for demo)
  // In production, you'd have a proper team directory
  const email = name
    .toLowerCase()
    .replace(/\s+/g, '.')
    .replace(/[^a-z.]/g, '');
  return `${email}@company.com`;
}
