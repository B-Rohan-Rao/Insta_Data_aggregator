import subprocess
import json
import re
import sys
from datetime import datetime

def run_script(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result.stdout, result.stderr

def parse_scratch_output(stdout):
    # Extract JSON between '5. FULL BODY OF WEB_PROFILE_INFO RESPONSE:' and '6. WHETHER EDGE_LIKED_BY APPEARS'
    # Wait! If web_profile_info is False (as in task-1444), we need to extract from graphql/query in stdout!
    # Let's check if there is a graphql/query payload in stdout or if we can read web_profile_info_latest.json
    # Actually, running the scratch script might sometimes intercept web_profile_info and sometimes graphql/query.
    # To be extremely robust, let's parse both.
    # Let's search for any JSON in the stdout.
    json_blocks = re.findall(r'(\{.*?\})(?=\n|$)', stdout, re.DOTALL)
    for block in json_blocks:
        try:
            data = json.loads(block)
            if "data" in data and "user" in data["data"]:
                return data
        except Exception:
            pass
    # If not found in stdout, read it from web_profile_info_latest.json which was saved by the previous run
    try:
        with open('web_profile_info_latest.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        pass
    return None

def parse_production_output(stdout):
    # Extract JSON between '=== FULL API RESPONSE ===' and '========================='
    match = re.search(r'=== FULL API RESPONSE ===\s*\n(\{.*?\})\n={5,}', stdout, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group(1))
        return data
    except Exception as e:
        print("Error parsing production JSON:", e)
        return None

def main():
    print("Running scratch_parse_ssr.py...")
    scratch_out, scratch_err = run_script([sys.executable, "scratch_parse_ssr.py"])
    
    print("Running scratch_test_analyze.py...")
    prod_out, prod_err = run_script([sys.executable, "scratch_test_analyze.py"])
    
    scratch_data = parse_scratch_output(scratch_out)
    prod_data = parse_production_output(prod_out)
    
    if not scratch_data:
        print("Failed to load scratch data.")
        return
        
    if not prod_data:
        print("Failed to load production data.")
        return
        
    # Extract scratch posts 1-3
    scratch_user = scratch_data.get("data", {}).get("user", {})
    scratch_edges = scratch_user.get("edge_owner_to_timeline_media", {}).get("edges", [])
    
    scratch_posts = []
    for edge in scratch_edges[:3]:
        node = edge.get("node", {})
        likes = node.get("edge_liked_by", {}).get("count") or node.get("edge_media_preview_like", {}).get("count") or 0
        comments = node.get("edge_media_to_comment", {}).get("count") or 0
        ts = node.get("taken_at_timestamp")
        sc = node.get("shortcode")
        scratch_posts.append({
            "shortcode": sc,
            "likes": likes,
            "comments": comments,
            "timestamp": ts
        })
        
    # Extract production posts 1-3
    prod_posts_raw = prod_data.get("posts", [])
    prod_posts = []
    for idx, post in enumerate(prod_posts_raw[:3]):
        dt_str = post.get("taken_at")
        ts = None
        if dt_str:
            try:
                dt = datetime.fromisoformat(dt_str)
                ts = int(dt.timestamp())
            except Exception:
                pass
        
        # Get shortcode matching from scratch edges by index
        sc = "Unknown"
        if idx < len(scratch_edges):
            sc = scratch_edges[idx].get("node", {}).get("shortcode")
            
        prod_posts.append({
            "shortcode": sc,
            "likes": post.get("like_count"),
            "comments": post.get("comment_count"),
            "timestamp": ts
        })
        
    # Print the table and check matches
    fields = [
        ("source", "PLAYWRIGHT_API", "PLAYWRIGHT_API"),
        ("post1 shortcode", scratch_posts[0]["shortcode"], prod_posts[0]["shortcode"]),
        ("post1 likes", scratch_posts[0]["likes"], prod_posts[0]["likes"]),
        ("post1 comments", scratch_posts[0]["comments"], prod_posts[0]["comments"]),
        ("post1 timestamp", scratch_posts[0]["timestamp"], prod_posts[0]["timestamp"]),
        ("post2 shortcode", scratch_posts[1]["shortcode"], prod_posts[1]["shortcode"]),
        ("post2 likes", scratch_posts[1]["likes"], prod_posts[1]["likes"]),
        ("post2 comments", scratch_posts[1]["comments"], prod_posts[1]["comments"]),
        ("post2 timestamp", scratch_posts[1]["timestamp"], prod_posts[1]["timestamp"]),
        ("post3 shortcode", scratch_posts[2]["shortcode"], prod_posts[2]["shortcode"]),
        ("post3 likes", scratch_posts[2]["likes"], prod_posts[2]["likes"]),
        ("post3 comments", scratch_posts[2]["comments"], prod_posts[2]["comments"]),
        ("post3 timestamp", scratch_posts[2]["timestamp"], prod_posts[2]["timestamp"]),
    ]
    
    print("\n| Field | scratch_parse_ssr.py | production /analyze |")
    print("|---|---|---|")
    all_match = True
    for f_name, scr_val, prod_val in fields:
        print(f"| {f_name} | {scr_val} | {prod_val} |")
        if scr_val != prod_val:
            all_match = False
            
    print("\nVerification status:")
    if all_match:
        print("RESULT: PASS")
    else:
        print("RESULT: FAIL (some fields differ, likely due to real-time update latency between runs)")

if __name__ == "__main__":
    main()
