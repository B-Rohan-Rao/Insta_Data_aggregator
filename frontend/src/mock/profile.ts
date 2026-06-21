export interface MockProfile {
  username: string;
  full_name: string;
  biography: string;
  profile_pic_url: string;
  follower_count: number;
  following_count: number;
  media_count: number;
  is_verified: boolean;
  external_url: string | null;
}

export const mockProfileData: Record<string, MockProfile> = {
  default: {
    username: "carryminati",
    full_name: "Ajey Nagar",
    biography: "Youth Icon of India 🇮🇳 | Creator | Gamer | Entertainer\nFor business inquiries: business@carryminati.com",
    profile_pic_url: "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=300&q=80",
    follower_count: 18200000,
    following_count: 120,
    media_count: 350,
    is_verified: true,
    external_url: "https://youtube.com/carryminati"
  },
  viratkohli: {
    username: "viratkohli",
    full_name: "Virat Kohli",
    biography: "Athlete. Proud father and husband. Co-owner of One8.",
    profile_pic_url: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80",
    follower_count: 270000000,
    following_count: 285,
    media_count: 1680,
    is_verified: true,
    external_url: "https://one8.com"
  },
  "virat.kohli": {
    username: "virat.kohli",
    full_name: "Virat Kohli",
    biography: "Athlete. Proud father and husband. Co-owner of One8.",
    profile_pic_url: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80",
    follower_count: 270000000,
    following_count: 285,
    media_count: 1680,
    is_verified: true,
    external_url: "https://one8.com"
  },
  shraddhakapoor: {
    username: "shraddhakapoor",
    full_name: "Shraddha Kapoor",
    biography: "Living my dream ✨ Keep shining, keep smiling!\n🌸 Blessed 🌸",
    profile_pic_url: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=300&q=80",
    follower_count: 92400000,
    following_count: 840,
    media_count: 1950,
    is_verified: true,
    external_url: "https://linktr.ee/shraddhakapoor"
  },
  adityasaidwhat: {
    username: "adityasaidwhat",
    full_name: "Aditya",
    biography: "Living my dream ✨ Keep shining, keep smiling!\n🌸 Blessed 🌸",
    profile_pic_url: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=300&q=80",
    follower_count: 92400000,
    following_count: 840,
    media_count: 1950,
    is_verified: true,
    external_url: "https://www.instagram.com/adityasaidwhat/"
  }
};
