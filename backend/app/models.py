from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime

class ProfileResponse(BaseModel):
    """
    Pydantic response model representing a public creator's profile data.
    """
    username: str
    full_name: str
    biography: str
    external_url: Optional[str] = None
    profile_pic_url: str
    is_verified: bool
    follower_count: int
    following_count: int
    media_count: int

class PostResponse(BaseModel):
    """
    Pydantic response model representing a single Instagram post's metadata.
    """
    id: str
    caption: str
    thumbnail_url: Optional[str] = None
    like_count: int
    comment_count: int
    taken_at: Union[datetime, str]

class AnalyticsResponse(BaseModel):
    """
    Pydantic response model representing creator analytics.
    """
    engagement_rate: float
    avg_likes: float
    avg_comments: float
    total_posts_analyzed: int
    posting_frequency_days: float
    viral_posts: List[PostResponse]
    collaboration_posts: List[PostResponse]
    english_percent: float
    hindi_percent: float
    hinglish_percent: float

class AnalyzeResponse(BaseModel):
    """
    Pydantic response model representing the overall response for POST /analyze/{username}.
    """
    profile: ProfileResponse
    analytics: AnalyticsResponse
    posts: List[PostResponse]
