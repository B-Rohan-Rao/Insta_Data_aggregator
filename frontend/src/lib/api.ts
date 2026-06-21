import { mockProfileData, MockProfile } from "../mock/profile";
import { mockPostsData, MockPost } from "../mock/posts";
import { mockAnalyticsData, MockAnalytics } from "../mock/analytics";

export interface AnalyzeResult {
  profile: MockProfile;
  analytics: MockAnalytics;
  recent_posts: MockPost[];
  isMock: boolean;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function checkBackendHealth(): Promise<{ mongodb: string } | null> {
  try {
    const res = await fetch(`${API_URL}/health`, { signal: AbortSignal.timeout(3000) });
    if (res.ok) {
      return await res.json();
    }
  } catch (e) {
    // Backend is unreachable
  }
  return null;
}

export class HttpError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = "HttpError";
    Object.setPrototypeOf(this, HttpError.prototype);
  }
}

export async function analyzeCreator(username: string): Promise<AnalyzeResult> {
  const normalizedUsername = username.trim().toLowerCase();
  
  try {
    const response = await fetch(`${API_URL}/analyze/${normalizedUsername}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    
    if (response.ok) {
      const data = await response.json();
      
      return {
        profile: data.profile,
        analytics: data.analytics,
        recent_posts: data.posts,
        isMock: false,
      };
    } else {
      let detail = `Server returned status: ${response.status}`;
      try {
        const errJson = await response.json();
        if (errJson && errJson.detail) {
          detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail);
        }
      } catch (err) {
        // Failed to parse JSON detail
      }
      throw new HttpError(response.status, detail);
    }
  } catch (e: any) {
    // Propagate all errors directly to the caller, disabling mock fallback
    throw e;
  }
}

