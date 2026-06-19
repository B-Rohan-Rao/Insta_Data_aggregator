import sys
import logging
from pathlib import Path

# Add backend directory to Python path so `app` can be imported
sys.path.append(str(Path(__file__).parent))

from app.services.instagram import InstagramService

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    print("--- Instagram Session Refresh Utility ---")
    service = InstagramService()
    
    print("Forcing authentication process...")
    try:
        # Force login forces the service to bypass the valid check
        service.login(force=True)
        print("Session successfully bootstrapped and saved.")
    except Exception as e:
        print(f"Failed to refresh session: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
