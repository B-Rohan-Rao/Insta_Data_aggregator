"use client";

import { MockPost } from "../mock/posts";

interface PostsGridProps {
  posts: MockPost[];
  followerCount: number;
}

export default function PostsGrid({ posts, followerCount }: PostsGridProps) {
  const getPostEngagementScore = (likes: number, comments: number) => {
    if (!followerCount || followerCount === 0) return "0.00%";
    const er = ((likes + comments) / followerCount) * 100;
    return er.toFixed(2) + "%";
  };

  const formatDate = (dateStr: string) => {
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    } catch (e) {
      return dateStr;
    }
  };

  return (
    <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm">
      <h3 className="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
        <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        Recent Content Analysis
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {posts.map((post, idx) => {
          const isCollab = post.caption.toLowerCase().includes("#ad") || 
                           post.caption.toLowerCase().includes("#sponsored") || 
                           post.caption.toLowerCase().includes("#collab") || 
                           post.caption.includes("@");

          return (
            <div
              key={post.id}
              className="group bg-slate-50 border border-slate-100 rounded-xl hover:shadow-md hover:border-slate-200 transition-all duration-300 p-5 flex flex-col justify-between space-y-4"
            >
              {/* Top Row: Post Number and ER */}
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Post #{idx + 1}</span>
                <span className="bg-indigo-50 text-indigo-700 text-[10px] font-extrabold px-2 py-0.5 rounded-md">
                  {getPostEngagementScore(post.like_count, post.comment_count)} ER
                </span>
              </div>

              {/* Body: Caption */}
              <div className="flex-1">
                <p className="text-xs font-semibold text-slate-700 line-clamp-4 leading-relaxed">
                  {post.caption ? (
                    post.caption.length > 120 ? post.caption.substring(0, 120) + "..." : post.caption
                  ) : (
                    <span className="text-slate-400 italic">No caption</span>
                  )}
                </p>
              </div>

              {/* Footer: Metadata & Metrics */}
              <div className="space-y-3 pt-3 border-t border-slate-100">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="font-semibold text-slate-400">{formatDate(post.taken_at)}</span>
                  <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider ${
                    isCollab 
                      ? "bg-amber-50 text-amber-700 border border-amber-100/50" 
                      : "bg-green-50 text-green-700 border border-green-100/50"
                  }`}>
                    {isCollab ? "Sponsor / Tag" : "Organic"}
                  </span>
                </div>

                {/* Likes and Comments */}
                <div className="flex items-center justify-between text-xs text-slate-500 font-extrabold">
                  <span className="flex items-center gap-1.5">
                    <svg className="w-3.5 h-3.5 text-rose-500 fill-current" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                    </svg>
                    {post.like_count.toLocaleString()}
                  </span>
                  <span className="flex items-center gap-1.5">
                    <svg className="w-3.5 h-3.5 text-cyan-500 fill-current" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
                    </svg>
                    {post.comment_count.toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
