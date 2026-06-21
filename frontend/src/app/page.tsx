"use client";

import { useState, useEffect, useRef } from "react";
import { analyzeCreator, checkBackendHealth, AnalyzeResult } from "../lib/api";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";
import ProfileCard, { formatCount } from "../components/ProfileCard";
import MetricCard from "../components/MetricCard";
import AnalyticsCard from "../components/AnalyticsCard";
import LanguageCard from "../components/LanguageCard";
import InsightsCard from "../components/InsightsCard";
import PostsGrid from "../components/PostsGrid";
import { ShineButton } from "../components/ShineButton";

type PageState = "LANDING" | "LOADING" | "ERROR" | "RESULTS";

export default function Home() {
  const [state, setState] = useState<PageState>("LANDING");
  const [username, setUsername] = useState("");
  const [analyzingUsername, setAnalyzingUsername] = useState("");
  const [errorType, setErrorType] = useState<string>("backend_down");
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [backendHealth, setBackendHealth] = useState<{ mongodb: string } | null>(null);
  const [lastAnalysisTime, setLastAnalysisTime] = useState<string>("");
  const activeRequestRef = useRef<string | null>(null);

  useEffect(() => {
    // Initial health check
    checkBackendHealth().then((health) => {
      setBackendHealth(health);
    });
  }, []);

  const handleSearch = async (searchName: string) => {
    if (!searchName.trim()) return;

    activeRequestRef.current = searchName;
    setAnalyzingUsername(searchName);
    setState("LOADING");

    try {
      const data = await analyzeCreator(searchName);

      if (activeRequestRef.current !== searchName) {
        return;
      }

      // Determine if there was an explicit profile error or if the account is private
      if (data.profile.username === "" || !data.profile.follower_count) {
        setErrorType("not_found");
        setState("ERROR");
        return;
      }

      setResult(data);
      setLastAnalysisTime(new Date().toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }) + " " + new Date().toLocaleDateString("en-US", { month: "short", day: "numeric" }));
      setState("RESULTS");
    } catch (e: any) {
      if (activeRequestRef.current !== searchName) {
        return;
      }
      console.warn("Analysis request failed:", e.message || e);
      if (e && e.status) {
        const msg = (e.message || "").toLowerCase();
        if (e.status === 400) {
          if (msg.includes("private")) {
            setErrorType("private");
          } else {
            setErrorType("not_found");
          }
        } else if (e.status === 404) {
          setErrorType("not_found");
        } else {
          if (msg.includes("rate limit") || msg.includes("block") || msg.includes("unavailable")) {
            setErrorType("instagram_down");
          } else {
            setErrorType("backend_down");
          }
        }
      } else {
        setErrorType("backend_unreachable");
      }
      setState("ERROR");
    }
  };

  const handleReset = () => {
    activeRequestRef.current = null;
    setUsername("");
    setResult(null);
    setState("LANDING");
  };

  // Re-run health check on manual click
  const refreshHealth = () => {
    setBackendHealth(null);
    checkBackendHealth().then((health) => {
      setBackendHealth(health);
    });
  };

  return (
    <div className="flex flex-col min-h-screen bg-neumorphic-page text-slate-900 font-sans">
      {/* Main Content */}
      <main className="flex-1 w-full flex flex-col">
        {state === "LANDING" && (
          <div className="relative flex-1 flex items-start pt-20 sm:pt-32 min-h-screen">
            {/* Decorative background blobs */}
            <div className="pointer-events-none absolute inset-0 overflow-hidden">
              <div className="absolute -top-32 -right-32 w-[480px] h-[480px] rounded-full bg-gradient-to-br from-indigo-200/40 to-purple-200/30 blur-3xl" />
              <div className="absolute bottom-0 right-1/4 w-72 h-72 rounded-full bg-gradient-to-tr from-cyan-200/30 to-indigo-200/20 blur-2xl" />
              <div className="absolute top-1/2 -left-24 w-64 h-64 rounded-full bg-gradient-to-br from-purple-200/20 to-pink-200/10 blur-2xl" />
            </div>

            <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-16">
              <h1 className="text-[2.4rem] leading-[1.05] sm:text-6xl lg:text-[6.5rem] xl:text-[8rem] font-black tracking-tight text-slate-900 select-none break-words">
                Analyse your{" "}
                <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 bg-clip-text text-transparent">
                  Insta
                </span>{" "}
                creator
              </h1>

              {/* Search area */}
              <div className="mt-6 sm:mt-8 space-y-4">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSearch(username);
                  }}
                  className="flex flex-col sm:flex-row items-stretch gap-3 max-w-xl"
                >
                  <div className="relative flex-1">
                    <span className="absolute inset-y-0 left-4 flex items-center text-slate-400 font-semibold text-base">
                      @
                    </span>
                    <input
                      type="text"
                      required
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      placeholder="Enter Instagram username"
                      className="w-full pl-[38px] pr-4 py-4 bg-white border border-slate-200 rounded-2xl text-slate-900 placeholder-slate-400 focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 font-medium transition-all text-sm shadow-sm"
                    />
                  </div>
                  <ShineButton
                    type="submit"
                    bgColor="linear-gradient(to right, #4f46e5, #7c3aed)"
                    className="px-6 py-4 rounded-2xl font-bold text-sm flex items-center justify-center gap-2 cursor-pointer whitespace-nowrap"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    Analyse
                  </ShineButton>
                </form>

                {/* Popular creators */}
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-[11px] font-bold uppercase tracking-widest text-slate-400 mr-1">Try:</span>
                  {["virat.kohli", "carryminati", "adityasaidwhat"].map((name) => (
                    <button
                      key={name}
                      onClick={() => {
                        setUsername(name);
                        handleSearch(name);
                      }}
                      className="px-3 py-1.5 bg-white hover:bg-indigo-50 hover:text-indigo-600 border border-slate-200 hover:border-indigo-200 text-xs font-semibold text-slate-500 rounded-full transition-all cursor-pointer shadow-sm hover:shadow-neumorphic-hover"
                    >
                      @{name}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}


        {state === "LOADING" && (
          <div className="flex-1 flex items-center justify-center min-h-screen">
            <LoadingState username={analyzingUsername} onCancel={handleReset} />
          </div>
        )}

        {state === "ERROR" && (
          <div className="flex-1 flex items-center justify-center min-h-screen">
            <ErrorState
              errorType={errorType}
              onRetry={handleReset}
            />
          </div>
        )}

        {state === "RESULTS" && result && (
          <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
            {/* Top Toolbar / Reset */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-5">
              <div>
                <h2 className="text-2xl font-semibold text-slate-800">Intelligence Dashboard</h2>
              </div>
              <div className="flex items-center gap-3">
                {/* API status pill in results view */}
                <button
                  onClick={refreshHealth}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-bold transition-all hover:shadow-neumorphic-hover ${backendHealth
                      ? "bg-green-50 text-green-700 border-green-100 hover:bg-green-100"
                      : "bg-amber-50 text-amber-700 border-amber-100 hover:bg-amber-100 animate-pulse"
                    }`}
                >
                  <span className={`w-1.5 h-1.5 rounded-full ${backendHealth ? "bg-green-500" : "bg-amber-500 animate-ping"}`} />
                  {backendHealth ? "API Connected" : "API Offline"}
                </button>
                <button
                  onClick={handleReset}
                  className="inline-flex items-center justify-center px-4 py-2 bg-slate-100 hover:bg-slate-200 border border-slate-200 hover:border-slate-300 text-slate-700 font-bold rounded-xl text-xs transition-all gap-1.5 cursor-pointer hover:shadow-neumorphic-hover"
                >
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  Analyse Another
                </button>
              </div>
            </div>

            {/* Results Grid Layout */}
            <div className="grid grid-cols-1 gap-8">

              {/* SECTION 1 - CREATOR OVERVIEW */}
              <ProfileCard profile={result.profile} />

              {/* SECTION 2 - KPI METRICS ROW */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                  value={`${result.analytics.posting_frequency_days.toFixed(1)} Days`}
                  label="Posting Frequency"
                  trend={
                    result.analytics.posting_frequency_days <= 2.2
                      ? "Highly Consistent"
                      : result.analytics.posting_frequency_days <= 4.5
                        ? "Moderately Consistent"
                        : "Occasional Poster"
                  }
                  trendDirection={
                    result.analytics.posting_frequency_days <= 2.2
                      ? "up"
                      : result.analytics.posting_frequency_days <= 4.5
                        ? "neutral"
                        : "down"
                  }
                  iconType="frequency"
                />
                <MetricCard
                  value={`${result.analytics.engagement_rate.toFixed(2)}%`}
                  label="Engagement Rate"
                  trend={result.analytics.engagement_rate > 2.0 ? "Strong ER" : "Standard ER"}
                  trendDirection="up"
                  iconType="engagement"
                />
                <MetricCard
                  value={formatCount(result.analytics.avg_likes)}
                  label="Avg Likes"
                  trend="Likes/Post"
                  trendDirection="up"
                  iconType="likes"
                />
                <MetricCard
                  value={formatCount(result.analytics.avg_comments)}
                  label="Avg Comments"
                  trend="Comments/Post"
                  trendDirection="up"
                  iconType="comments"
                />
              </div>

              {/* SECTIONS 3 & 4 - ANALYTICS & LANGUAGE GRID (50% / 50%) */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Section 3: Performance Analytics */}
                <AnalyticsCard analytics={result.analytics} />

                {/* Section 4: Language Distribution */}
                <LanguageCard analytics={result.analytics} />
              </div>

              {/* SECTION 5 - CREATOR INSIGHTS (Full Width Below) */}
              <InsightsCard analytics={result.analytics} posts={result.recent_posts} />

              {/* SECTION 6 - RECENT POSTS GRID */}
              <PostsGrid posts={result.recent_posts} followerCount={result.profile.follower_count} />

              {/* SECTION 7 - DATABASE & STATUS INFO CARD */}
              <div className="bg-white border border-slate-100 rounded-xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-4 text-xs">
                <div className="flex flex-wrap items-center gap-6">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-400 uppercase tracking-wider">Backend Connection:</span>
                    <span className={`px-2 py-0.5 rounded-full font-bold uppercase tracking-wider text-[10px] ${result.isMock ? "bg-amber-50 text-amber-700" : "bg-green-50 text-green-700"
                      }`}>
                      {result.isMock ? "Fallback (Local)" : "Live API"}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-400 uppercase tracking-wider">MongoDB:</span>
                    <span className={`px-2 py-0.5 rounded-full font-bold uppercase tracking-wider text-[10px] ${backendHealth?.mongodb === "connected" ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"
                      }`}>
                      {backendHealth?.mongodb === "connected" ? "Connected" : "Disconnected"}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-slate-400 uppercase tracking-wider">Analysis Timestamp:</span>
                  <span className="font-bold text-slate-700">{lastAnalysisTime}</span>
                </div>
              </div>

            </div>
          </div>
        )}
      </main>
    </div>
  );
}
