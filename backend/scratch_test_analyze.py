import os
import sys
import json
import logging
from datetime import datetime

# Set up logging to stdout to capture warnings (e.g. SOURCE = ...)
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import analyze_creator

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def main():
    print("Running analyze_creator for adityasaidwhat...")
    try:
        response = analyze_creator("adityasaidwhat")
        
        # Pretty print response
        print("\n=== FULL API RESPONSE ===")
        print(json.dumps(response, indent=2, cls=DateTimeEncoder))
        print("=========================")
        
    except Exception as e:
        print(f"\n[ERROR] analyze_creator failed: {e}")

if __name__ == "__main__":
    main()
