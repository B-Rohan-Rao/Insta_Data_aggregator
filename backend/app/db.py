from pymongo import MongoClient
from app.config import settings

# Global MongoClient and Database instances to reuse the connection pool
_client = None
_db = None

def get_database():
    """
    Returns the MongoDB Database instance configured from settings.
    Initializes the MongoClient, creates collections, and configures unique indexes on the first call.
    """
    global _client, _db
    if _db is None:
        _client = MongoClient(settings.MONGO_URI)
        _db = _client[settings.DB_NAME]
        _init_db(_db)
    return _db

def _init_db(db):
    """
    Initializes the required collections and sets up unique indexes:
    - profiles: unique index on username
    - posts: unique index on post_id
    - comments: unique index on comment_id
    """
    existing_collections = db.list_collection_names()
    
    # 1. Create collections if they do not exist
    required_collections = ["profiles", "posts", "comments"]
    for col_name in required_collections:
        if col_name not in existing_collections:
            db.create_collection(col_name)
            
    # 2. Create unique indexes
    db.profiles.create_index("username", unique=True)
    db.posts.create_index("post_id", unique=True)
    db.comments.create_index("comment_id", unique=True)
