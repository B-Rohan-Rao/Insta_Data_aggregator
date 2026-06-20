import re
from datetime import datetime
from typing import Any, Dict, List, Optional

def parse_datetime(val: Any) -> datetime:
    """
    Parses a datetime object, timestamp float/int, or ISO format string to a datetime object.
    """
    if isinstance(val, datetime):
        return val
    if isinstance(val, (int, float)):
        return datetime.fromtimestamp(val)
    if isinstance(val, str):
        # Handle Zulu suffix 'Z' for ISO 8601 strings
        if val.endswith("Z"):
            val = val[:-1] + "+00:00"
        return datetime.fromisoformat(val)
    raise ValueError(f"Unsupported datetime type: {type(val)}")

def calculate_median(values: List[float]) -> float:
    """
    Computes the median of a list of numeric values.
    """
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_vals[mid])
    else:
        return float(sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0

def is_collaboration_post(caption: Optional[str]) -> bool:
    """
    Checks if a post is a collaboration or sponsored post by looking for:
    - Hashtags: #ad, #sponsored, #collab (case-insensitive)
    - Username mentions: @username (excluding lone '@')
    """
    if not caption:
        return False
    
    caption_lower = caption.lower()
    
    # Check hashtags
    for tag in ["#ad", "#sponsored", "#collab"]:
        if tag in caption_lower:
            return True
            
    # Check for @brand mentions (@ followed by alphanumeric, dot, or underscore)
    if re.search(r"@[a-zA-Z0-9_.]+", caption):
        return True
        
    return False

def calculate_analytics(profile_data: Optional[Dict[str, Any]], recent_posts: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Computes creator analytics from profile data and a list of recent posts.
    
    Returns:
        Dict: {
            "engagement_rate": float,
            "avg_likes": float,
            "avg_comments": float,
            "total_posts_analyzed": int,
            "posting_frequency_days": float,
            "viral_posts": List[Dict],
            "collaboration_posts": List[Dict]
        }
    """
    if not profile_data:
        profile_data = {}
    if not recent_posts:
        recent_posts = []
        
    total_posts = len(recent_posts)
    follower_count = int(profile_data.get("follower_count") or 0)
    
    # 1. Averages
    total_likes = sum(int(p.get("like_count") or 0) for p in recent_posts)
    total_comments = sum(int(p.get("comment_count") or 0) for p in recent_posts)
    
    avg_likes = round(total_likes / total_posts, 2) if total_posts > 0 else 0.0
    avg_comments = round(total_comments / total_posts, 2) if total_posts > 0 else 0.0
    
    # 2. Engagement Rate
    # Formula: engagement_rate = (avg_likes + avg_comments) / follower_count * 100
    if follower_count > 0:
        engagement_rate = round(((avg_likes + avg_comments) / follower_count) * 100, 2)
    else:
        engagement_rate = 0.0
        
    # 3. Posting Frequency
    posting_frequency_days = 0.0
    valid_dates = []
    for p in recent_posts:
        if p.get("taken_at") is not None:
            try:
                valid_dates.append(parse_datetime(p["taken_at"]))
            except Exception:
                pass
                
    if len(valid_dates) > 1:
        valid_dates.sort()
        span = valid_dates[-1] - valid_dates[0]
        posting_frequency_days = round(span.total_seconds() / (86400 * (len(valid_dates) - 1)), 2)
        
    # 4. Viral posts: engagement > 3x median engagement
    engagements = []
    post_engagements = []
    for p in recent_posts:
        eng = int(p.get("like_count") or 0) + int(p.get("comment_count") or 0)
        engagements.append(eng)
        post_engagements.append((p, eng))
        
    median_engagement = calculate_median(engagements)
    viral_threshold = 3.0 * median_engagement
    
    viral_posts = [p for p, eng in post_engagements if eng > viral_threshold]
    
    # 5. Collaboration posts
    collaboration_posts = [p for p in recent_posts if is_collaboration_post(p.get("caption"))]
    
    return {
        "engagement_rate": engagement_rate,
        "avg_likes": avg_likes,
        "avg_comments": avg_comments,
        "total_posts_analyzed": total_posts,
        "posting_frequency_days": posting_frequency_days,
        "viral_posts": viral_posts,
        "collaboration_posts": collaboration_posts
    }
