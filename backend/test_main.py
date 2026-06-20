import sys
import unittest
from unittest.mock import patch, MagicMock

# Import the routes directly for fallback function testing
from app.main import app, read_root, health_check, analyze_creator
from app.db import get_database

try:
    from fastapi.testclient import TestClient
    client = TestClient(app)
    has_test_client = True
except Exception:
    has_test_client = False
    print("Warning: httpx or fastapi.testclient not found. Falling back to direct function-level route testing.")

class TestFastAPI(unittest.TestCase):
    def test_root_endpoint(self):
        if has_test_client:
            response = client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "ok"})
        else:
            res = read_root()
            self.assertEqual(res, {"status": "ok"})
            
    def test_health_endpoint(self):
        if has_test_client:
            response = client.get("/health")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"mongodb": "connected"})
        else:
            res = health_check()
            self.assertEqual(res, {"mongodb": "connected"})

    @patch("app.main.instagram_service")
    def test_analyze_endpoint(self, mock_service):
        # Mock profile and recent posts response
        mock_profile = {
            "username": "test_fastapi_user",
            "full_name": "Test FastAPI User",
            "biography": "Mock Bio #collab with @brand",
            "follower_count": 5000,
            "following_count": 100,
            "media_count": 2
        }
        mock_posts = [
            {"id": "post_111", "caption": "Awesome day #ad", "like_count": 100, "comment_count": 10, "taken_at": "2026-06-20T03:00:00+00:00"},
            {"id": "post_222", "caption": "Normal day", "like_count": 50, "comment_count": 5, "taken_at": "2026-06-19T03:00:00+00:00"}
        ]
        mock_service.fetch_profile.return_value = mock_profile
        mock_service.fetch_recent_posts.return_value = mock_posts

        if has_test_client:
            response = client.post("/analyze/test_fastapi_user")
            self.assertEqual(response.status_code, 200)
            data = response.json()
        else:
            data = analyze_creator("test_fastapi_user")
            
        # Assertions on returned data
        self.assertIn("profile", data)
        self.assertIn("analytics", data)
        self.assertIn("posts", data)
        self.assertEqual(len(data["posts"]), 2)
        self.assertEqual(data["profile"]["username"], "test_fastapi_user")
        self.assertEqual(data["analytics"]["total_posts_analyzed"], 2)
        self.assertEqual(data["analytics"]["avg_likes"], 75.0)
        self.assertEqual(data["analytics"]["avg_comments"], 7.5)
        # avg engagement per post = 82.5. ER = 82.5 / 5000 * 100 = 1.65
        self.assertEqual(data["analytics"]["engagement_rate"], 1.65)
        
        # Verify it was successfully upserted to MongoDB Atlas
        db = get_database()
        db_profile = db.profiles.find_one({"username": "test_fastapi_user"})
        self.assertIsNotNone(db_profile)
        self.assertEqual(db_profile["username"], "test_fastapi_user")
        self.assertEqual(db_profile["analytics"]["engagement_rate"], 1.65)
        
        db_post1 = db.posts.find_one({"post_id": "post_111"})
        self.assertIsNotNone(db_post1)
        self.assertEqual(db_post1["caption"], "Awesome day #ad")

        # Cleanup test records
        db.profiles.delete_one({"username": "test_fastapi_user"})
        db.posts.delete_many({"post_id": {"$in": ["post_111", "post_222"]}})
        print("Integration test passed and DB successfully cleaned up!")

if __name__ == "__main__":
    unittest.main()
