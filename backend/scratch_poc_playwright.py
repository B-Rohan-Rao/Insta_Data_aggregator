import os
import shutil
import tempfile
import sys
import time
from playwright.sync_api import sync_playwright

def copy_chrome_profile():
    src_dir = r"C:\Users\Win11\AppData\Local\Google\Chrome\User Data"
    dest_dir = os.path.join(tempfile.gettempdir(), "chrome_profile_copy")
    
    print(f"Copying Chrome profile from {src_dir} to {dest_dir}...")
    
    # Clean up destination directory if it already exists
    if os.path.exists(dest_dir):
        try:
            # On Windows, files might be locked if a previous run didn't close properly.
            # We try to clean up.
            shutil.rmtree(dest_dir, ignore_errors=True)
        except Exception as e:
            print(f"Warning: Failed to clean up existing temp directory {dest_dir}: {e}")
            
    os.makedirs(dest_dir, exist_ok=True)
    
    # 1. Copy Local State (critical for encryption keys)
    local_state_src = os.path.join(src_dir, "Local State")
    if os.path.exists(local_state_src):
        shutil.copy2(local_state_src, os.path.join(dest_dir, "Local State"))
        
    default_dest = os.path.join(dest_dir, "Default")
    os.makedirs(default_dest, exist_ok=True)
    
    default_src = os.path.join(src_dir, "Default")
    
    # 2. Copy Preferences
    pref_src = os.path.join(default_src, "Preferences")
    if os.path.exists(pref_src):
        shutil.copy2(pref_src, os.path.join(default_dest, "Preferences"))
        
    # 3. Copy Cookies (under Network/Cookies)
    network_dest = os.path.join(default_dest, "Network")
    os.makedirs(network_dest, exist_ok=True)
    
    cookies_src = os.path.join(default_src, "Network", "Cookies")
    if os.path.exists(cookies_src):
        try:
            shutil.copy2(cookies_src, os.path.join(network_dest, "Cookies"))
        except Exception as ce:
            print(f"Warning: Failed to copy Cookies database (might be locked by Chrome): {ce}")
            # If copying fails due to locks, we try standard file copy
            import io
            with open(cookies_src, 'rb') as f_in:
                data = f_in.read()
            with open(os.path.join(network_dest, "Cookies"), 'wb') as f_out:
                f_out.write(data)
                
    # 4. Copy Local Storage
    local_storage_src = os.path.join(default_src, "Local Storage")
    if os.path.exists(local_storage_src):
        try:
            # We copy local storage but ignore cache/etc inside it if any
            shutil.copytree(local_storage_src, os.path.join(default_dest, "Local Storage"), dirs_exist_ok=True)
        except Exception as e:
            print(f"Warning: Failed to copy Local Storage: {e}")
            
    print("Copy completed successfully.")
    return dest_dir

def main():
    # Reconfigure stdout to support UTF-8 encoding (resolves Windows CMD/PowerShell emoji encoding crashes)
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
        
    try:
        # Copy the profile to a temp folder to bypass the open browser lock
        temp_profile_dir = copy_chrome_profile()
        
        print("\nLaunching Playwright with copied context...")
        with sync_playwright() as p:
            # We use launch_persistent_context pointing to the temp directory.
            # Running headless=True to avoid opening a browser window on screen.
            context = p.chromium.launch_persistent_context(
                user_data_dir=temp_profile_dir,
                channel="chrome",  # Use user's Chrome binary to guarantee cookie encryption key matches Chrome
                headless=True
            )
            
            page = context.new_page()
            
            # Set a standard viewport size for screenshots
            page.set_viewport_size({"width": 1280, "height": 800})
            
            print("Navigating to https://www.instagram.com/carryminati/...")
            page.goto("https://www.instagram.com/carryminati/", timeout=60000)
            
            # Wait for data/dynamic elements to load
            print("Waiting for page load and screenshot...")
            time.sleep(5)
            
            # Capture screenshot 1: General load state
            page.screenshot(path="instagram_loaded.png")
            print("Saved screenshot to instagram_loaded.png")
            
            current_url = page.url
            page_title = page.title()
            
            # Search for visible stats/headers in DOM
            profile_name = "N/A"
            follower_count = "N/A"
            media_count = "N/A"
            following_count = "N/A"
            
            try:
                # Find verified username header
                h2_elements = page.query_selector_all("h2")
                for h2 in h2_elements:
                    text = h2.inner_text()
                    if "carryminati" in text.lower():
                        profile_name = text
                        break
            except Exception:
                pass
                
            # Logged-in verification check
            body_text = page.inner_text("body")
            
            # Robust regex-based parsing on page text
            import re
            followers_match = re.search(r'([\d\.]+[KMB]?)\s+followers', body_text)
            if followers_match:
                follower_count = followers_match.group(1)
                
            posts_match = re.search(r'([\d,]+)\s+posts', body_text)
            if posts_match:
                media_count = posts_match.group(1)
                
            following_match = re.search(r'([\d,]+)\s+following', body_text)
            if following_match:
                following_count = following_match.group(1)
                
            # Instagram displays "Log In" / "Sign Up" buttons, but if we see the posts & followers,
            # it means the profile itself was successfully loaded and is fully visible.
            is_visible = follower_count != "N/A" and profile_name != "N/A"
            is_login_page = "accounts/login" in current_url
            
            # Take profile details screenshot
            page.screenshot(path="carry_profile.png")
            print("Saved screenshot to carry_profile.png")
            
            print(f"\n=== VERIFICATION REPORT ===")
            print(f"Status: {'SUCCESS' if is_visible else 'FAILURE'}")
            print(f"Final URL: {current_url}")
            print(f"Page Title: {page_title}")
            print(f"Is Login Page Redirected?: {is_login_page}")
            print(f"Is Profile Visible?: {is_visible}")
            print(f"Extracted Username: {profile_name}")
            print(f"Extracted Follower Count: {follower_count}")
            print(f"Extracted Media Count: {media_count}")
            print(f"Extracted Following Count: {following_count}")
            print(f"===========================\n")
            
            context.close()
            
            # Clean up the temp profile copy directory
            try:
                shutil.rmtree(temp_profile_dir, ignore_errors=True)
            except Exception:
                pass
                
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
