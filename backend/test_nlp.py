import sys
from app.nlp import detect_language, analyze_comments

def run_tests():
    print("Starting nlp.py verification...")
    
    # 1. Test detect_language
    
    # Empty / whitespace
    assert detect_language("") == "UNKNOWN"
    assert detect_language("   ") == "UNKNOWN"
    assert detect_language(None) == "UNKNOWN"
    
    # Devanagari
    assert detect_language("नमस्ते आप कैसे हैं?") == "HINDI"
    
    # Hinglish words check
    assert detect_language("tum kaise ho?") == "HINGLISH"
    assert detect_language("kya baat hai yaar") == "HINGLISH"
    assert detect_language("mera bhai!") == "HINGLISH"
    
    # English (langdetect fallback)
    assert detect_language("This is a beautiful day, hope you enjoy it.") == "ENGLISH"
    
    # Unknown (e.g. only numbers, emojis, or unsupported lang)
    assert detect_language("1234567890") == "UNKNOWN"
    assert detect_language("👍🔥😎") == "UNKNOWN"
    
    print("Individual language detection tests passed!")
    
    # 2. Test analyze_comments
    comments = [
        "This is an amazing photo, love the colors!", # ENGLISH
        "kya baat hai yaar, bahut acha",             # HINGLISH
        "नमस्ते दोस्तों",                                # HINDI
        "tum kaise ho?",                              # HINGLISH
        "Random gibberish that doesn't trigger",      # ENGLISH (likely detected as English by langdetect)
        "12345"                                       # UNKNOWN
    ]
    
    # Out of 6 comments:
    # 2 English (This is..., Random...)
    # 2 Hinglish (kya baat..., tum...)
    # 1 Hindi (नमस्ते...)
    # 1 Unknown (12345)
    
    # Percents:
    # English: 2/6 * 100 = 33.33%
    # Hinglish: 2/6 * 100 = 33.33%
    # Hindi: 1/6 * 100 = 16.67%
    
    res = analyze_comments(comments)
    print(f"Comment analysis results: {res}")
    
    assert res["english_percent"] == 33.33
    assert res["hinglish_percent"] == 33.33
    assert res["hindi_percent"] == 16.67
    
    # Test dictionary comments input
    dict_comments = [
        {"username": "user1", "text": "This is great!"},
        {"username": "user2", "text": "kya baat hai"}
    ]
    res_dict = analyze_comments(dict_comments)
    assert res_dict["english_percent"] == 50.0
    assert res_dict["hinglish_percent"] == 50.0
    assert res_dict["hindi_percent"] == 0.0
    
    print("Comment analysis tests passed!")
    
    # 3. Test empty inputs
    empty_res = analyze_comments([])
    assert empty_res["english_percent"] == 0.0
    assert empty_res["hindi_percent"] == 0.0
    assert empty_res["hinglish_percent"] == 0.0
    print("Empty comment analysis tests passed!")

    print("\nAll NLP tests passed successfully!")

if __name__ == "__main__":
    run_tests()
