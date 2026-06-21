"use client";

interface ErrorStateProps {
  errorType: "not_found" | "private" | "instagram_down" | "backend_down" | string;
  onRetry: () => void;
}

export default function ErrorState({ errorType, onRetry }: ErrorStateProps) {
  const getErrorInfo = () => {
    switch (errorType) {
      case "not_found":
        return {
          title: "Profile Not Found",
          message: "The requested Instagram username does not exist. Please check the spelling and try again.",
        };
      case "private":
        return {
          title: "Private Profile",
          message: "This profile is private. We can only retrieve analytics and post history for public creator accounts.",
        };
      case "instagram_down":
        return {
          title: "Instagram Temporarily Unavailable",
          message: "Instagram's servers are currently blocking requests or rate-limiting traffic. Please try again in a few minutes.",
        };
      case "backend_down":
      default:
        return {
          title: "Analysis Failed",
          message: "Our server or database is temporarily unavailable. We will fall back to using offline mock data shortly, or you can retry the connection.",
        };
    }
  };

  const info = getErrorInfo();

  return (
    <div className="max-w-md mx-auto px-4 py-8">
      <div className="bg-red-50 border border-red-200 rounded-2xl p-6 shadow-sm text-center">
        {/* Red Warning Icon */}
        <div className="inline-flex items-center justify-center w-12 h-12 bg-red-100 text-red-600 rounded-full mb-4">
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>

        {/* Text */}
        <h3 className="text-lg font-bold text-red-900 mb-2">{info.title}</h3>
        <p className="text-sm text-red-700 mb-6">{info.message}</p>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            onClick={onRetry}
            className="w-full sm:w-auto px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white font-medium rounded-xl text-sm transition-colors cursor-pointer"
          >
            Retry Analysis
          </button>
        </div>
      </div>
    </div>
  );
}
