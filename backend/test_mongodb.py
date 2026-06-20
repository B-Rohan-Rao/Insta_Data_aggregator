import sys
from app.db import get_database

def main():
    print("Connecting to MongoDB Atlas...")
    try:
        # Retrieve the database instance, which also runs collections & indexes setup
        db = get_database()
        
        # 1. Ping database
        print("Pinging database...")
        db.command("ping")
        print("MongoDB Atlas connection ping successful!")
        
        # 2. Insert one test document
        test_doc = {
            "username": "test_mongo_user_123",
            "full_name": "Test User",
            "biography": "Temporary test profile for connection verification."
        }
        print(f"Inserting test document into 'profiles' collection: {test_doc}")
        insert_result = db.profiles.insert_one(test_doc)
        print(f"Document inserted with _id: {insert_result.inserted_id}")
        
        # 3. Read it back
        print("Reading the test document back...")
        retrieved_doc = db.profiles.find_one({"username": "test_mongo_user_123"})
        if retrieved_doc:
            print(f"Successfully retrieved document: {retrieved_doc}")
            assert retrieved_doc["username"] == "test_mongo_user_123", "Username mismatch!"
            assert retrieved_doc["full_name"] == "Test User", "Full name mismatch!"
        else:
            print("Error: Could not retrieve the inserted document!")
            sys.exit(1)
            
        # 4. Delete it
        print("Deleting the test document...")
        delete_result = db.profiles.delete_one({"username": "test_mongo_user_123"})
        print(f"Deleted count: {delete_result.deleted_count}")
        assert delete_result.deleted_count == 1, f"Expected 1 deleted document, got {delete_result.deleted_count}"
        
        print("\nAll MongoDB Atlas database checks passed successfully!")
        
    except Exception as e:
        print(f"\nDatabase layer test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
