import sys
from datetime import datetime, timedelta
from app.analytics import calculate_analytics, is_collaboration_post

def run_tests():
    print("Starting analytics.py verification...")
    
    # 1. Test collab detection
    assert is_collaboration_post("Just a normal post") is False
    assert is_collaboration_post("Checking out this cool stuff #ad") is True
    assert is_collaboration_post("SPONSORED content: #sponsored") is True
    assert is_collaboration_post("We have a new #collab with @nike") is True
    assert is_collaboration_post("Hey there @brand!") is True
    assert is_collaboration_post(None) is False
    print("Collab detection tests passed!")

    # 2. Test analytics calculation with mock data
    profile = {
        "username": "test_influencer",
        "follower_count": 10000
    }
    
    now = datetime.now()
    posts = [
        {"like_count": 100, "comment_count": 10, "caption": "Post 1", "taken_at": now - timedelta(days=9)},
        {"like_count": 120, "comment_count": 15, "caption": "Post 2 #ad", "taken_at": now - timedelta(days=6)},
        {"like_count": 90, "comment_count": 5, "caption": "Post 3", "taken_at": now - timedelta(days=3)},
        # This post should be viral: engagement is 500 + 50 = 550.
        # Engagements: Post 1 (110), Post 2 (135), Post 3 (95), Post 4 (550).
        # Sorted engagements: [95, 110, 135, 550]
        # Median engagement = (110 + 135) / 2 = 122.5
        # Viral threshold = 3 * 122.5 = 367.5
        # Post 4 engagement is 550 > 367.5 (viral)
        {"like_count": 500, "comment_count": 50, "caption": "Viral post!", "taken_at": now}
    ]
    
    res = calculate_analytics(profile, posts)
    
    # Total likes = 100+120+90+500 = 810. Avg = 810 / 4 = 202.5
    # Total comments = 10+15+5+50 = 80. Avg = 80 / 4 = 20.0
    # Engagement rate = (202.5 + 20.0) / 10000 * 100 = 222.5 / 10000 * 100 = 2.225% (rounds to 2.23%)
    # Posting frequency: 9 days span over 4 posts (3 intervals) = 3 days/post.
    
    print(f"Results computed: {res}")
    
    assert res["total_posts_analyzed"] == 4
    assert res["avg_likes"] == 202.5
    assert res["avg_comments"] == 20.0
    assert res["engagement_rate"] == 2.23
    assert res["posting_frequency_days"] == 3.0
    
    # Viral posts check
    assert len(res["viral_posts"]) == 1
    assert res["viral_posts"][0]["caption"] == "Viral post!"
    
    # Collab posts check
    assert len(res["collaboration_posts"]) == 1
    assert res["collaboration_posts"][0]["caption"] == "Post 2 #ad"
    
    print("Analytics calculation checks passed!")
    
    # 3. Test division by zero and empty profile
    res_empty = calculate_analytics(None, [])
    assert res_empty["engagement_rate"] == 0.0
    assert res_empty["total_posts_analyzed"] == 0
    assert res_empty["posting_frequency_days"] == 0.0
    print("Empty / edge-case checks passed!")

    print("\nAll analytics tests passed successfully!")

if __name__ == "__main__":
    run_tests()
