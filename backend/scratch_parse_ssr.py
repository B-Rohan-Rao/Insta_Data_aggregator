import os
import shutil
import tempfile
import sys
import time
import json
from playwright.sync_api import sync_playwright

def copy_chrome_profile():
    src_dir = r"C:\Users\Win11\AppData\Local\Google\Chrome\User Data"
    dest_dir = tempfile.mkdtemp(prefix="chrome_profile_network_")
    
    # 1. Local State
    local_state_src = os.path.join(src_dir, "Local State")
    if os.path.exists(local_state_src):
        shutil.copy2(local_state_src, os.path.join(dest_dir, "Local State"))
        
    default_dest = os.path.join(dest_dir, "Default")
    os.makedirs(default_dest, exist_ok=True)
    default_src = os.path.join(src_dir, "Profile 1")
    
    # 2. Preferences
    pref_src = os.path.join(default_src, "Preferences")
    if os.path.exists(pref_src):
        shutil.copy2(pref_src, os.path.join(default_dest, "Preferences"))
        
    # 3. Cookies
    network_dest = os.path.join(default_dest, "Network")
    os.makedirs(network_dest, exist_ok=True)
    cookies_src = os.path.join(default_src, "Network", "Cookies")
    if os.path.exists(cookies_src):
        shutil.copy2(cookies_src, os.path.join(network_dest, "Cookies"))
        
    return dest_dir

def find_metrics_recursive(data, path="root"):
    matches = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k in ["edge_liked_by", "edge_media_preview_like", "edge_media_to_comment", "taken_at_timestamp", "taken_at", "like_count", "comment_count"]:
                matches.append((f"{path} -> {k}", str(v)))
            matches.extend(find_metrics_recursive(v, f"{path} -> {k}"))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            matches.extend(find_metrics_recursive(item, f"{path}[{idx}]"))
    return matches

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
        
    temp_profile_dir = copy_chrome_profile()
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
            all_urls_intercepted = []
            
            def handle_response(response):
                try:
                    url = response.url
                    status = response.status
                    content_type = response.headers.get("content-type") or ""
                    all_urls_intercepted.append(f"{url} ({status}, {content_type})")
                    
                    if "json" in content_type or "graphql" in url or "api" in url:
                        try:
                            # We try to get response body/json
                            text = response.text()
                            intercepted_responses.append({
                                "url": url,
                                "status": status,
                                "type": content_type,
                                "body": text
                            })
                        except Exception:
                            pass
                except Exception:
                    pass
            
            page.on("response", handle_response)
            
            print("--- PHASE 1: Loading Profile Page ---")
            page.goto("https://www.instagram.com/adityasaidwhat/", timeout=60000)
            time.sleep(5)
            
            # Dismiss login modal if present to reveal posts
            try:
                close_btn = page.query_selector("svg[aria-label='Close']") or page.query_selector("svg[aria-label='Close']").parent
                if close_btn:
                    print("Found close button for login modal, clicking it...")
                    close_btn.click()
                    time.sleep(2)
            except Exception as e:
                print(f"Could not click close button: {e}")
                
            print(f"Captured {len(intercepted_responses)} JSON/API/GraphQL responses during load.")
            
            print("\n--- PHASE 2: Clicking First Post ---")
            first_post_link = page.query_selector("a[href*='/p/'], a[href*='/reel/']")
            if first_post_link:
                href = first_post_link.get_attribute("href")
                print(f"Found first post link: {href}. Clicking it...")
                
                # Click the post and wait
                first_post_link.click()
                time.sleep(6)
                
            final_url = page.url
            print(f"Page URL after click/navigation: {final_url}")
            
            # Audit of captured data
            web_profile_info_body = None
            web_profile_info_found = False
            for resp in intercepted_responses:
                if "web_profile_info" in resp["url"]:
                    web_profile_info_found = True
                    web_profile_info_body = resp["body"]
                    break
                    
            # Check for strings anywhere in intercepted bodies
            all_text_combined = " ".join([resp["body"] for resp in intercepted_responses if resp["body"]])
            edge_liked_by_present = "edge_liked_by" in all_text_combined
            edge_media_to_comment_present = "edge_media_to_comment" in all_text_combined
            taken_at_timestamp_present = "taken_at_timestamp" in all_text_combined
            
            print("\n================ REPORT START ================")
            print(f"1. FINAL URL: {final_url}")
            print(f"2. TOTAL INTERCEPTED RESPONSES: {len(all_urls_intercepted)}")
            print("3. EVERY INTERCEPTED URL:")
            for u in all_urls_intercepted:
                print(f"   - {u}")
            print(f"4. WHETHER WEB_PROFILE_INFO APPEARS: {web_profile_info_found}")
            print("5. FULL BODY OF WEB_PROFILE_INFO RESPONSE:")
            if web_profile_info_found and web_profile_info_body:
                print(web_profile_info_body)
            else:
                print("None")
            print(f"6. WHETHER EDGE_LIKED_BY APPEARS ANYWHERE: {edge_liked_by_present}")
            print(f"7. WHETHER EDGE_MEDIA_TO_COMMENT APPEARS ANYWHERE: {edge_media_to_comment_present}")
            print(f"8. WHETHER TAKEN_AT_TIMESTAMP APPEARS ANYWHERE: {taken_at_timestamp_present}")
            print("================= REPORT END =================")
            
            context.close()
    finally:
        shutil.rmtree(temp_profile_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
