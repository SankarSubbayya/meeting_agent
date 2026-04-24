'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');

      const { jobId } = await response.json();
      router.push(`/meeting/${jobId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="space-y-4">
        <h2 className="text-4xl font-bold">
          <span className="text-cyan-400">Meetings</span> → <span className="text-green-400">Actions</span>
        </h2>
        <p className="text-slate-400 max-w-2xl">
          Upload a Google Meet recording. The agent listens, extracts action items,
          and automatically sends emails to your team. No manual follow-ups needed.
        </p>
      </div>

      {/* Upload Form */}
      <div className="bg-slate-900 border border-slate-700 rounded-lg p-8 max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* File Input */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-300">
              📹 Google Meet Recording (MP4, WAV, WebM)
            </label>
            <input
              type="file"
              accept="video/mp4,audio/wav,video/webm,.mp4,.wav,.webm"
              onChange={handleFileChange}
              disabled={loading}
              className="w-full"
            />
            {file && (
              <p className="text-sm text-slate-400">
                Selected: <span className="text-cyan-400">{file.name}</span> (
                {(file.size / 1024 / 1024).toFixed(2)} MB)
              </p>
            )}
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-900/20 border border-red-700 rounded p-3">
              <p className="text-red-400 text-sm">⚠️ {error}</p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!file || loading}
            className="w-full bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-700 text-white py-3 rounded font-medium transition-colors"
          >
            {loading ? (
              <span className="inline-flex items-center gap-2">
                <span className="animate-spin">⟳</span>
                Processing...
              </span>
            ) : (
              '🚀 Upload & Process'
            )}
          </button>
        </form>
      </div>

      {/* Info */}
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div className="bg-slate-900/50 border border-slate-700 rounded p-4">
          <p className="text-cyan-400 font-medium">🎙️ Transcription</p>
          <p className="text-slate-400 mt-2">Vapi listens & transcribes</p>
        </div>
        <div className="bg-slate-900/50 border border-slate-700 rounded p-4">
          <p className="text-green-400 font-medium">🤖 Extraction</p>
          <p className="text-slate-400 mt-2">Claude finds action items</p>
        </div>
        <div className="bg-slate-900/50 border border-slate-700 rounded p-4">
          <p className="text-yellow-400 font-medium">✉️ Execution</p>
          <p className="text-slate-400 mt-2">SendGrid sends emails</p>
        </div>
      </div>
    </div>
  );
}
