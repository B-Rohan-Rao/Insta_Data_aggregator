import sys
from pathlib import Path

# Add backend directory to Python path so `app` can be imported
sys.path.append(str(Path(__file__).parent / "backend"))

from app.services.instagram import InstagramService
from instagrapi.exceptions import PrivateAccount, UserNotFound

def main() -> None:
    """
    Test the InstagramService by logging in, fetching a profile,
    fetching recent posts, and fetching comments for the first post.
    """
    print("Initializing InstagramService...")
    service = InstagramService()
    
    try:
        print("Logging in...")
        service.login()
        print("Login successful!\n")
        
        username = "viratkohli"
        
        # 1. Fetch Profile
        print(f"--- Fetching profile for @{username} ---")
        profile = service.fetch_profile(username)
        print("Profile Information:")
        print(profile)
        
        # 2. Fetch Recent Posts
        print(f"\n--- Fetching recent posts for @{username} ---")
        posts = service.fetch_recent_posts(username)
        print(f"Number of posts fetched: {len(posts)}")
        
        # 3. Fetch Comments
        if posts:
            first_post = posts[0]
            media_id = first_post["id"]
            print(f"\n--- Fetching comments for latest post ({media_id}) ---")
            comments = service.fetch_comments(media_id)
            print(f"Number of comments fetched: {len(comments)}")
        else:
            print("\nNo posts found to fetch comments.")
            
    except UserNotFound as e:
        print(f"\n[Error] User Not Found: {e}")
    except PrivateAccount as e:
        print(f"\n[Error] Private Account: {e}")
    except ValueError as e:
        print(f"\n[Error] Configuration check failed: {e}")
    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
