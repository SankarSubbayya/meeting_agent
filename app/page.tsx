'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface Briefing {
  jobId: string;
  title: string;
  createdAt: string;
  actions: Array<{ id: string }>;
  status: string;
}

export default function Home() {
  const router = useRouter();
  const [recentBriefings, setRecentBriefings] = useState<Briefing[]>([]);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    fetchMeetings();
  }, []);

  const fetchMeetings = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/meetings');
      if (response.ok) {
        const meetings = await response.json();
        setRecentBriefings(meetings);
      }
    } catch (err) {
      console.error('Error fetching meetings:', err);
    }
  };

  const handleUpload = async (file: File) => {
    try {
      setUploading(true);
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const result = await response.json();
      router.push(`/meeting/${result.jobId}`);
    } catch (err) {
      console.error('Error uploading file:', err);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleUpload(e.target.files[0]);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 font-sans">
      
      {/* SIDEBAR */}
      <aside className="w-64 shrink-0 border-r border-slate-200 bg-white p-6 hidden md:flex flex-col">
        <div className="mb-10 flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded bg-blue-600 text-white shadow-sm">
            <span className="text-sm font-serif font-bold">E</span> {/* <-- Changed M to E */}
          </div>
          <div>
            <p className="text-sm font-bold text-slate-900">ExecuAI</p> {/* <-- Changed here */}
            <p className="text-[10px] uppercase tracking-widest text-slate-500">Workspace</p>
          </div>
        </div>
        {/* ... rest of sidebar ... */}

        <nav className="space-y-1">
          {['Recent Briefings', 'Action Hub', 'Team Integrations'].map((item, i) => (
            <button
              key={item}
              className={`w-full rounded-md px-3 py-2 text-left text-sm font-medium transition-colors ${i === 0 ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}
            >
              {item}
            </button>
          ))}
        </nav>
      </aside>

      {/* MAIN STAGE */}
      <main className="flex-1 h-full overflow-y-auto p-8 lg:p-12">
        <div className="max-w-5xl mx-auto">
          
          <div className="flex justify-between items-end mb-8">
            <div>
              <h1 className="text-3xl font-serif font-semibold text-slate-900 mb-2">Recent Briefings</h1>
              <p className="text-slate-500 text-sm">Review meeting contexts and autonomous agent executions.</p>
            </div>
            <label className="bg-blue-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium shadow-sm hover:bg-blue-700 transition-colors cursor-pointer">
              + {uploading ? 'Uploading...' : 'New Live Session'}
              <input type="file" onChange={handleFileInput} className="hidden" accept="audio/*,video/*" disabled={uploading} />
            </label>
          </div>

          {/* Drag and Drop Upload Area */}
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-xl p-8 text-center mb-8 transition-colors ${
              dragActive ? 'border-blue-500 bg-blue-50' : 'border-slate-300 bg-slate-50'
            }`}
          >
            <p className="text-slate-600 text-sm">
              Drag meeting recording here or click "New Live Session" to upload
            </p>
          </div>

          {/* LIST OF RECORDINGS */}
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
            <div className="grid grid-cols-12 gap-4 p-4 border-b border-slate-100 bg-slate-50/50 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <div className="col-span-6">Briefing Name</div>
              <div className="col-span-3">Date</div>
              <div className="col-span-3 text-right">Agent Status</div>
            </div>
            
            <div className="divide-y divide-slate-100">
              {recentBriefings.length === 0 ? (
                <div className="p-8 text-center text-slate-500">
                  <p>No briefings yet. Upload a meeting recording to get started.</p>
                </div>
              ) : (
                recentBriefings.map((briefing) => (
                  <Link href={`/meeting/${briefing.jobId}`} key={briefing.jobId} className="grid grid-cols-12 gap-4 p-4 items-center hover:bg-slate-50 transition-colors group cursor-pointer">
                    <div className="col-span-6">
                      <p className="font-medium text-slate-900 group-hover:text-blue-600 transition-colors">{briefing.title}</p>
                      <p className="text-xs text-slate-500 mt-0.5">{briefing.actions?.length || 0} autonomous actions identified</p>
                    </div>
                    <div className="col-span-3 text-sm text-slate-600">
                      {new Date(briefing.createdAt).toLocaleDateString()}
                    </div>
                    <div className="col-span-3 flex justify-end">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${briefing.status === 'completed' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-amber-50 text-amber-700 border-amber-200'}`}>
                        {briefing.status === 'completed' ? 'Executed' : 'Processing'}
                      </span>
                    </div>
                  </Link>
                ))
              )}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}