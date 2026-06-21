"use client";

import { MockAnalytics } from "../mock/analytics";

interface LanguageCardProps {
  analytics: MockAnalytics;
}

export default function LanguageCard({ analytics }: LanguageCardProps) {
  return (
    <div className="shadow-neumorphic hover:shadow-neumorphic-hover transition-all duration-300 p-4 sm:p-5 flex flex-col justify-between h-full">
      {/* Header — always fully visible */}
      <div>
        <h3 className="text-lg font-bold text-slate-900 mb-1.5 flex items-center gap-2">
          <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 21a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zm0 0a1.5 1.5 0 01-3 0m3 0h7.5m-9 0V3.75m0 2.25h9a1.5 1.5 0 011.5 1.5v11.25a1.5 1.5 0 01-1.5 1.5h-9" />
          </svg>
          Audience Language Distribution
          {/* Coming Soon badge */}
          <span className="ml-auto inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold tracking-wide bg-amber-100 text-amber-700 border border-amber-200">
            Coming Soon
          </span>
        </h3>

        {/* Blurred / dimmed content area */}
        <div className="relative mt-3">
          {/* Frosted overlay */}
          <div className="absolute inset-0 z-10 flex flex-col items-center justify-center text-center px-4 py-6">
            <div className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-indigo-50 mb-3">
              <svg className="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
              </svg>
            </div>
            <p className="text-[13px] font-semibold text-slate-700 leading-snug mb-1">
              This feature requires audience comment access from Instagram.
            </p>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              Instagram currently restricts comment access for many public profiles, so reliable audience language analysis is temporarily unavailable.
            </p>
            <span className="mt-3 inline-block px-3 py-1 rounded-full text-[10px] font-bold tracking-widest uppercase bg-indigo-50 text-indigo-500 border border-indigo-100">
              Coming Soon
            </span>
          </div>

          {/* Blurred background content */}
          <div className="blur-sm opacity-30 pointer-events-none select-none space-y-4 py-2">
            {[
              { label: "Hinglish (Hindi in Latin script)", value: 48, color: "bg-gradient-to-r from-indigo-400 to-indigo-500" },
              { label: "English", value: 35, color: "bg-gradient-to-r from-purple-400 to-purple-500" },
              { label: "Hindi (Devanagari script)", value: 17, color: "bg-gradient-to-r from-cyan-400 to-cyan-500" },
            ].map((item, idx) => (
              <div key={idx} className="space-y-2">
                <div className="flex items-center justify-between text-sm font-semibold">
                  <span className="text-slate-700">{item.label}</span>
                  <span className="text-slate-900">{item.value.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${item.color}`}
                    style={{ width: `${item.value}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-6 pt-4 border-t border-slate-50 text-[10px] text-slate-400 leading-normal flex items-start gap-1.5">
        <svg className="w-4 h-4 text-slate-300 flex-shrink-0" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>Analysis scans comments section for Devanagari character ranges and romanized Hindi/Urdu keywords.</span>
      </div>
    </div>
  );
}
