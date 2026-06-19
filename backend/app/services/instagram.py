import os
import json
import logging
from datetime import datetime
from app.config import settings
from typing import Any, Dict, List, Optional

from instagrapi import Client
from instagrapi.exceptions import (
    ClientError,
    LoginRequired,
    PrivateAccount,
    UserNotFound,
    ChallengeRequired,
    BadPassword,
    ReloginAttemptExceeded
)

logger = logging.getLogger(__name__)

class InstagramService:
    """
    Service for interacting with the Instagram API via instagrapi.
    Handles authentication, session persistence, and data extraction for public profiles.
    """

    def __init__(self) -> None:
        """
        Initializes the Instagram Client and sets up the session directory.
        """
        self.client = Client()
        self.session_file: str = "sessions/instagram_session.json"
        
        session_dir = os.path.dirname(self.session_file)
        if session_dir:
            os.makedirs(session_dir, exist_ok=True)
            
        self.client.challenge_code_handler = self._challenge_code_handler

    def _challenge_code_handler(self, username: str, choice: str) -> str:
        """
        Handles Instagram challenge (OTP/Verification code).
        Prompts the terminal user for the code.
        """
        logger.info("Challenge required")
        otp_code = input("Instagram verification code: ")
        return otp_code

    def login(self, force: bool = False) -> None:
        """
        Authenticates the client using credentials from environment variables.
        Attempts to reuse an existing session by validating it.
        If invalid or forced, falls back to standard login with OTP support.
        Persists the updated session to disk.
        """
        username = settings.IG_USERNAME
        password = settings.IG_PASSWORD

        if not username or not password:
            raise ValueError("IG_USERNAME and IG_PASSWORD environment variables must be populated.")

        session_valid = False
        
        if not force and os.path.exists(self.session_file):
            logger.info("Session file found")
            try:
                self.client.load_settings(self.session_file)
                
                # Check validation with lightweight call First
                try:
                    self.client.get_timeline_feed()
                    session_valid = True
                    logger.info("Session validation succeeded. Using existing Instagram session")
                except LoginRequired:
                    logger.warning("Session invalid or expired")
            except Exception as e:
                logger.warning(f"Failed to load or validate existing session: {e}")

        if not session_valid:
            logger.info("Attempting login")
            try:
                self.client.login(username, password)
                logger.info("Verification successful")
            except ChallengeRequired as e:
                logger.info("Challenge required")
                # instagrapi handles challenge using the challenge_code_handler under the hood
                # if login raises this, something went wrong with the handler or it failed.
                raise e
            except BadPassword as e:
                logger.error("Invalid credentials provided.")
                raise e
            except ReloginAttemptExceeded as e:
                logger.error("Relogin attempt exceeded limit.")
                raise e
            except Exception as e:
                logger.error(f"Login failed: {e}")
                raise LoginRequired(f"Failed to login: {str(e)}")

        try:
            self.client.dump_settings(self.session_file)
            logger.info("Session saved")
        except Exception as e:
            logger.error(f"Failed to save session: {e}")

    def fetch_profile(self, username: str) -> Dict[str, Any]:
        """
        Fetches a public creator's profile data.
        Returns a structured dictionary indicating account_status if the profile is private.
        """
        try:
            user_info = self.client.user_info_by_username(username)
            
            if user_info.is_private:
                return {
                    "account_status": "private",
                    "message": "Unable to access private account data"
                }

            return {
                "username": user_info.username,
                "full_name": user_info.full_name,
                "biography": user_info.biography,
                "external_url": str(user_info.external_url) if user_info.external_url else None,
                "profile_pic_url": str(user_info.profile_pic_url) if user_info.profile_pic_url else "",
                "is_verified": user_info.is_verified,
                "follower_count": int(user_info.follower_count),
                "following_count": int(user_info.following_count),
                "media_count": int(user_info.media_count)
            }
        except PrivateAccount:
            return {
                "account_status": "private",
                "message": "Unable to access private account data"
            }
        except UserNotFound:
            raise UserNotFound(f"The user '{username}' could not be found.")

    def fetch_recent_posts(self, username: str, limit: int = 12) -> List[Dict[str, Any]]:
        """
        Fetches the recent posts for the specified creator up to the given limit.
        """
        try:
            user_id = self.client.user_id_from_username(username)
            medias = self.client.user_medias(user_id, amount=limit)
            
            posts: List[Dict[str, Any]] = []
            for media in medias:
                posts.append({
                    "id": str(media.id),
                    "caption": media.caption_text,
                    "thumbnail_url": str(media.thumbnail_url) if media.thumbnail_url else None,
                    "like_count": int(media.like_count),
                    "comment_count": int(media.comment_count),
                    "taken_at": media.taken_at
                })
            return posts
        except PrivateAccount:
            return []
        except UserNotFound:
            raise UserNotFound(f"The user '{username}' could not be found.")

    def fetch_comments(self, media_id: str) -> List[Dict[str, Any]]:
        """
        Fetches text and usernames for comments on a specified media ID.
        If comments are disabled, gracefully returns an empty list without crashing.
        """
        try:
            # We fetch up to 50 comments (modify as needed) to supply sufficient NLP sample size
            comments_data = self.client.media_comments(media_id, amount=50)
            
            comments: List[Dict[str, Any]] = []
            for comment in comments_data:
                comments.append({
                    "username": comment.user.username,
                    "text": comment.text
                })
            return comments
        except ClientError:
            # instagrapi often throws a ClientError representing that comments are closed/disabled
            return []
        except Exception:
            # Ensure no crashes occur for other undefined comment retrieval errors
            return []
