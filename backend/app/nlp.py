import re
from typing import Any, Dict, List, Optional
from langdetect import detect

# Set of common Hinglish words for quick heuristic detection
HINGLISH_WORDS = {
    "hai", "nahi", "kya", "kaise", "acha", "accha", "yaar", "tum", 
    "mera", "meri", "bhai", "kar", "karna", "ho", "hoga", "hu", "hun"
}

def detect_language(text: Optional[str]) -> str:
    """
    Detects the language of a given text.
    Returns: 'ENGLISH', 'HINDI', 'HINGLISH', or 'UNKNOWN'
    
    Rules:
    1. Empty text => UNKNOWN
    2. Devanagari characters => HINDI
    3. Contains common Hinglish words => HINGLISH
    4. Fallback to langdetect library (en => ENGLISH, hi => HINDI)
    """
    if not text or not text.strip():
        return "UNKNOWN"
        
    # Rule 1: Check for Devanagari characters (U+0900 to U+097F)
    if re.search(r"[\u0900-\u097F]", text):
        return "HINDI"
        
    # Rule 2: Check for common Hinglish words (case-insensitive whole-word match)
    words = set(re.findall(r"\b[a-zA-Z]+\b", text.lower()))
    if words.intersection(HINGLISH_WORDS):
        return "HINGLISH"
        
    # Rule 3: Use langdetect fallback
    try:
        lang = detect(text)
        if lang == "en":
            return "ENGLISH"
        elif lang == "hi":
            return "HINDI"
    except Exception:
        # Gracefully catch langdetect exceptions (e.g. text containing only numbers/punctuation)
        pass
        
    return "UNKNOWN"

def analyze_comments(comments: Optional[List[Any]]) -> Dict[str, float]:
    """
    Analyzes a list of comments and returns the percentage distribution of
    English, Hindi, and Hinglish.
    
    Input:
        comments: List of comment strings, or list of dicts containing a 'text' key.
        
    Returns:
        Dict: {
            "english_percent": float,
            "hindi_percent": float,
            "hinglish_percent": float
        }
    """
    if not comments:
        return {
            "english_percent": 0.0,
            "hindi_percent": 0.0,
            "hinglish_percent": 0.0
        }
        
    english_count = 0
    hindi_count = 0
    hinglish_count = 0
    total_comments = len(comments)
    
    for comment in comments:
        if isinstance(comment, dict):
            text = comment.get("text", "")
        else:
            text = str(comment)
            
        lang = detect_language(text)
        if lang == "ENGLISH":
            english_count += 1
        elif lang == "HINDI":
            hindi_count += 1
        elif lang == "HINGLISH":
            hinglish_count += 1
            
    return {
        "english_percent": round((english_count / total_comments) * 100, 2),
        "hindi_percent": round((hindi_count / total_comments) * 100, 2),
        "hinglish_percent": round((hinglish_count / total_comments) * 100, 2)
    }
