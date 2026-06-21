import { MockPost } from "./posts";

export interface MockAnalytics {
  engagement_rate: number;
  avg_likes: number;
  avg_comments: number;
  total_posts_analyzed: number;
  posting_frequency_days: number;
  viral_posts: MockPost[];
  collaboration_posts: MockPost[];
  english_percent?: number;
  hindi_percent?: number;
  hinglish_percent?: number;
}

export const mockAnalyticsData: Record<string, MockAnalytics> = {
  default: {
    engagement_rate: 2.79,
    avg_likes: 486666.67,
    avg_comments: 21916.67,
    total_posts_analyzed: 12,
    posting_frequency_days: 2.08,
    english_percent: 22.4,
    hindi_percent: 35.8,
    hinglish_percent: 41.8,
    viral_posts: [
      {
        id: "post_4",
        caption: "Throwback to when we hit 40M subscribers. Sapna lagta hai abhi bhi. Thank you for this beautiful journey! 🏆✨ #milestone",
        thumbnail_url: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=600&q=80",
        like_count: 1250000,
        comment_count: 95000,
        taken_at: "2026-06-12T16:45:00Z"
      }
    ],
    collaboration_posts: [
      {
        id: "post_1",
        caption: "New video coming out tonight at 7 PM! Stay tuned guys, this one is gonna be wild ⚡ #collab with @brand #newvideo",
        thumbnail_url: "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=600&q=80",
        like_count: 450000,
        comment_count: 25000,
        taken_at: "2026-06-19T14:30:00Z"
      },
      {
        id: "post_3",
        caption: "Thank you for all the support on the latest podcast. Mera bhai log, you guys are the best! #sponsored by @hostcompany",
        thumbnail_url: "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=600&q=80",
        like_count: 380000,
        comment_count: 14000,
        taken_at: "2026-06-15T09:00:00Z"
      },
      {
        id: "post_7",
        caption: "Gaming night stream starts in 30 mins. Aajaao sab, link bio me hai! #streamer #gaming #ad with @computergods",
        thumbnail_url: "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=600&q=80",
        like_count: 280000,
        comment_count: 15000,
        taken_at: "2026-06-06T15:00:00Z"
      }
    ]
  },
  viratkohli: {
    engagement_rate: 1.85,
    avg_likes: 4850000.0,
    avg_comments: 14500.0,
    total_posts_analyzed: 12,
    posting_frequency_days: 1.45,
    english_percent: 68.5,
    hindi_percent: 12.2,
    hinglish_percent: 19.3,
    viral_posts: [
      {
        id: "v_post_1",
        caption: "Match winning innings today! Truly special moment. Thank you everyone for the love. 🇮🇳🏏",
        thumbnail_url: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=600&q=80",
        like_count: 8900000,
        comment_count: 45000,
        taken_at: "2026-06-18T16:00:00Z"
      }
    ],
    collaboration_posts: [
      {
        id: "v_post_3",
        caption: "Excited to partner with @brand to launch the new collection. #ad #sports #activewear",
        thumbnail_url: "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80",
        like_count: 4200000,
        comment_count: 12000,
        taken_at: "2026-06-14T11:00:00Z"
      }
    ]
  },
  "virat.kohli": {
    engagement_rate: 1.85,
    avg_likes: 4850000.0,
    avg_comments: 14500.0,
    total_posts_analyzed: 12,
    posting_frequency_days: 1.45,
    english_percent: 68.5,
    hindi_percent: 12.2,
    hinglish_percent: 19.3,
    viral_posts: [
      {
        id: "v_post_1",
        caption: "Match winning innings today! Truly special moment. Thank you everyone for the love. 🇮🇳🏏",
        thumbnail_url: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=600&q=80",
        like_count: 8900000,
        comment_count: 45000,
        taken_at: "2026-06-18T16:00:00Z"
      }
    ],
    collaboration_posts: [
      {
        id: "v_post_3",
        caption: "Excited to partner with @brand to launch the new collection. #ad #sports #activewear",
        thumbnail_url: "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80",
        like_count: 4200000,
        comment_count: 12000,
        taken_at: "2026-06-14T11:00:00Z"
      }
    ]
  },
  shraddhakapoor: {
    engagement_rate: 3.12,
    avg_likes: 2780000.0,
    avg_comments: 98000.0,
    total_posts_analyzed: 12,
    posting_frequency_days: 2.5,
    english_percent: 44.8,
    hindi_percent: 23.5,
    hinglish_percent: 31.7,
    viral_posts: [
      {
        id: "s_post_1",
        caption: "Happy Sunday everyone! What are you all reading today? 📚🌸✨ #sundayvibes",
        thumbnail_url: "https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?auto=format&fit=crop&w=600&q=80",
        like_count: 5200000,
        comment_count: 180000,
        taken_at: "2026-06-19T08:00:00Z"
      }
    ],
    collaboration_posts: [
      {
        id: "s_post_4",
        caption: "Tried this new skincare range from @brand and absolutely loved it! #collab #skincare #natural",
        thumbnail_url: "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=600&q=80",
        like_count: 2400000,
        comment_count: 75000,
        taken_at: "2026-06-12T14:00:00Z"
      }
    ]
  },
  adityasaidwhat: {
    engagement_rate: 3.12,
    avg_likes: 2780000.0,
    avg_comments: 98000.0,
    total_posts_analyzed: 12,
    posting_frequency_days: 2.5,
    english_percent: 44.8,
    hindi_percent: 23.5,
    hinglish_percent: 31.7,
    viral_posts: [
      {
        id: "s_post_1",
        caption: "Happy Sunday everyone! What are you all reading today? 📚🌸✨ #sundayvibes",
        thumbnail_url: "https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?auto=format&fit=crop&w=600&q=80",
        like_count: 5200000,
        comment_count: 180000,
        taken_at: "2026-06-19T08:00:00Z"
      }
    ],
    collaboration_posts: [
      {
        id: "s_post_4",
        caption: "Tried this new skincare range from @brand and absolutely loved it! #collab #skincare #natural",
        thumbnail_url: "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=600&q=80",
        like_count: 2400000,
        comment_count: 75000,
        taken_at: "2026-06-12T14:00:00Z"
      }
    ]
  }
};
