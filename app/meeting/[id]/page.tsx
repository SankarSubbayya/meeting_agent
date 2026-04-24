'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

interface ActionItem {
  id: string;
  action: string;
  owner: string;
  deadline: string;
  status: 'pending' | 'done';
}

interface MeetingData {
  jobId: string;
  transcript: string;
  actions: ActionItem[];
  emailResults: Array<{ recipient: string; status: string }>;
  createdAt: string;
}

export default function MeetingPage() {
  const params = useParams();
  const jobId = params.id as string;
  const [data, setData] = useState<MeetingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/api/meeting/${jobId}`);
        if (!response.ok) throw new Error('Failed to fetch meeting data');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [jobId]);

  if (loading) {
    return (
      <div className="space-y-8">
        <h2 className="text-2xl font-bold">Processing Meeting...</h2>
        <div className="space-y-2">
          <div className="h-4 bg-slate-700 rounded animate-pulse"></div>
          <div className="h-4 bg-slate-700 rounded animate-pulse w-5/6"></div>
          <div className="h-4 bg-slate-700 rounded animate-pulse w-4/6"></div>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="bg-red-900/20 border border-red-700 rounded-lg p-6">
        <p className="text-red-400">Error: {error || 'Failed to load meeting'}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h2 className="text-3xl font-bold">Meeting Results</h2>
        <p className="text-slate-400">
          Meeting ID: <code className="text-cyan-400">{jobId.slice(0, 8)}...</code>
        </p>
      </div>

      {/* Actions */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-cyan-400">
          ✅ Extracted Actions ({data.actions.length})
        </h3>
        <div className="space-y-3">
          {data.actions.map((action) => (
            <div
              key={action.id}
              className="bg-slate-900 border border-slate-700 rounded-lg p-4"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <p className="text-white font-medium">{action.action}</p>
                  <div className="flex gap-4 mt-2 text-sm text-slate-400">
                    <span>👤 {action.owner}</span>
                    <span>📅 {action.deadline}</span>
                  </div>
                </div>
                <div className={`text-sm font-medium ${
                  action.status === 'done' ? 'text-green-400' : 'text-yellow-400'
                }`}>
                  {action.status === 'done' ? '✅ Done' : '⏳ Pending'}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Email Status */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-green-400">
          ✉️ Emails Sent ({data.emailResults.length})
        </h3>
        <div className="space-y-2">
          {data.emailResults.map((result, idx) => (
            <div key={idx} className="flex items-center justify-between bg-slate-900 border border-slate-700 rounded px-4 py-3">
              <span className="text-slate-300">{result.recipient}</span>
              <span className={result.status === 'sent' ? 'text-green-400' : 'text-red-400'}>
                {result.status === 'sent' ? '✅ Sent' : '❌ Failed'}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Transcript */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-cyan-400">📝 Full Transcript</h3>
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-6 max-h-96 overflow-y-auto">
          <pre className="text-sm text-slate-300 whitespace-pre-wrap break-words">
            {data.transcript}
          </pre>
        </div>
      </div>

      {/* Download */}
      <div className="flex gap-4">
        <button
          onClick={() => {
            const element = document.createElement('a');
            element.setAttribute('href', `data:text/plain;charset=utf-8,${encodeURIComponent(generateCitedMD(data))}`);
            element.setAttribute('download', `meeting-${jobId}.md`);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
          }}
          className="bg-cyan-600 hover:bg-cyan-500 text-white px-6 py-2 rounded font-medium"
        >
          📄 Download cited.md
        </button>
        <button
          onClick={() => window.history.back()}
          className="bg-slate-700 hover:bg-slate-600 text-white px-6 py-2 rounded font-medium"
        >
          ← Back
        </button>
      </div>
    </div>
  );
}

function generateCitedMD(data: MeetingData): string {
  return `# Meeting Summary
**Date:** ${new Date(data.createdAt).toLocaleDateString()}
**Meeting ID:** ${data.jobId}

## Transcript
${data.transcript}

## Actions Extracted
${data.actions
  .map(
    (a) => `- [ ] **${a.action}**
  - Owner: ${a.owner}
  - Deadline: ${a.deadline}
  - Status: ${a.status}`
  )
  .join('\n\n')}

## Emails Sent
${data.emailResults.map((r) => `- ${r.recipient}: ${r.status}`).join('\n')}

---
Generated by Meeting Agent • Ship to Production 2026
`;
}
