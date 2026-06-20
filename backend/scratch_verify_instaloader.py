import json
import logging
from app.services.instagram import InstagramService

# Configure logging to output to console
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

def test_user(service: InstagramService, username: str):
    print(f"\n========================================")
    print(f"TESTING USERNAME: @{username}")
    print(f"========================================")
    
    # 1. Test profile retrieval
    profile_data = None
    try:
        profile_data = service.fetch_profile(username)
        print(f"Profile Retrieval: SUCCESS")
        print(f"  Follower Count: {profile_data.get('follower_count')}")
        print(f"  Media Count: {profile_data.get('media_count')}")
        print(f"  Verified: {profile_data.get('is_verified')}")
    except Exception as e:
        print(f"Profile Retrieval: FAILED")
        print(f"  Reason: {e}")
        
    # 2. Test recent posts retrieval
    posts_data = None
    try:
        posts_data = service.fetch_recent_posts(username, limit=12)
        print(f"Recent Posts Retrieval: SUCCESS")
        print(f"  Number of Posts Retrieved: {len(posts_data)}")
        if posts_data:
            print(f"  First Post ID: {posts_data[0].get('id')}")
            print(f"  First Post Like Count: {posts_data[0].get('like_count')}")
    except Exception as e:
        print(f"Recent Posts Retrieval: FAILED")
        print(f"  Reason: {e}")

def main():
    service = InstagramService()
    
    # List of usernames to test
    usernames = ["carryminati", "viratkohli", "shraddhakapoor", "leomessi"]
    
    for username in usernames:
        test_user(service, username)

if __name__ == "__main__":
    main()
