"use client";

import AnimatedNumber from "./AnimatedNumber";

interface LanguageCardProps {
  username: string;
}

export default function LanguageCard({ username }: LanguageCardProps) {
  // Return mock language distribution based on creator type
  const getLanguageDistribution = () => {
    const name = username.toLowerCase().trim();
    if (name.includes("virat") || name.includes("kohli")) {
      return { english: 68.5, hindi: 12.2, hinglish: 19.3 };
    }
    if (name.includes("shraddha") || name.includes("kapoor") || name.includes("adityasaidwhat") || name.includes("aditya")) {
      return { english: 44.8, hindi: 23.5, hinglish: 31.7 };
    }
    // default (e.g. carryminati / standard creator)
    return { english: 22.4, hindi: 35.8, hinglish: 41.8 };
  };

  const dist = getLanguageDistribution();

  const items = [
    { label: "Hinglish (Hindi in Latin script)", value: dist.hinglish, color: "bg-gradient-to-r from-indigo-400 to-indigo-500", bg: "bg-indigo-50" },
    { label: "English", value: dist.english, color: "bg-gradient-to-r from-purple-400 to-purple-500", bg: "bg-purple-50" },
    { label: "Hindi (Devanagari script)", value: dist.hindi, color: "bg-gradient-to-r from-cyan-400 to-cyan-500", bg: "bg-cyan-50" },
  ];

  return (
    <div className="shadow-neumorphic hover:shadow-neumorphic-hover transition-all duration-300 p-4 sm:p-5 flex flex-col justify-between h-full">
      <div>
        <h3 className="text-lg font-bold text-slate-900 mb-1.5 flex items-center gap-2">
          <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 21a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zm0 0a1.5 1.5 0 01-3 0m3 0h7.5m-9 0V3.75m0 2.25h9a1.5 1.5 0 011.5 1.5v11.25a1.5 1.5 0 01-1.5 1.5h-9" />
          </svg>
          Audience Language Distribution
        </h3>
        <p className="text-xs text-slate-400 mb-4">Language distribution estimated from audience comments.</p>
 
        <div className="space-y-4">
          {items.map((item, idx) => (
            <div key={idx} className="space-y-2">
              <div className="flex items-center justify-between text-sm font-semibold">
                <span className="text-slate-700">{item.label}</span>
                <span className="text-slate-900">
                  <AnimatedNumber value={item.value.toFixed(1) + "%"} />
                </span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
                <div
                  className={`h-full rounded-full ${item.color} transition-all duration-1000 ease-out`}
                  style={{ width: `${item.value}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-slate-50 text-[10px] text-slate-400 leading-normal flex items-start gap-1.5">
        <svg className="w-4 h-4 text-slate-300 flex-shrink-0" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>Analysis scans comments section for Devanagari character ranges and romanized Hindi/Urdu keywords.</span>
      </div>
    </div>
  );
}
