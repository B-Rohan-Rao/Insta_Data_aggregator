"use client";

import { MockAnalytics } from "../mock/analytics";
import { MockPost } from "../mock/posts";
import AnimatedNumber from "./AnimatedNumber";

interface InsightsCardProps {
  analytics: MockAnalytics;
  posts: MockPost[];
}

export default function InsightsCard({ analytics, posts }: InsightsCardProps) {
  // Find highest engagement post (likes + comments)
  const getHighestEngagementPost = () => {
    if (!posts || posts.length === 0) return null;
    return posts.reduce((prev, current) => {
      const prevEng = prev.like_count + prev.comment_count;
      const currEng = current.like_count + current.comment_count;
      return currEng > prevEng ? current : prev;
    });
  };

  // Find most commented post
  const getMostCommentedPost = () => {
    if (!posts || posts.length === 0) return null;
    return posts.reduce((prev, current) => 
      current.comment_count > prev.comment_count ? current : prev
    );
  };

  const highestEngPost = getHighestEngagementPost();
  const mostCommentedPost = getMostCommentedPost();

  // Posting consistency evaluation
  const getConsistencyLabel = () => {
    const freq = analytics.posting_frequency_days;
    if (freq <= 0) return { label: "No Posts Analyzed", color: "text-slate-500", desc: "No posting activity found." };
    if (freq <= 2.2) return { label: "Highly Consistent", color: "text-green-600", desc: "Uploads content every 1-2 days." };
    if (freq <= 4.5) return { label: "Moderately Consistent", color: "text-amber-600", desc: "Uploads content twice a week." };
    return { label: "Occasional Poster", color: "text-rose-600", desc: "Posting frequency exceeds 5 days." };
  };

  // Collaboration status evaluation
  const getCollabStatus = () => {
    const count = analytics.collaboration_posts.length;
    if (count === 0) return { label: "Organic Focus", color: "text-indigo-600", desc: "No sponsored tags detected." };
    if (count <= 2) return { label: "Selective Collaborator", color: "text-purple-600", desc: "Collaborates with brands occasionally." };
    return { label: "Active Brand Partner", color: "text-cyan-600", desc: "Highly monetized with frequent sponsored spots." };
  };

  const consistency = getConsistencyLabel();
  const collab = getCollabStatus();

  return (
    <div className="shadow-neumorphic hover:shadow-neumorphic-hover transition-all duration-300 p-4 sm:p-5">
      <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
        Creator Insights
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Insight 1: Highest Engagement */}
        {highestEngPost && (
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-start gap-2">
            <span className="p-2 bg-indigo-50 text-indigo-600 rounded-lg flex-shrink-0 text-sm">🏆</span>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Top Performing Post</p>
              <p className="text-sm font-semibold text-slate-800 mt-0.5">
                <AnimatedNumber value={(highestEngPost.like_count + highestEngPost.comment_count).toLocaleString() + " Engagement"} />
              </p>
              <p className="text-xs text-slate-500 line-clamp-2 mt-0.5">"{highestEngPost.caption}"</p>
            </div>
          </div>
        )}

        {/* Insight 2: Most Commented */}
        {mostCommentedPost && (
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-start gap-2">
            <span className="p-2 bg-purple-50 text-purple-600 rounded-lg flex-shrink-0 text-sm">💬</span>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Most Discussed Post</p>
              <p className="text-sm font-semibold text-slate-800 mt-0.5">
                <AnimatedNumber value={mostCommentedPost.comment_count.toLocaleString() + " Comments"} />
              </p>
              <p className="text-xs text-slate-500 line-clamp-2 mt-0.5">"{mostCommentedPost.caption}"</p>
            </div>
          </div>
        )}

        {/* Insight 3: Posting Consistency */}
        <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-start gap-2">
          <span className="p-2 bg-green-50 text-green-600 rounded-lg flex-shrink-0 text-sm">📅</span>
          <div className="min-w-0 flex-1">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Posting Consistency</p>
            <p className={`text-sm font-semibold mt-0.5 ${consistency.color}`}>{consistency.label}</p>
            <p className="text-xs text-slate-400 mt-0.5">{consistency.desc}</p>
          </div>
        </div>

        {/* Insight 4: Sponsorship Rate */}
        <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-start gap-2">
          <span className="p-2 bg-amber-50 text-amber-600 rounded-lg flex-shrink-0 text-sm">🤝</span>
          <div className="min-w-0 flex-1">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Monetization Profile</p>
            <p className={`text-sm font-semibold mt-0.5 ${collab.color}`}>{collab.label}</p>
            <p className="text-xs text-slate-400 mt-0.5">{collab.desc}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
