from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_database
from app.services.instagram import InstagramService
from app.analytics import calculate_analytics
from app.models import AnalyzeResponse
from app.exceptions import (
    InstagramProfileNotFoundError,
    InstagramProfilePrivateError,
    InstagramRateLimitError
)

app = FastAPI(title="Praja Insta Data Aggregator API")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Instagram Service
instagram_service = InstagramService()

@app.get("/")
def read_root():
    """
    Root endpoint verifying application status.
    """
    return {"status": "ok"}

@app.get("/health")
def health_check():
    """
    Health check endpoint verifying database connectivity.
    """
    try:
        db = get_database()
        db.command("ping")
        return {"mongodb": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={"mongodb": "disconnected", "error": str(e)}
        )

@app.post("/analyze/{username}", response_model=AnalyzeResponse)
def analyze_creator(username: str):
    """
    Fetches creator profile, fetches recent posts (12), calculates analytics,
    saves the results (upsert) to MongoDB collections, and returns the response.
    """
    try:
        # 1. Fetch profile
        profile_data = instagram_service.fetch_profile(username)
        
        # Check if profile retrieval failed or if it is private
        if not profile_data or profile_data.get("account_status") == "private" or profile_data.get("is_private"):
            raise InstagramProfilePrivateError("Instagram profile is private")
            
        # 2. Fetch recent posts (limit 12)
        recent_posts = instagram_service.fetch_recent_posts(username, limit=12)
        
        # 3. Calculate analytics
        analytics_data = calculate_analytics(profile_data, recent_posts)
        
        # 4. Save results to MongoDB
        db = get_database()
        
        # Upsert profile with latest analytics attached
        profile_doc = profile_data.copy()
        profile_doc["analytics"] = analytics_data
        db.profiles.update_one(
            {"username": username},
            {"$set": profile_doc},
            upsert=True
        )
        
        # Upsert posts in posts collection
        for post in recent_posts:
            post_data = post.copy()
            # Convert taken_at datetime to ISO format string or timestamp if needed for MongoDB serialization
            # PyMongo handles datetime objects natively, so we can keep it as is.
            post_data["post_id"] = post["id"]
            db.posts.update_one(
                {"post_id": post["id"]},
                {"$set": post_data},
                upsert=True
            )
            
        return {
            "profile": profile_data,
            "analytics": analytics_data,
            "posts": recent_posts
        }
        
    except InstagramProfileNotFoundError as e:
        raise HTTPException(status_code=404, detail="Instagram profile not found")
    except InstagramProfilePrivateError as e:
        raise HTTPException(status_code=400, detail="Instagram profile is private")
    except InstagramRateLimitError as e:
        raise HTTPException(status_code=429, detail="Instagram rate limit reached")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
