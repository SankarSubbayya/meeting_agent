import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Meeting Agent',
  description: 'Autonomous agent that listens to meetings and executes actions',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 font-mono">
        <div className="min-h-screen flex flex-col">
          {/* Header */}
          <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur">
            <div className="max-w-6xl mx-auto px-6 py-4">
              <div className="flex items-center justify-between">
                <h1 className="text-xl font-bold">
                  <span className="text-cyan-400">Meeting</span> Agent
                </h1>
                <div className="text-sm text-slate-400">
                  Autonomous action execution
                </div>
              </div>
            </div>
          </header>

          {/* Main */}
          <main className="flex-1">
            <div className="max-w-6xl mx-auto px-6 py-8">
              {children}
            </div>
          </main>

          {/* Footer */}
          <footer className="border-t border-slate-800 bg-slate-900/50 mt-16">
            <div className="max-w-6xl mx-auto px-6 py-4 text-sm text-slate-400">
              Context Engineering Challenge • Ship to Production 2026
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
