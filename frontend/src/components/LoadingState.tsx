"use client";

import { useEffect, useState } from "react";

interface LoadingStateProps {
  username: string;
}

const STAGES = [
  "Fetching profile...",
  "Analyzing posts...",
  "Calculating engagement...",
  "Generating insights..."
];

export default function LoadingState({ username }: LoadingStateProps) {
  const [currentStage, setCurrentStage] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Increment loading stages
    const stageInterval = setInterval(() => {
      setCurrentStage((prev) => (prev < STAGES.length - 1 ? prev + 1 : prev));
    }, 500);

    // Smooth progress bar
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 2;
      });
    }, 40);

    return () => {
      clearInterval(stageInterval);
      clearInterval(progressInterval);
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] max-w-md mx-auto text-center px-4">
      {/* Large Spinner */}
      <div className="relative flex items-center justify-center w-24 h-24 mb-8">
        <div className="absolute w-full h-full border-4 border-slate-200 rounded-full"></div>
        <div className="absolute w-full h-full border-4 border-indigo-600 rounded-full border-t-transparent animate-spin"></div>
        <span className="text-sm font-semibold text-indigo-600">{progress}%</span>
      </div>

      {/* Title */}
      <h3 className="text-xl font-bold text-slate-900 mb-2">Analyzing @{username}</h3>
      <p className="text-sm text-slate-500 mb-8">Please wait while we gather creator intelligence.</p>

      {/* Progress Card */}
      <div className="w-full bg-white rounded-2xl border border-slate-100 p-6 shadow-sm">
        <div className="w-full bg-slate-100 rounded-full h-2 mb-6 overflow-hidden">
          <div 
            className="bg-gradient-to-r from-indigo-600 to-purple-600 h-full rounded-full transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          ></div>
        </div>

        {/* Stages Checklist */}
        <div className="space-y-3 text-left">
          {STAGES.map((stage, idx) => {
            const isCompleted = idx < currentStage;
            const isCurrent = idx === currentStage;
            return (
              <div key={idx} className="flex items-center space-x-3 text-sm">
                <span className={`flex items-center justify-center w-5 h-5 rounded-full border text-xs font-bold transition-all duration-300 ${
                  isCompleted 
                    ? "bg-green-100 border-green-500 text-green-700" 
                    : isCurrent 
                      ? "bg-indigo-50 border-indigo-500 text-indigo-700 animate-pulse" 
                      : "bg-slate-50 border-slate-200 text-slate-400"
                }`}>
                  {isCompleted ? "✓" : idx + 1}
                </span>
                <span className={`transition-colors duration-300 ${
                  isCompleted 
                    ? "text-slate-500 line-through" 
                    : isCurrent 
                      ? "text-indigo-600 font-medium" 
                      : "text-slate-400"
                }`}>
                  {stage}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
