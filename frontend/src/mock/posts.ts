export interface MockPost {
  id: string;
  caption: string;
  thumbnail_url: string;
  like_count: number;
  comment_count: number;
  taken_at: string;
}

export const mockPostsData: Record<string, MockPost[]> = {
  default: [
    {
      id: "post_1",
      caption: "New video coming out tonight at 7 PM! Stay tuned guys, this one is gonna be wild ⚡ #collab with @brand #newvideo",
      thumbnail_url: "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=600&q=80",
      like_count: 450000,
      comment_count: 25000,
      taken_at: "2026-06-19T14:30:00Z"
    },
    {
      id: "post_2",
      caption: "Chilling with the squad after a long week of shoot. Acha laga sabse milkar! #yaar #fun #squad",
      thumbnail_url: "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=600&q=80",
      like_count: 520000,
      comment_count: 18000,
      taken_at: "2026-06-17T11:15:00Z"
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
      id: "post_4",
      caption: "Throwback to when we hit 40M subscribers. Sapna lagta hai abhi bhi. Thank you for this beautiful journey! 🏆✨ #milestone",
      thumbnail_url: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=600&q=80",
      like_count: 1250000,
      comment_count: 95000,
      taken_at: "2026-06-12T16:45:00Z"
    },
    {
      id: "post_5",
      caption: "Workout diaries. Mehnat karna kabhi mat chodo. Stay fit, stay healthy! 💪🏋️ #fitness #lifestyle",
      thumbnail_url: "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80",
      like_count: 310000,
      comment_count: 8500,
      taken_at: "2026-06-10T07:30:00Z"
    },
    {
      id: "post_6",
      caption: "Exploring the beautiful streets of Mumbai. Yeh sheher nahi, emotions hai. What is your favorite place here? 🚕🌃",
      thumbnail_url: "https://images.unsplash.com/photo-1566552881560-0be862a7c445?auto=format&fit=crop&w=600&q=80",
      like_count: 420000,
      comment_count: 11000,
      taken_at: "2026-06-08T18:20:00Z"
    },
    {
      id: "post_7",
      caption: "Gaming night stream starts in 30 mins. Aajaao sab, link bio me hai! #streamer #gaming #ad with @computergods",
      thumbnail_url: "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=600&q=80",
      like_count: 280000,
      comment_count: 15000,
      taken_at: "2026-06-06T15:00:00Z"
    },
    {
      id: "post_8",
      caption: "Met this little fan today. Inke chehre ki smile hi sabse acha gift hai. ❤️ #blessed #fanslove",
      thumbnail_url: "https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?auto=format&fit=crop&w=600&q=80",
      like_count: 610000,
      comment_count: 12000,
      taken_at: "2026-06-04T12:00:00Z"
    },
    {
      id: "post_9",
      caption: "Trying out some new street food in Delhi. Dil waalon ki Dilli aur swaad ka khazana! 🍲😋 #foodie #delhistreetfood",
      thumbnail_url: "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=600&q=80",
      like_count: 390000,
      comment_count: 9500,
      taken_at: "2026-06-02T13:40:00Z"
    },
    {
      id: "post_10",
      caption: "Focus. Keep working in silence, let your success make the noise. #motivation #hustle",
      thumbnail_url: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80",
      like_count: 330000,
      comment_count: 7000,
      taken_at: "2026-05-31T08:10:00Z"
    },
    {
      id: "post_11",
      caption: "Behind the scenes from the next skit. Script reading is in progress. Kaise hoga ye shoot? Let's see! 😂🎬",
      thumbnail_url: "https://images.unsplash.com/photo-1501504905252-473c47e087f8?auto=format&fit=crop&w=600&q=80",
      like_count: 490000,
      comment_count: 22000,
      taken_at: "2026-05-29T10:30:00Z"
    },
    {
      id: "post_12",
      caption: "Weekend vibes. Calm before the storm. Hope you guys have a wonderful weekend! 🌅☕",
      thumbnail_url: "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=80",
      like_count: 270000,
      comment_count: 6500,
      taken_at: "2026-05-27T16:00:00Z"
    }
  ]
};
