"use client";

import { useEffect, useState } from "react";

interface LoadingStateProps {
  username: string;
  onCancel?: () => void;
}

const STAGES = [
  "Fetching profile details...",
  "Scraping and analyzing recent posts...",
  "Calculating metrics and engagement...",
  "Generating creator intelligence insights..."
];

export default function LoadingState({ username, onCancel }: LoadingStateProps) {
  const [currentStage, setCurrentStage] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Increment loading stages
    const stageInterval = setInterval(() => {
      setCurrentStage((prev) => (prev < STAGES.length - 1 ? prev + 1 : prev));
    }, 950);

    // Smooth progress bar
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 1;
      });
    }, 38);

    return () => {
      clearInterval(stageInterval);
      clearInterval(progressInterval);
    };
  }, []);

  // SVG dimensions & math
  const radius = 56;
  const stroke = 6;
  const normalizedRadius = radius - stroke; // = 50
  const circumference = normalizedRadius * 2 * Math.PI; // = 314.16
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative flex flex-col items-center justify-center min-h-[60vh] w-full max-w-lg mx-auto text-center px-6 py-8">
      {/* Decorative localized glows */}
      <div className="pointer-events-none absolute -top-10 left-1/2 -translate-x-1/2 w-72 h-72 rounded-full bg-indigo-500/10 blur-3xl" />

      {/* Premium Circular SVG Progress Indicator */}
      <div className="relative flex items-center justify-center w-28 h-28 mb-8 mt-2 scale-110 select-none">
        {/* Outer subtle rotating dashed accent ring */}
        <div className="absolute inset-0 rounded-full border border-indigo-500/15 border-dashed animate-[spin_10s_linear_infinite]" />
        
        {/* Inner SVG progress circle */}
        <svg height={radius * 2} width={radius * 2} className="transform -rotate-90">
          {/* Track */}
          <circle
            stroke="rgba(226, 232, 240, 0.8)"
            fill="transparent"
            strokeWidth={stroke}
            r={normalizedRadius}
            cx={radius}
            cy={radius}
          />
          {/* Progress */}
          <circle
            stroke="url(#progress-gradient)"
            fill="transparent"
            strokeWidth={stroke}
            strokeDasharray={`${circumference} ${circumference}`}
            style={{ strokeDashoffset }}
            strokeLinecap="round"
            r={normalizedRadius}
            cx={radius}
            cy={radius}
            className="transition-all duration-300 ease-out"
          />
          <defs>
            <linearGradient id="progress-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#6366f1" />
              <stop offset="50%" stopColor="#a855f7" />
              <stop offset="100%" stopColor="#ec4899" />
            </linearGradient>
          </defs>
        </svg>
        
        {/* Glowing center text */}
        <div className="absolute flex flex-col items-center justify-center">
          <span className="text-2xl font-black bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-800 bg-clip-text text-transparent drop-shadow-sm">
            {progress}%
          </span>
          <span className="text-[8px] font-bold text-indigo-500 uppercase tracking-widest animate-pulse">
            Analyzing
          </span>
        </div>
      </div>

      {/* Header Info */}
      <div className="space-y-2 mb-8">
        <h3 className="text-2xl sm:text-3xl font-black tracking-tight text-slate-900 select-none">
          Analyzing{" "}
          <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 bg-clip-text text-transparent">
            @{username}
          </span>
        </h3>
      </div>

      {/* Progress Card */}
      <div className="w-full shadow-neumorphic hover:shadow-neumorphic-hover transition-all duration-300 p-8 mb-8">


        {/* Stages Checklist */}
        <div className="space-y-4 text-left">
          {STAGES.map((stage, idx) => {
            const isCompleted = idx < currentStage;
            const isCurrent = idx === currentStage;
            return (
              <div 
                key={idx} 
                className={`flex items-center space-x-4 transition-all duration-300 ${
                  isCurrent ? "scale-[1.02] translate-x-1" : ""
                }`}
              >
                {/* Stage Badge */}
                {isCompleted ? (
                  <span className="flex items-center justify-center w-6 h-6 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-600 transition-all duration-500 shadow-sm shadow-emerald-100">
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="3" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>
                  </span>
                ) : isCurrent ? (
                  <span className="relative flex items-center justify-center w-6 h-6 rounded-full bg-indigo-50 border border-indigo-300 text-indigo-600 shadow-sm shadow-indigo-100">
                    <span className="absolute inset-0 rounded-full bg-indigo-400/25 animate-ping" />
                    <span className="w-2.5 h-2.5 rounded-full bg-indigo-600" />
                  </span>
                ) : (
                  <span className="flex items-center justify-center w-6 h-6 rounded-full bg-slate-50 border border-slate-200 text-slate-400 text-xs font-bold transition-all duration-300">
                    {idx + 1}
                  </span>
                )}

                {/* Stage Description */}
                <span className={`text-sm transition-all duration-300 select-none ${
                  isCompleted 
                    ? "text-slate-400 font-medium" 
                    : isCurrent 
                      ? "text-indigo-950 font-bold" 
                      : "text-slate-400/70 font-medium"
                }`}>
                  {stage}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Cancel Button */}
      {onCancel && (
        <button
          onClick={onCancel}
          className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-slate-50 border border-slate-200/80 text-slate-700 font-bold rounded-2xl text-xs transition-all gap-2 cursor-pointer shadow-sm hover:shadow-md active:scale-95 duration-200 select-none"
        >
          <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
          Cancel & Go Back
        </button>
      )}
    </div>
  );
}
