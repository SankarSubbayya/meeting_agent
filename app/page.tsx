import React from 'react';
import Link from 'next/link';

export default function Home() {
  // Filler data to make the dashboard look active and enterprise-ready
  const recentBriefings = [
    { id: '123', title: 'Q3 Product Roadmap Sync', date: 'Today, 10:00 AM', actions: 3, status: 'Executed' },
    { id: '124', title: 'Acme Corp: Technical Onboarding', date: 'Yesterday, 2:30 PM', actions: 5, status: 'Executed' },
    { id: '125', title: 'Weekly Engineering Standup', date: 'Apr 22, 9:00 AM', actions: 1, status: 'Pending Review' },
  ];

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
            <button className="bg-blue-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium shadow-sm hover:bg-blue-700 transition-colors">
              + New Live Session
            </button>
          </div>

          {/* LIST OF RECORDINGS */}
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
            <div className="grid grid-cols-12 gap-4 p-4 border-b border-slate-100 bg-slate-50/50 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <div className="col-span-6">Briefing Name</div>
              <div className="col-span-3">Date</div>
              <div className="col-span-3 text-right">Agent Status</div>
            </div>
            
            <div className="divide-y divide-slate-100">
              {recentBriefings.map((briefing) => (
                <Link href={`/meeting/${briefing.id}`} key={briefing.id} className="grid grid-cols-12 gap-4 p-4 items-center hover:bg-slate-50 transition-colors group cursor-pointer">
                  <div className="col-span-6">
                    <p className="font-medium text-slate-900 group-hover:text-blue-600 transition-colors">{briefing.title}</p>
                    <p className="text-xs text-slate-500 mt-0.5">{briefing.actions} autonomous actions identified</p>
                  </div>
                  <div className="col-span-3 text-sm text-slate-600">
                    {briefing.date}
                  </div>
                  <div className="col-span-3 flex justify-end">
                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${briefing.status === 'Executed' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-amber-50 text-amber-700 border-amber-200'}`}>
                      {briefing.status}
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}