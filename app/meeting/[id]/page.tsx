'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

interface MeetingData {
  jobId: string;
  title: string;
  summary: string;
  transcript: string;
  createdAt: string;
  actions: Array<{ id: string; action: string; owner: string; deadline: string; status: string }>;
  emails: Array<{ recipient: string; status: string }>;
}

export default function MeetingPage() {
  const params = useParams();
  const jobId = params.id as string;
  const [data, setData] = useState<MeetingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMeeting = async () => {
      try {
        setLoading(true);

        // Use GraphQL endpoint (WunderGraph)
        const response = await fetch('/api/graphql', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: `query GetMeeting($jobId: String!) {
              meeting(jobId: $jobId) {
                jobId
                title
                status
                summary
                transcript
                actions {
                  id
                  action
                  owner
                  deadline
                  status
                }
                emails {
                  recipient
                  status
                }
                createdAt
              }
            }`,
            variables: { jobId }
          })
        });

        const result = await response.json();
        if (result.data?.meeting) {
          setData(result.data.meeting);
        } else if (result.errors) {
          throw new Error(result.errors[0]?.message || 'Failed to fetch meeting');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        console.error('Error fetching meeting:', err);
      } finally {
        setLoading(false);
      }
    };

    if (jobId) {
      fetchMeeting();
    }
  }, [jobId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 font-sans p-6 md:p-12 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-slate-600">Processing meeting...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-50 font-sans p-6 md:p-12 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">Error: {error || 'No data found'}</p>
          <button onClick={() => window.history.back()} className="text-blue-600 hover:text-blue-700">
            ← Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white font-sans">
      {/* Header */}
      <div className="border-b border-slate-200 bg-white sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <button onClick={() => window.history.back()} className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors flex items-center gap-2">
            ← Back
          </button>
          <button className="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors">
            Export .md
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Title Section */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">{data.title}</h1>
          <p className="text-slate-500">ID: {jobId} • Processed autonomously</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">

          {/* LEFT COLUMN: Summary & Transcript */}
          <div className="lg:col-span-2 space-y-8">

            {/* Executive Summary */}
            <div>
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Executive Summary</h2>
              <p className="text-slate-600 leading-relaxed">
                {data.summary}
              </p>
            </div>

            {/* Transcript */}
            <div>
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Transcript</h2>
              <div className="bg-slate-50 rounded-lg p-6 max-h-96 overflow-y-auto border border-slate-200">
                <pre className="text-sm text-slate-600 whitespace-pre-wrap break-words font-sans leading-relaxed">
                  {data.transcript}
                </pre>
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN: Action Items & Emails */}
          <div className="space-y-8">

            {/* Action Items */}
            <div>
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Action Items</h2>
              <div className="space-y-3">
                {data.actions.map(action => (
                  <div key={action.id} className="border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <p className="font-medium text-slate-900 text-sm mb-3">{action.action}</p>
                    <div className="space-y-2 text-xs text-slate-600">
                      <div className="flex items-center gap-2">
                        <span className="text-slate-400">Assigned to:</span>
                        <span className="font-medium text-slate-900">{action.owner}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-slate-400">Due:</span>
                        <span className="font-medium text-slate-900">{action.deadline}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Notifications Sent */}
            <div>
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Notifications</h2>
              <div className="space-y-2">
                {data.emails.map((email, i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                    <span className="text-sm text-slate-700 truncate">{email.recipient}</span>
                    <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded">
                      Sent
                    </span>
                  </div>
                ))}
              </div>
            </div>

          </div>

        </div>
      </div>
    </div>
  );
}
// Markdown Generator goes down here, OUTSIDE the main component
function generateCitedMD(data: MeetingData): string {
  return `# Meeting Summary
**Date:** ${new Date(data.createdAt).toLocaleDateString()}
**Meeting ID:** ${data.jobId}

## Actions Extracted
${data.actions.map((a) => `- [ ] **${a.action}**\n  - Owner: ${a.owner}\n  - Deadline: ${a.deadline}`).join('\n\n')}

## Emails Dispatched
${data.emails.map((r) => `- ${r.recipient}: ${r.status}`).join('\n')}

## Raw Transcript
${data.transcript}

---
Generated autonomously by ExecuAI
`;
}
