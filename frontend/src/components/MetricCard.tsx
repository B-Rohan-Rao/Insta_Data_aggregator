"use client";

import { ReactNode } from "react";

interface MetricCardProps {
  value: string | number;
  label: string;
  trend: string;
  trendDirection: "up" | "down" | "neutral";
  iconType: "followers" | "engagement" | "likes" | "comments";
}

export default function MetricCard({ value, label, trend, trendDirection, iconType }: MetricCardProps) {
  const getIcon = () => {
    switch (iconType) {
      case "followers":
        return (
          <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        );
      case "engagement":
        return (
          <div className="p-3 bg-purple-50 text-purple-600 rounded-xl">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
        );
      case "likes":
        return (
          <div className="p-3 bg-rose-50 text-rose-600 rounded-xl">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
        );
      case "comments":
        return (
          <div className="p-3 bg-cyan-50 text-cyan-600 rounded-xl">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
        );
    }
  };

  const getTrendStyles = () => {
    switch (trendDirection) {
      case "up":
        return "bg-green-50 text-green-700 border-green-100";
      case "down":
        return "bg-red-50 text-red-700 border-red-100";
      case "neutral":
      default:
        return "bg-slate-50 text-slate-600 border-slate-100";
    }
  };

  return (
    <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm flex items-start justify-between">
      <div className="space-y-3">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{label}</p>
        <h3 className="text-2xl font-extrabold text-slate-900">{value}</h3>
        
        {/* Trend Indicator */}
        <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 border text-xs font-medium rounded-full ${getTrendStyles()}`}>
          {trendDirection === "up" && (
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" />
            </svg>
          )}
          {trendDirection === "down" && (
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 4.5l15 15m0 0V8.25m0 11.25H8.25" />
            </svg>
          )}
          <span>{trend}</span>
        </div>
      </div>
      
      {getIcon()}
    </div>
  );
}
