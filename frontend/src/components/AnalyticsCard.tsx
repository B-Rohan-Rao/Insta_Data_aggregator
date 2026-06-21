"use client";

import { MockAnalytics } from "../mock/analytics";
import AnimatedNumber from "./AnimatedNumber";

interface AnalyticsCardProps {
  analytics: MockAnalytics;
}

export default function AnalyticsCard({ analytics }: AnalyticsCardProps) {
  const formatNumber = (num: number): string => {
    return Math.round(num).toLocaleString();
  };

  const metrics = [
    {
      label: "Posts Analyzed",
      value: analytics.total_posts_analyzed,
      description: "Sample volume size",
      color: "border-l-green-500",
    },
    {
      label: "Viral Posts",
      value: analytics.viral_posts.length,
      description: "Engagement > 3x median",
      color: "border-l-rose-500",
    },
    {
      label: "Collaboration Posts",
      value: analytics.collaboration_posts.length,
      description: "Identified sponsored/ad posts",
      color: "border-l-amber-500",
    },
  ];

  return (
    <div className="shadow-neumorphic hover:shadow-neumorphic-hover transition-all duration-300 p-4 sm:p-5">
      <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6a7.5 7.5 0 107.5 7.5h-7.5V6z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0013.5 3v7.5z" />
        </svg>
        Performance Analytics
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {metrics.map((item, idx) => (
          <div
            key={idx}
            className={`border-l-4 p-3 rounded-r-xl bg-slate-50 border-y border-r border-slate-100 flex flex-col justify-between ${item.color}`}
          >
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{item.label}</p>
              <h4 className="text-xl font-semibold text-slate-900 mt-0.5">
                <AnimatedNumber value={item.value} />
              </h4>
            </div>
            <p className="text-[10px] text-slate-400 mt-1 font-medium">{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
