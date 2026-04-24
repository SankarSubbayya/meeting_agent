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
    <div className="min-h-screen bg-slate-50 font-sans p-6 md:p-12">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Navigation & Header */}
        <div>
          <button onClick={() => window.history.back()} className="text-sm font-medium text-slate-500 hover:text-blue-600 mb-4 flex items-center gap-1">
            ← Back to Workspace
          </button>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-serif font-semibold text-slate-900">{data.title}</h1>
              <p className="text-slate-500 text-sm mt-1">Briefing ID: {jobId} • Processed autonomously</p>
            </div>
            <button className="bg-white border border-slate-200 text-slate-700 px-4 py-2 rounded-lg text-sm font-medium shadow-sm hover:bg-slate-50 transition-colors">
              Export cited.md
            </button>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          
          {/* LEFT COLUMN: The Context (Summary & Transcript) */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* AI Summary */}
            <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
              <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-3 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-600"></span> Executive Summary
              </h2>
              <p className="text-slate-600 text-sm leading-relaxed">
                {data.summary}
              </p>
            </div>

            {/* Raw Transcript */}
            <div className="bg-white border border-slate-200 rounded-xl flex flex-col shadow-sm h-[500px]">
              <div className="p-4 border-b border-slate-100 bg-slate-50/50 rounded-t-xl">
                <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Raw Transcript</h2>
              </div>
              <div className="p-6 overflow-y-auto flex-1 bg-slate-50/30">
                <pre className="text-sm text-slate-600 whitespace-pre-wrap break-words font-sans leading-relaxed">
                  {data.transcript}
                </pre>
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN: The Agent Execution Log */}
          <div className="space-y-6">
            <div className="bg-slate-900 rounded-xl shadow-lg border border-slate-800 overflow-hidden flex flex-col h-full">
              
              <div className="p-5 border-b border-slate-800 bg-slate-950/50">
                <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> 
                  Agent Execution Log
                </h2>
                <p className="text-slate-400 text-xs mt-1">Actions taken based on briefing context</p>
              </div>

              <div className="p-5 space-y-6 flex-1 overflow-y-auto">
                
                {/* Extracted Tasks */}
                <div>
                  <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Tasks Assigned</h3>
                  <div className="space-y-3">
                    {data.actions.map(action => (
                      <div key={action.id} className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-3">
                        <p className="text-sm text-white font-medium mb-2">{action.action}</p>
                        <div className="flex justify-between items-center text-xs">
                          <span className="text-slate-400">👤 {action.owner}</span>
                          <span className="text-slate-400">📅 {action.deadline}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Email Dispatch */}
                <div>
                  <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Communications Dispatched</h3>
                  <div className="space-y-2">
                    {data.emails.map((email, i) => (
                      <div key={i} className="flex justify-between items-center bg-slate-800/50 border border-slate-700/50 rounded-lg p-3">
                        <span className="text-xs text-slate-300 truncate mr-2">{email.recipient}</span>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
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
