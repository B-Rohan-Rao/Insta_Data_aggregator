import os
import shutil
import tempfile
import sys
import time
from playwright.sync_api import sync_playwright

def copy_chrome_profile():
    src_dir = r"C:\Users\Win11\AppData\Local\Google\Chrome\User Data"
    dest_dir = tempfile.mkdtemp(prefix="chrome_profile_ssr_dump_")
    
    # 1. Local State
    local_state_src = os.path.join(src_dir, "Local State")
    if os.path.exists(local_state_src):
        shutil.copy2(local_state_src, os.path.join(dest_dir, "Local State"))
        
    default_dest = os.path.join(dest_dir, "Default")
    os.makedirs(default_dest, exist_ok=True)
    default_src = os.path.join(src_dir, "Default")
    
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
            
            print("Navigating to carryminati...")
            page.goto("https://www.instagram.com/carryminati/", timeout=60000)
            time.sleep(5)
            
            scripts = page.query_selector_all("script")
            print(f"Found {len(scripts)} script tags in total.")
            
            for i, script in enumerate(scripts):
                text = script.inner_text() or ""
                # Check if it has biography or followers in it
                if "biography" in text or "followers" in text or "media" in text:
                    script_type = script.get_attribute("type") or "text/javascript"
                    print(f"\n--- Script {i} | type={script_type} | length={len(text)} ---")
                    print(text[:1000])
                    print("--------------------------------------------------")
            
            context.close()
    finally:
        shutil.rmtree(temp_profile_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
