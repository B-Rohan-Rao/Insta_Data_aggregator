"use client";

import { MockAnalytics } from "../mock/analytics";

interface AnalyticsCardProps {
  analytics: MockAnalytics;
}

export default function AnalyticsCard({ analytics }: AnalyticsCardProps) {
  const formatNumber = (num: number): string => {
    return Math.round(num).toLocaleString();
  };

  const metrics = [
    {
      label: "Average Likes",
      value: formatNumber(analytics.avg_likes),
      description: "Average likes per post",
      color: "border-l-indigo-500",
    },
    {
      label: "Average Comments",
      value: formatNumber(analytics.avg_comments),
      description: "Average comments per post",
      color: "border-l-purple-500",
    },
    {
      label: "Posting Frequency",
      value: `${analytics.posting_frequency_days.toFixed(1)} Days`,
      description: "Avg days between posts",
      color: "border-l-cyan-500",
    },
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
    <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
      <h3 className="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
        <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6a7.5 7.5 0 107.5 7.5h-7.5V6z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0013.5 3v7.5z" />
        </svg>
        Performance Analytics
      </h3>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
        {metrics.map((item, idx) => (
          <div
            key={idx}
            className={`border-l-4 p-4 rounded-r-xl bg-slate-50 border-y border-r border-slate-100 flex flex-col justify-between ${item.color}`}
          >
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{item.label}</p>
              <h4 className="text-xl font-black text-slate-900 mt-1">{item.value}</h4>
            </div>
            <p className="text-[10px] text-slate-400 mt-2 font-medium">{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
