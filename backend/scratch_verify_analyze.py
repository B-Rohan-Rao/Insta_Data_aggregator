import json
import asyncio
from app.main import analyze_creator

def main():
    print("Executing analyze_creator('carryminati')...")
    try:
        # Call the endpoint directly
        result = analyze_creator("carryminati")
        
        # Serialize to JSON, handling datetime serialization
        class DateTimeEncoder(json.JSONEncoder):
            def default(self, obj):
                from datetime import datetime
                if isinstance(obj, datetime):
                    return obj.isoformat()
                return super().default(obj)
                
        pretty_response = json.dumps(result, indent=2, cls=DateTimeEncoder)
        print("\n=== RESPONSE START ===")
        print(pretty_response)
        print("=== RESPONSE END ===\n")
        
    except Exception as e:
        print(f"Error executing analysis: {e}")

if __name__ == "__main__":
    main()
