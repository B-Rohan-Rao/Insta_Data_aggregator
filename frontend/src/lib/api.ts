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

export async function analyzeCreator(username: string): Promise<AnalyzeResult> {
  const normalizedUsername = username.trim().toLowerCase();
  
  // Simulate network delay for nice loading screen transitions
  await new Promise((resolve) => setTimeout(resolve, 2000));
  
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
      // If server returned non-200 (e.g. 404, 400), throw to trigger mock fallback or error
      throw new Error(`Server returned status: ${response.status}`);
    }
  } catch (e) {
    console.warn("Backend API unavailable or returned error, falling back to mock data.", e);
    
    // Check if the username exists in our mock profiles database
    const mockProfile = mockProfileData[normalizedUsername] || mockProfileData.default;
    const mockAnalytics = mockAnalyticsData[normalizedUsername] || mockAnalyticsData.default;
    const mockPosts = mockPostsData[normalizedUsername] || mockPostsData.default;
    
    return {
      profile: {
        ...mockProfile,
        // If they searched a custom user, override username to match their search
        username: mockProfileData[normalizedUsername] ? mockProfile.username : username
      },
      analytics: mockAnalytics,
      recent_posts: mockPosts,
      isMock: true,
    };
  }
}
