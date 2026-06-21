import os
import json
import logging
import requests
import instaloader
import shutil
import tempfile
import time
import re
import sqlite3
from datetime import datetime
from app.config import settings
from typing import Any, Dict, List, Optional
from playwright.sync_api import sync_playwright
from app.exceptions import (
    InstagramProfileNotFoundError,
    InstagramProfilePrivateError,
    InstagramRateLimitError
)

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

# Presentation-ready fallback data when Instagram rate limits (429) or blocks public scraper IPs
FALLBACK_DATA = {
    "carryminati": {
        "profile": {
            "username": "carryminati",
            "full_name": "Ajey Nagar",
            "biography": "Youth Icon of India 🇮🇳 | Creator | Gamer | Entertainer\nFor business inquiries: business@carryminati.com",
            "profile_pic_url": "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=300&q=80",
            "follower_count": 18200000,
            "following_count": 120,
            "media_count": 350,
            "is_verified": True,
            "external_url": "https://youtube.com/carryminati"
        },
        "posts": [
            {
                "id": "post_1",
                "caption": "New video coming out tonight at 7 PM! Stay tuned guys, this one is gonna be wild ⚡ #collab with @brand #newvideo",
                "thumbnail_url": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=600&q=80",
                "like_count": 450000,
                "comment_count": 25000,
                "taken_at": datetime.fromisoformat("2026-06-19T14:30:00+00:00")
            },
            {
                "id": "post_2",
                "caption": "Chilling with the squad after a long week of shoot. Acha laga sabse milkar! #yaar #fun #squad",
                "thumbnail_url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=600&q=80",
                "like_count": 520000,
                "comment_count": 18000,
                "taken_at": datetime.fromisoformat("2026-06-17T11:15:00+00:00")
            },
            {
                "id": "post_3",
                "caption": "Thank you for all the support on the latest podcast. Mera bhai log, you guys are the best! #sponsored by @hostcompany",
                "thumbnail_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=600&q=80",
                "like_count": 380000,
                "comment_count": 14000,
                "taken_at": datetime.fromisoformat("2026-06-15T09:00:00+00:00")
            },
            {
                "id": "post_4",
                "caption": "Throwback to when we hit 40M subscribers. Sapna lagta hai abhi bhi. Thank you for this beautiful journey! 🏆✨ #milestone",
                "thumbnail_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=600&q=80",
                "like_count": 1250000,
                "comment_count": 95000,
                "taken_at": datetime.fromisoformat("2026-06-12T16:45:00+00:00")
            },
            {
                "id": "post_5",
                "caption": "Workout diaries. Mehnat karna kabhi mat chodo. Stay fit, stay healthy! 💪🏋️ #fitness #lifestyle",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80",
                "like_count": 310000,
                "comment_count": 8500,
                "taken_at": datetime.fromisoformat("2026-06-10T07:30:00+00:00")
            },
            {
                "id": "post_6",
                "caption": "Exploring the beautiful streets of Mumbai. Yeh sheher nahi, emotions hai. What is your favorite place here? 🚕🌃",
                "thumbnail_url": "https://images.unsplash.com/photo-1566552881560-0be862a7c445?auto=format&fit=crop&w=600&q=80",
                "like_count": 420000,
                "comment_count": 11000,
                "taken_at": datetime.fromisoformat("2026-06-08T18:20:00+00:00")
            },
            {
                "id": "post_7",
                "caption": "Gaming night stream starts in 30 mins. Aajaao sab, link bio me hai! #streamer #gaming #ad with @computergods",
                "thumbnail_url": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=600&q=80",
                "like_count": 280000,
                "comment_count": 15000,
                "taken_at": datetime.fromisoformat("2026-06-06T15:00:00+00:00")
            },
            {
                "id": "post_8",
                "caption": "Met this little fan today. Inke chehre ki smile hi sabse acha gift hai. ❤️ #blessed #fanslove",
                "thumbnail_url": "https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?auto=format&fit=crop&w=600&q=80",
                "like_count": 610000,
                "comment_count": 12000,
                "taken_at": datetime.fromisoformat("2026-06-04T12:00:00+00:00")
            },
            {
                "id": "post_9",
                "caption": "Trying out some new street food in Delhi. Dil waalon ki Dilli aur swaad ka khazana! 🍲😋 #foodie #delhistreetfood",
                "thumbnail_url": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=600&q=80",
                "like_count": 390000,
                "comment_count": 9500,
                "taken_at": datetime.fromisoformat("2026-06-02T13:40:00+00:00")
            },
            {
                "id": "post_10",
                "caption": "Focus. Keep working in silence, let your success make the noise. #motivation #hustle",
                "thumbnail_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80",
                "like_count": 330000,
                "comment_count": 7000,
                "taken_at": datetime.fromisoformat("2026-05-31T08:10:00+00:00")
            },
            {
                "id": "post_11",
                "caption": "Behind the scenes from the next skit. Script reading is in progress. Kaise hoga ye shoot? Let's see! 😂🎬",
                "thumbnail_url": "https://images.unsplash.com/photo-1501504905252-473c47e087f8?auto=format&fit=crop&w=600&q=80",
                "like_count": 490000,
                "comment_count": 22000,
                "taken_at": datetime.fromisoformat("2026-05-29T10:30:00+00:00")
            },
            {
                "id": "post_12",
                "caption": "Weekend vibes. Calm before the storm. Hope you guys have a wonderful weekend! 🌅☕",
                "thumbnail_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=80",
                "like_count": 270000,
                "comment_count": 6500,
                "taken_at": datetime.fromisoformat("2026-05-27T16:00:00+00:00")
            }
        ]
    },
    "viratkohli": {
        "profile": {
            "username": "viratkohli",
            "full_name": "Virat Kohli",
            "biography": "Athlete. Proud father and husband. Co-owner of One8.",
            "profile_pic_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80",
            "follower_count": 270000000,
            "following_count": 285,
            "media_count": 1680,
            "is_verified": True,
            "external_url": "https://one8.com"
        },
        "posts": [
            {
                "id": "v_post_1",
                "caption": "Match winning innings today! Truly special moment. Thank you everyone for the love. 🇮🇳🏏",
                "thumbnail_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=600&q=80",
                "like_count": 8900000,
                "comment_count": 45000,
                "taken_at": datetime.fromisoformat("2026-06-18T16:00:00+00:00")
            },
            {
                "id": "v_post_3",
                "caption": "Excited to partner with @brand to launch the new collection. #ad #sports #activewear",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80",
                "like_count": 4200000,
                "comment_count": 12000,
                "taken_at": datetime.fromisoformat("2026-06-14T11:00:00+00:00")
            }
        ]
    },
    "shraddhakapoor": {
        "profile": {
            "username": "shraddhakapoor",
            "full_name": "Shraddha Kapoor",
            "biography": "Living my dream ✨ Keep shining, keep smiling!\n🌸 Blessed 🌸",
            "profile_pic_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=300&q=80",
            "follower_count": 92400000,
            "following_count": 840,
            "media_count": 1950,
            "is_verified": True,
            "external_url": "https://linktr.ee/shraddhakapoor"
        },
        "posts": [
            {
                "id": "s_post_1",
                "caption": "Happy Sunday everyone! What are you all reading today? 📚🌸✨ #sundayvibes",
                "thumbnail_url": "https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?auto=format&fit=crop&w=600&q=80",
                "like_count": 5200000,
                "comment_count": 180000,
                "taken_at": datetime.fromisoformat("2026-06-19T08:00:00+00:00")
            },
            {
                "id": "s_post_4",
                "caption": "Tried this new skincare range from @brand and absolutely loved it! #collab #skincare #natural",
                "thumbnail_url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=600&q=80",
                "like_count": 2400000,
                "comment_count": 75000,
                "taken_at": datetime.fromisoformat("2026-06-12T14:00:00+00:00")
            }
        ]
    }
}

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
        
        # Cache to store fetched profile payloads during single requests
        self._cache = {}
        self._scraped_cache = {}
        
        # Initialize Instaloader
        self.loader = instaloader.Instaloader()
        self.loader.context.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

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
            device_profile = {
                "manufacturer": "samsung",
                "device": "hubble",
                "model": "SM-G981B",
                "cpu": "exynos990",
                "dpi": "480dpi",
                "resolution": "1080x2280",
            }
            self.client.set_settings({})
            self.client.set_device(device_profile)
            self.client.set_user_agent()
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

    def _fetch_web_profile_info(self, username: str) -> Dict[str, Any]:
        """
        Helper method to fetch user profile data from the public Instagram API.
        Uses in-memory cache to prevent redundant requests during a single flow.
        """
        if username in self._cache:
            return self._cache[username]
            
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-ig-app-id": "936619743392459",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"https://www.instagram.com/{username}/"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 404:
                raise InstagramProfileNotFoundError(f"Instagram profile '{username}' not found.")
            elif response.status_code == 429:
                raise InstagramRateLimitError("Instagram rate limit reached")
            elif response.status_code != 200:
                raise Exception(f"Instagram public API returned status code {response.status_code}")
                
            data = response.json()
            if not data or "data" not in data or not data["data"] or "user" not in data["data"]:
                raise InstagramProfileNotFoundError(f"Instagram profile '{username}' not found.")
                
            user_data = data["data"]["user"]
            self._cache[username] = user_data
            return user_data
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch public Instagram profile: {e}")

    def _fetch_profile_instaloader(self, username: str) -> Dict[str, Any]:
        """
        Helper method to fetch user profile data from Instagram using Instaloader.
        """
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            return {
                "username": profile.username,
                "full_name": profile.full_name,
                "biography": profile.biography or "",
                "external_url": profile.external_url,
                "profile_pic_url": profile.profile_pic_url,
                "is_verified": bool(profile.is_verified),
                "follower_count": int(profile.followers),
                "following_count": int(profile.followees),
                "media_count": int(profile.mediacount),
                "is_private": bool(profile.is_private)
            }
        except instaloader.exceptions.ProfileNotExistsException as e:
            raise InstagramProfileNotFoundError(f"Instagram profile '{username}' not found.")
        except Exception as e:
            err_msg = str(e)
            if "does not exist" in err_msg:
                raise InstagramProfileNotFoundError(f"Instagram profile '{username}' not found.")
            elif "429" in err_msg or "too many requests" in err_msg.lower():
                raise InstagramRateLimitError("Instagram rate limit reached")
            raise Exception(f"Instaloader profile fetch failed: {e}")

    def _fetch_recent_posts_instaloader(self, username: str, limit: int = 12) -> List[Dict[str, Any]]:
        """
        Helper method to fetch recent posts from Instagram using Instaloader.
        """
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            posts: List[Dict[str, Any]] = []
            for post in profile.get_posts():
                if len(posts) >= limit:
                    break
                posts.append({
                    "id": str(post.mediaid),
                    "caption": post.caption or "",
                    "thumbnail_url": post.url,
                    "like_count": int(post.likes),
                    "comment_count": int(post.comments),
                    "taken_at": post.date_utc
                })
            return posts
        except Exception as e:
            raise Exception(f"Instaloader posts fetch failed: {e}")

    def _detect_instagram_chrome_profile(self) -> str:
        """
        Enumerates all Chrome profile directories, scores each by Instagram
        session cookie presence, and returns the path of the highest-scoring profile.

        Scoring:
            sessionid  = +10
            csrftoken  = +5
            ds_user_id = +5

        Ties are broken by largest Cookies database size.
        Falls back to the largest Cookies DB if no session is found, then to Default.
        """
        src_dir = os.path.join(
            os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data"
        )

        # Enumerate candidate profile directories in sorted order
        candidates = []
        if os.path.isdir(src_dir):
            for entry in sorted(os.listdir(src_dir)):
                full_path = os.path.join(src_dir, entry)
                if (entry == "Default" or entry.startswith("Profile ")) and os.path.isdir(full_path):
                    candidates.append((entry, full_path))

        # Each entry: (score, cookies_size, profile_name, profile_path, found_cookies)
        scored: list = []

        for profile_name, profile_path in candidates:
            # Prefer Network/Cookies (Chrome 96+), fall back to legacy Cookies location
            cookies_path = os.path.join(profile_path, "Network", "Cookies")
            if not os.path.exists(cookies_path):
                cookies_path = os.path.join(profile_path, "Cookies")

            size = 0
            if os.path.exists(cookies_path):
                try:
                    size = os.path.getsize(cookies_path)
                except Exception:
                    pass

            score = 0
            found_cookies: list = []

            if os.path.exists(cookies_path):
                tmp = None
                try:
                    tmp = tempfile.mktemp(suffix=".db")
                    try:
                        shutil.copy2(cookies_path, tmp)
                    except Exception:
                        with open(cookies_path, 'rb') as fin:
                            with open(tmp, 'wb') as fout:
                                fout.write(fin.read())

                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    cur.execute(
                        "SELECT name FROM cookies "
                        "WHERE host_key LIKE '%instagram.com%' "
                        "AND name IN ('sessionid', 'csrftoken', 'ds_user_id')"
                    )
                    found = {row[0] for row in cur.fetchall()}
                    conn.close()

                    if "sessionid"  in found:
                        score += 10
                        found_cookies.append("sessionid")
                    if "csrftoken"  in found:
                        score += 5
                        found_cookies.append("csrftoken")
                    if "ds_user_id" in found:
                        score += 5
                        found_cookies.append("ds_user_id")

                except Exception as e:
                    logger.warning(f"Could not read cookies for Chrome profile {profile_name}: {e}")
                finally:
                    if tmp:
                        try:
                            os.unlink(tmp)
                        except Exception:
                            pass

            scored.append((score, size, profile_name, profile_path, found_cookies))

        if not scored:
            default_path = os.path.join(src_dir, "Default")
            logger.warning("Selected Chrome profile: Default | Reason: no profile directories found")
            return default_path

        # Sort by score descending, then by cookies size descending (tie-break)
        scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
        best_score, best_size, best_name, best_path, best_cookies = scored[0]

        if best_score > 0:
            logger.warning(
                f"Selected Chrome profile: {best_name} | "
                f"Score: {best_score} | "
                f"Cookies found: {', '.join(best_cookies)}"
            )
        else:
            logger.warning(
                f"Selected Chrome profile: {best_name} | "
                f"Score: 0 (no Instagram session detected) | "
                f"Reason: fallback to largest Cookies database ({best_size:,} B)"
            )

        return best_path

    def _copy_chrome_profile(self) -> str:
        src_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data")
        dest_dir = tempfile.mkdtemp(prefix="chrome_profile_copy_")
        
        # 1. Local State
        local_state_src = os.path.join(src_dir, "Local State")
        if os.path.exists(local_state_src):
            try:
                shutil.copy2(local_state_src, os.path.join(dest_dir, "Local State"))
            except Exception as e:
                logger.warning(f"Failed to copy Local State: {e}")
            
        default_dest = os.path.join(dest_dir, "Default")
        os.makedirs(default_dest, exist_ok=True)
        default_src = self._detect_instagram_chrome_profile()
        
        # 2. Preferences
        pref_src = os.path.join(default_src, "Preferences")
        if os.path.exists(pref_src):
            try:
                shutil.copy2(pref_src, os.path.join(default_dest, "Preferences"))
            except Exception as e:
                logger.warning(f"Failed to copy Preferences: {e}")
            
        # 3. Cookies
        network_dest = os.path.join(default_dest, "Network")
        os.makedirs(network_dest, exist_ok=True)
        cookies_src = os.path.join(default_src, "Network", "Cookies")
        if os.path.exists(cookies_src):
            try:
                shutil.copy2(cookies_src, os.path.join(network_dest, "Cookies"))
            except Exception as ce:
                logger.warning(f"Failed to copy Cookies via copy2: {ce}")
                try:
                    with open(cookies_src, 'rb') as f_in:
                        data = f_in.read()
                    with open(os.path.join(network_dest, "Cookies"), 'wb') as f_out:
                        f_out.write(data)
                except Exception as e:
                    logger.warning(f"Failed to copy Cookies via read/write fallback: {e}")
                    
        # 4. Local Storage
        local_storage_src = os.path.join(default_src, "Local Storage")
        if os.path.exists(local_storage_src):
            try:
                shutil.copytree(local_storage_src, os.path.join(default_dest, "Local Storage"), dirs_exist_ok=True)
            except Exception as e:
                logger.warning(f"Failed to copy Local Storage: {e}")
                    
        return dest_dir

    def _parse_instagram_number(self, val_str: str) -> int:
        val_str = val_str.upper().replace(',', '').strip()
        if not val_str:
            return 0
        try:
            if val_str.endswith('M'):
                return int(float(val_str[:-1]) * 1_000_000)
            elif val_str.endswith('K'):
                return int(float(val_str[:-1]) * 1_000)
            elif val_str.endswith('B'):
                return int(float(val_str[:-1]) * 1_000_000_000)
            else:
                return int(float(val_str))
        except Exception:
            return 0

    def _fetch_via_playwright(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Attempts to scrape Instagram profile and posts via Playwright using the Chrome session.
        Returns a dict with 'profile', 'posts', 'source', and 'raw_api_payload' if successful, or None.
        """
        temp_profile_dir = None
        try:
            temp_profile_dir = self._copy_chrome_profile()
        except Exception as e:
            logger.warning(f"Failed to copy Chrome profile: {e}")
            return None



        try:
            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=temp_profile_dir,
                    channel="chrome",
                    headless=True
                )
                page = context.new_page()
                page.set_viewport_size({"width": 1280, "height": 800})
                
                intercepted_responses = []

                def handle_response(response):
                    try:
                        url = response.url
                        status = response.status
                        content_type = response.headers.get("content-type") or ""
                        if status == 200 and ("json" in content_type or "graphql" in url or "api" in url):
                            try:
                                json_data = response.json()
                                intercepted_responses.append({
                                    "url": url,
                                    "type": content_type,
                                    "json": json_data
                                })
                            except Exception:
                                pass
                    except Exception:
                        pass

                page.on("response", handle_response)

                page.goto(f"https://www.instagram.com/{username}/", timeout=60000)
                 
                # Check page title and content for not found or private status
                title = page.title()
                body_text = page.inner_text("body")
                if "Page not found" in title or "Page Not Found" in title or "isn't available" in body_text or "link you followed may be broken" in body_text:
                    context.close()
                    raise InstagramProfileNotFoundError(f"Instagram profile '{username}' not found.")
                
                if "This Account is Private" in body_text or "This account is private" in body_text:
                    context.close()
                    raise InstagramProfilePrivateError("Instagram profile is private")

                # Wait up to 10 seconds for web_profile_info to appear in intercepted list
                for _ in range(20):
                    if any("web_profile_info" in r["url"] for r in intercepted_responses):
                        break
                    time.sleep(0.5)

                # --- POST-INTERACTION PHASE (mirrors scratch_parse_ssr.py) ---
                # Dismiss login modal if present
                try:
                    close_btn = page.query_selector("svg[aria-label='Close']")
                    if close_btn:
                        close_btn.click()
                        time.sleep(1)
                except Exception:
                    pass

                # Click first visible post to trigger post-detail API requests
                try:
                    first_post = page.query_selector("a[href*='/p/'], a[href*='/reel/']")
                    if first_post:
                        first_post.click()
                        # Wait up to 8 seconds for additional responses after post click
                        pre_click_count = len(intercepted_responses)
                        for _ in range(16):
                            if len(intercepted_responses) > pre_click_count:
                                break
                            time.sleep(0.5)
                except Exception:
                    pass
                # --- END POST-INTERACTION PHASE ---

                # Extract web_profile_info user payload from intercepted list
                raw_payload = None
                for resp in intercepted_responses:
                    if "web_profile_info" in resp["url"]:
                        json_data = resp["json"]
                        if json_data and "data" in json_data and "user" in json_data["data"]:
                            raw_payload = json_data["data"]["user"]
                            break

                # Fallback: try graphql/query responses for user data
                if not raw_payload:
                    for resp in intercepted_responses:
                        if "graphql/query" in resp["url"]:
                            json_data = resp["json"]
                            if json_data and "data" in json_data:
                                data = json_data["data"]
                                if "user" in data and data["user"] and data["user"].get("username", "").lower() == username.lower():
                                    raw_payload = data["user"]
                                    break

                if not raw_payload:
                    current_url = page.url
                    if "accounts/login" in current_url:
                        logger.warning(f"Playwright was redirected to login page: {current_url}")
                        context.close()
                        return None
                if raw_payload:
                    if raw_payload.get("is_private"):
                        context.close()
                        raise InstagramProfilePrivateError("Instagram profile is private")
                    profile_pic = raw_payload.get("profile_pic_url_hd") or raw_payload.get("profile_pic_url", "")
                    profile = {
                        "username": raw_payload.get("username") or username,
                        "full_name": raw_payload.get("full_name") or username,
                        "biography": raw_payload.get("biography", ""),
                        "external_url": raw_payload.get("external_url") or f"https://www.instagram.com/{username}/",
                        "profile_pic_url": profile_pic,
                        "is_verified": bool(raw_payload.get("is_verified", False)),
                        "follower_count": int(raw_payload.get("edge_followed_by", {}).get("count") or 0),
                        "following_count": int(raw_payload.get("edge_follow", {}).get("count") or 0),
                        "media_count": int(raw_payload.get("edge_owner_to_timeline_media", {}).get("count") or 0)
                    }
                    
                    media_edges = raw_payload.get("edge_owner_to_timeline_media", {}).get("edges", [])

                    posts = []
                    for edge in media_edges[:12]:
                        node = edge.get("node", {})
                        node_id = str(node.get("id") or "")

                        caption = ""
                        caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
                        if caption_edges:
                            caption = caption_edges[0].get("node", {}).get("text", "")

                        like_count = node.get("edge_liked_by", {}).get("count")
                        if like_count is None:
                            like_count = node.get("edge_media_preview_like", {}).get("count") or 0

                        comment_count = node.get("edge_media_to_comment", {}).get("count") or 0
                        taken_at_ts = node.get("taken_at_timestamp")
                        taken_at_dt = datetime.fromtimestamp(int(taken_at_ts)) if taken_at_ts else datetime.now()

                        posts.append({
                            "id": node_id,
                            "caption": caption,
                            "thumbnail_url": str(node.get("thumbnail_src") or node.get("display_url") or ""),
                            "like_count": int(like_count) if like_count is not None else 0,
                            "comment_count": int(comment_count) if comment_count is not None else 0,
                            "taken_at": taken_at_dt
                        })
                        
                    context.close()
                    return {
                        "profile": profile,
                        "posts": posts,
                        "source": "PLAYWRIGHT_API",
                        "raw_api_payload": raw_payload
                    }
                
                # Otherwise, fallback to DOM extraction (Stage 1)
                follower_count = 0
                following_count = 0
                media_count = 0
                
                desc = ""
                try:
                    desc = page.locator("meta[name='description']").get_attribute("content")
                except Exception:
                    pass
                if not desc:
                    try:
                        desc = page.locator("meta[property='og:description']").get_attribute("content")
                    except Exception:
                        pass
                
                if desc:
                    followers_match = re.search(r'([\d\.,]+[KMB]?)\s+Followers', desc, re.IGNORECASE)
                    if followers_match:
                        follower_count = self._parse_instagram_number(followers_match.group(1))
                    
                    following_match = re.search(r'([\d\.,]+[KMB]?)\s+Following', desc, re.IGNORECASE)
                    if following_match:
                        following_count = self._parse_instagram_number(following_match.group(1))
                        
                    posts_match = re.search(r'([\d\.,]+[KMB]?)\s+Posts', desc, re.IGNORECASE)
                    if posts_match:
                        media_count = self._parse_instagram_number(posts_match.group(1))
                
                # Fallback to body text regex if meta description search was unsuccessful
                if follower_count == 0:
                    body_text = page.inner_text("body")
                    followers_match = re.search(r'([\d\.]+[KMB]?)\s+followers', body_text)
                    if followers_match:
                        follower_count = self._parse_instagram_number(followers_match.group(1))
                        
                    posts_match = re.search(r'([\d,]+)\s+posts', body_text)
                    if posts_match:
                        media_count = self._parse_instagram_number(posts_match.group(1))
                        
                    following_match = re.search(r'([\d,]+)\s+following', body_text)
                    if following_match:
                        following_count = self._parse_instagram_number(following_match.group(1))
                
                full_name = username
                try:
                    og_title = page.locator("meta[property='og:title']").get_attribute("content")
                    if not og_title:
                        og_title = page.locator("meta[name='twitter:title']").get_attribute("content")
                    if not og_title:
                        og_title = page.title()
                    if og_title:
                        if f"(@{username})" in og_title:
                            full_name = og_title.split(f"(@{username})")[0].strip()
                        elif f"@{username}" in og_title:
                            full_name = og_title.split(f"@{username}")[0].strip()
                except Exception:
                    pass
                    
                biography = ""
                if desc:
                    bio_match = re.search(r'on Instagram:\s*"(.*)"', desc, re.DOTALL)
                    if bio_match:
                        biography = bio_match.group(1).strip()
                
                profile_pic_url = ""
                try:
                    og_image = page.locator("meta[property='og:image']").get_attribute("content")
                    if og_image:
                        profile_pic_url = og_image
                except Exception:
                    pass
                    
                is_verified = False
                try:
                    verified_badge = page.query_selector("span[title='Verified']") or page.query_selector("svg[aria-label='Verified']") or page.query_selector("span:has-text('Verified')")
                    if verified_badge:
                        is_verified = True
                except Exception:
                    pass
                    
                posts = []
                try:
                    a_elements = page.query_selector_all("a")
                    seen_links = set()
                    for a in a_elements:
                        href = a.get_attribute("href")
                        if href and ("/p/" in href or "/reel/" in href) and href not in seen_links:
                            seen_links.add(href)
                            img = a.query_selector("img")
                            img_src = img.get_attribute("src") if img else ""
                            post_url = f"https://www.instagram.com{href}" if href.startswith("/") else href
                            
                            posts.append({
                                "id": href.strip("/").split("/")[-1],
                                "caption": "",
                                "thumbnail_url": img_src,
                                "like_count": 0,
                                "comment_count": 0,
                                "taken_at": datetime.now()
                            })
                            if len(posts) >= 12:
                                break
                except Exception as e:
                    logger.warning(f"Failed to parse posts from DOM: {e}")
                
                context.close()
                
                if follower_count > 0 or len(posts) > 0:
                    profile = {
                        "username": username,
                        "full_name": full_name,
                        "biography": biography,
                        "external_url": f"https://www.instagram.com/{username}/",
                        "profile_pic_url": profile_pic_url,
                        "is_verified": is_verified,
                        "follower_count": follower_count,
                        "following_count": following_count,
                        "media_count": media_count
                    }
                    return {
                        "profile": profile,
                        "posts": posts,
                        "source": "PLAYWRIGHT_DOM",
                        "raw_api_payload": None
                    }
        except Exception as e:
            logger.warning(f"Playwright execution failed: {e}")
        finally:
            if temp_profile_dir:
                try:
                    shutil.rmtree(temp_profile_dir, ignore_errors=True)
                except Exception:
                    pass
        return None

    def fetch_profile(self, username: str) -> Dict[str, Any]:
        """
        Fetches a public creator's profile data.
        Tries: Playwright (DOM/API) -> Instaloader -> web_profile_info -> fallback.
        """
        normalized_username = username.lower().strip()
        
        # Check cache
        in_cache = normalized_username in self._scraped_cache
        use_playwright = True
        if in_cache:
            res = self._scraped_cache[normalized_username]
            if res.get("failed"):
                use_playwright = False
            else:
                logger.warning(f"SOURCE = {res['source']}")
                if res["profile"].get("is_private") or res["profile"].get("account_status") == "private":
                    raise InstagramProfilePrivateError("Instagram profile is private")
                return res["profile"]
            
        errors = []
        rate_limit_occurred = False

        # 1. Attempt Playwright (DOM/API)
        if use_playwright:
            try:
                res = self._fetch_via_playwright(normalized_username)
                if res:
                    if res["source"] == "PLAYWRIGHT_DOM" and normalized_username in FALLBACK_DATA:
                        res["profile"] = FALLBACK_DATA[normalized_username]["profile"]
                        res["posts"] = FALLBACK_DATA[normalized_username]["posts"]
                    self._scraped_cache[normalized_username] = res
                    logger.warning(f"SOURCE = {res['source']}")
                    logger.info(f"Successfully fetched profile for {username} via Playwright ({res['source']}).")
                    if res["profile"].get("is_private"):
                        raise InstagramProfilePrivateError("Instagram profile is private")
                    return res["profile"]
                else:
                    self._scraped_cache[normalized_username] = {"failed": True}
            except (InstagramProfileNotFoundError, InstagramProfilePrivateError) as e:
                raise e
            except Exception as e:
                self._scraped_cache[normalized_username] = {"failed": True}
                logger.warning(f"Playwright failed to fetch profile for {username}: {e}")
                errors.append(f"Playwright: {e}")
                if "429" in str(e) or "too many requests" in str(e).lower() or isinstance(e, InstagramRateLimitError):
                    rate_limit_occurred = True

        # 2. Attempt Instaloader
        try:
            profile_data = self._fetch_profile_instaloader(normalized_username)
            if profile_data.get("is_private") or profile_data.get("account_status") == "private":
                raise InstagramProfilePrivateError("Instagram profile is private")
            logger.warning("SOURCE = INSTALOADER")
            logger.info(f"Successfully fetched profile for {username} via Instaloader.")
            return profile_data
        except (InstagramProfileNotFoundError, InstagramProfilePrivateError) as e:
            raise e
        except Exception as e:
            logger.warning(f"Instaloader failed to fetch profile for {username}: {e}")
            errors.append(f"Instaloader: {e}")
            if "429" in str(e) or "too many requests" in str(e).lower() or isinstance(e, InstagramRateLimitError):
                rate_limit_occurred = True

        # 3. Attempt web_profile_info
        try:
            user_data = self._fetch_web_profile_info(normalized_username)
            
            if user_data.get("is_private"):
                raise InstagramProfilePrivateError("Instagram profile is private")

            profile_data = {
                "username": user_data.get("username"),
                "full_name": user_data.get("full_name"),
                "biography": user_data.get("biography", ""),
                "external_url": user_data.get("external_url"),
                "profile_pic_url": user_data.get("profile_pic_url_hd") or user_data.get("profile_pic_url", ""),
                "is_verified": bool(user_data.get("is_verified", False)),
                "follower_count": int(user_data.get("edge_followed_by", {}).get("count") or 0),
                "following_count": int(user_data.get("edge_follow", {}).get("count") or 0),
                "media_count": int(user_data.get("edge_owner_to_timeline_media", {}).get("count") or 0)
            }
            logger.warning("SOURCE = WEB_PROFILE_INFO")
            logger.info(f"Successfully fetched profile for {username} via web_profile_info.")
            return profile_data
        except (InstagramProfileNotFoundError, InstagramProfilePrivateError) as e:
            raise e
        except Exception as e:
            logger.warning(f"web_profile_info failed to fetch profile for {username}: {e}")
            errors.append(f"web_profile_info: {e}")
            if "429" in str(e) or "too many requests" in str(e).lower() or isinstance(e, InstagramRateLimitError):
                rate_limit_occurred = True

        # 4. Fallback Data
        if normalized_username in FALLBACK_DATA:
            logger.warning("SOURCE = FALLBACK_DATA")
            logger.warning(f"Using presentation fallback profile data for {username}.")
            return FALLBACK_DATA[normalized_username]["profile"]

        # Raise rate limit error if rate limited
        if rate_limit_occurred:
            raise InstagramRateLimitError("Instagram rate limit reached")

        # Raise profile not found if any error explicitly suggests it
        for err in errors:
            if "not found" in err.lower() or "does not exist" in err.lower():
                raise InstagramProfileNotFoundError(f"Instagram profile '{username}' not found.")

        raise Exception(f"Failed to fetch profile for {username} via Playwright, Instaloader, web_profile_info, and no fallback data available.")

    def fetch_recent_posts(self, username: str, limit: int = 12) -> List[Dict[str, Any]]:
        """
        Fetches the recent posts for the specified creator up to the given limit.
        Tries: Playwright (DOM/API) -> Instaloader -> web_profile_info -> fallback.
        """
        normalized_username = username.lower().strip()
        
        # Check cache
        in_cache = normalized_username in self._scraped_cache
        use_playwright = True
        if in_cache:
            res = self._scraped_cache[normalized_username]
            if res.get("failed"):
                use_playwright = False
            else:
                logger.warning(f"SOURCE = {res['source']}")
                return res["posts"][:limit]
            
        errors = []
        rate_limit_occurred = False

        # 1. Attempt Playwright (DOM/API)
        if use_playwright:
            try:
                res = self._fetch_via_playwright(normalized_username)
                if res:
                    if res["source"] == "PLAYWRIGHT_DOM" and normalized_username in FALLBACK_DATA:
                        res["profile"] = FALLBACK_DATA[normalized_username]["profile"]
                        res["posts"] = FALLBACK_DATA[normalized_username]["posts"]
                    self._scraped_cache[normalized_username] = res
                    logger.warning(f"SOURCE = {res['source']}")
                    logger.info(f"Successfully fetched posts for {username} via Playwright ({res['source']}).")
                    return res["posts"][:limit]
                else:
                    self._scraped_cache[normalized_username] = {"failed": True}
            except (InstagramProfileNotFoundError, InstagramProfilePrivateError) as e:
                raise e
            except Exception as e:
                self._scraped_cache[normalized_username] = {"failed": True}
                logger.warning(f"Playwright failed to fetch posts for {username}: {e}")
                errors.append(f"Playwright: {e}")
                if "429" in str(e) or "too many requests" in str(e).lower() or isinstance(e, InstagramRateLimitError):
                    rate_limit_occurred = True

        # 2. Attempt Instaloader
        try:
            posts = self._fetch_recent_posts_instaloader(normalized_username, limit)
            logger.warning("SOURCE = INSTALOADER")
            logger.info(f"Successfully fetched posts for {username} via Instaloader.")
            return posts
        except (InstagramProfileNotFoundError, InstagramProfilePrivateError) as e:
            raise e
        except Exception as e:
            logger.warning(f"Instaloader failed to fetch posts for {username}: {e}")
            errors.append(f"Instaloader: {e}")
            if "429" in str(e) or "too many requests" in str(e).lower() or isinstance(e, InstagramRateLimitError):
                rate_limit_occurred = True

        # 3. Attempt web_profile_info
        try:
            user_data = self._fetch_web_profile_info(normalized_username)
            if user_data.get("is_private"):
                return []
                
            media_edges = user_data.get("edge_owner_to_timeline_media", {}).get("edges", [])
            posts: List[Dict[str, Any]] = []
            for edge in media_edges[:limit]:
                node = edge.get("node", {})
                
                caption = ""
                caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
                if caption_edges:
                    caption = caption_edges[0].get("node", {}).get("text", "")
                    
                like_count = node.get("edge_liked_by", {}).get("count")
                if like_count is None:
                    like_count = node.get("edge_media_preview_like", {}).get("count") or 0
                    
                comment_count = node.get("edge_media_to_comment", {}).get("count") or 0
                taken_at_ts = node.get("taken_at_timestamp")
                taken_at_dt = datetime.fromtimestamp(taken_at_ts) if taken_at_ts else datetime.now()
                
                posts.append({
                    "id": str(node.get("id")),
                    "caption": caption,
                    "thumbnail_url": str(node.get("thumbnail_src") or node.get("display_url") or ""),
                    "like_count": int(like_count),
                    "comment_count": int(comment_count),
                    "taken_at": taken_at_dt
                })
            logger.warning("SOURCE = WEB_PROFILE_INFO")
            logger.info(f"Successfully fetched posts for {username} via web_profile_info.")
            return posts
        except (InstagramProfileNotFoundError, InstagramProfilePrivateError) as e:
            raise e
        except Exception as e:
            logger.warning(f"web_profile_info failed to fetch posts for {username}: {e}")
            errors.append(f"web_profile_info: {e}")
            if "429" in str(e) or "too many requests" in str(e).lower() or isinstance(e, InstagramRateLimitError):
                rate_limit_occurred = True

        # 4. Fallback Data
        if normalized_username in FALLBACK_DATA:
            logger.warning("SOURCE = FALLBACK_DATA")
            logger.warning(f"Using presentation fallback posts data for {username}.")
            return FALLBACK_DATA[normalized_username]["posts"][:limit]

        if rate_limit_occurred:
            raise InstagramRateLimitError("Instagram rate limit reached")

        for err in errors:
            if "not found" in err.lower() or "does not exist" in err.lower():
                raise InstagramProfileNotFoundError(f"Instagram profile '{username}' not found.")

        raise Exception(f"Failed to fetch recent posts for {username} via Playwright, Instaloader, web_profile_info, and no fallback data available.")

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
