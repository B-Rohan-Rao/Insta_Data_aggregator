"use client";

import { MockProfile } from "../mock/profile";
import AnimatedNumber from "./AnimatedNumber";

interface ProfileCardProps {
  profile: MockProfile;
}

export function formatCount(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1).replace(/\.0$/, "") + "M";
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1).replace(/\.0$/, "") + "K";
  }
  return num.toString();
}

export default function ProfileCard({ profile }: ProfileCardProps) {
  return (
    <div className="shadow-neumorphic hover:shadow-neumorphic-hover transition-all duration-300 p-4 sm:p-5">
      <div className="flex flex-col md:flex-row items-stretch md:items-start gap-4 sm:gap-6">
        {/* Left Side: Creator Identity Badge */}
        <div className="flex-shrink-0 flex flex-col items-center justify-center p-3 sm:p-4 bg-gradient-to-br from-indigo-50/50 to-purple-50/50 border border-indigo-100/40 rounded-2xl w-full md:w-40 text-center select-none">
          <span className="text-[10px] font-bold text-indigo-500 uppercase tracking-widest">Creator Profile</span>
          <div className="mt-2 text-base font-extrabold text-slate-800 flex items-center justify-center gap-1">
            {profile.is_verified ? (
              <>
                <span className="text-indigo-600">Verified</span>
                <svg className="w-4 h-4 text-indigo-500 fill-current" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4.13-5.69a.02.02 0 00.02-.02z" clipRule="evenodd" />
                </svg>
              </>
            ) : (
              <span className="text-slate-500">Public Account</span>
            )}
          </div>
          <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest mt-1">Status</span>
        </div>

        {/* Right Side: Profile Info */}
        <div className="flex-1 text-center md:text-left space-y-2.5">
          <div>
            <div className="flex flex-wrap items-center justify-center md:justify-start gap-2 mb-1">
              <h2 className="text-xl font-bold text-slate-900">@{profile.username}</h2>
              {profile.is_verified && (
                <svg className="w-5 h-5 text-indigo-500 fill-current" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M6.267 3.455a.75.75 0 00-.707-.547H3.5a.75.75 0 00-.75.75v2.06c0 .278.155.534.4.671l1.455.819a.75.75 0 00.353.09h1.768a.75.75 0 00.707-.547l.835-2.846zM13.733 3.455a.75.75 0 01.707-.547H16.5a.75.75 0 01.75.75v2.06c0 .278-.155.534-.4.671l-1.455.819a.75.75 0 01-.353.09h-1.768a.75.75 0 01-.707-.547l-.835-2.846zM3.5 13.733a.75.75 0 00-.75.75V16.5a.75.75 0 00.75.75h2.06c.278 0 .534-.155.671-.4l.819-1.455a.75.75 0 00.09-.353V14.5a.75.75 0 00-.547-.707l-2.846-.835zM16.5 13.733a.75.75 0 01.75.75V16.5a.75.75 0 01-.75.75h-2.06c-.278 0-.534-.155-.671-.4l-.819-1.455a.75.75 0 01-.09-.353V14.5a.75.75 0 01.547-.707l2.846-.835z" clipRule="evenodd" />
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4.13-5.69a.02.02 0 00.02-.02z" clipRule="evenodd" />
                </svg>
              )}
            </div>
            <p className="text-sm font-semibold text-slate-500">{profile.full_name}</p>
          </div>

          <p className="text-sm text-slate-700 whitespace-pre-line leading-relaxed max-w-xl">
            {profile.biography}
          </p>

          {profile.external_url && (
            <a
              href={profile.external_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-sm font-semibold text-indigo-600 hover:text-indigo-700"
            >
              <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
              </svg>
              {profile.external_url.replace(/https?:\/\/(www\.)?/, "")}
            </a>
          )}

          {/* Followers Summary for Small/Medium screen fallback */}
          <div className="flex items-center justify-center md:justify-start gap-6 pt-3 border-t border-slate-100">
            <div>
              <p className="text-xl font-semibold text-slate-900">
                <AnimatedNumber value={formatCount(profile.follower_count)} />
              </p>
              <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Followers</p>
            </div>
            <div>
              <p className="text-xl font-semibold text-slate-900">
                <AnimatedNumber value={formatCount(profile.following_count)} />
              </p>
              <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Following</p>
            </div>
            <div>
              <p className="text-xl font-semibold text-slate-900">
                <AnimatedNumber value={formatCount(profile.media_count)} />
              </p>
              <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Posts</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
