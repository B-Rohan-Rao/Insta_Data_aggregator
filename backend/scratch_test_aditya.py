import os
import sys
import logging
from datetime import datetime

# Set up logging to stdout to capture warnings (e.g. SOURCE = ...)
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.instagram import InstagramService

def safe_print(label, val):
    if val is None:
        val_str = "None"
    elif isinstance(val, str):
        val_str = val
    else:
        val_str = str(val)
        
    try:
        enc = sys.stdout.encoding or 'utf-8'
        encoded = val_str.encode(enc, errors='replace')
        decoded = encoded.decode(enc)
        print(f"{label}: {decoded}")
    except Exception:
        try:
            print(f"{label}: {val_str.encode('ascii', errors='replace').decode('ascii')}")
        except Exception:
            pass

def main():
    print("Initializing InstagramService...")
    service = InstagramService()
    
    username = "adityasaidwhat"
    
    print(f"\n==========================================")
    print(f"Testing Creator: {username}")
    print(f"==========================================")
    
    try:
        # Fetch profile
        print("Calling fetch_profile...")
        profile = service.fetch_profile(username)
        
        # Fetch posts
        print("Calling fetch_recent_posts...")
        posts = service.fetch_recent_posts(username)
        
        # Output Profile Details
        print("\n--- Profile Metadata ---")
        safe_print("Username", profile.get('username'))
        safe_print("Full Name", profile.get('full_name'))
        safe_print("Biography", profile.get('biography'))
        safe_print("Followers", profile.get('follower_count'))
        safe_print("Following", profile.get('following_count'))
        safe_print("Media Count", profile.get('media_count'))
        safe_print("Profile URL", profile.get('external_url'))
        safe_print("Is Verified", profile.get('is_verified'))
        
        # Output Posts Details
        print(f"\n--- Posts Extracted ({len(posts)} posts) ---")
        for i, post in enumerate(posts):
            taken_at_str = post.get('taken_at')
            if isinstance(taken_at_str, datetime):
                taken_at_str = taken_at_str.isoformat()
            caption_preview = post.get('caption', '')
            if len(caption_preview) > 50:
                caption_preview = caption_preview[:47] + "..."
            # Strip newlines for single-line display
            caption_preview = caption_preview.replace('\n', ' ')
            safe_print(f"  Post {i+1}", f"ID={post.get('id')} | Likes={post.get('like_count')} | Comments={post.get('comment_count')} | TakenAt={taken_at_str} | Caption='{caption_preview}'")
            
        # Check cache storage of raw payload
        norm_user = username.lower().strip()
        cache_entry = service._scraped_cache.get(norm_user)
        if cache_entry:
            has_raw = cache_entry.get("raw_api_payload") is not None
            source_used = cache_entry.get("source")
            print(f"\nCache check: Source={source_used} | Raw API Payload Preserved={has_raw}")
            
    except Exception as e:
        print(f"\n[ERROR] Failed to fetch data for {username}: {e}")

if __name__ == "__main__":
    main()
