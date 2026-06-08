"""Tests inserting a document into the local MongoDB pokemon collection."""
import pymongo
import pymongo.errors

def test_mongo_create():
    """Insert a test document and read it back to confirm it was stored."""
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client["pokemon_db"]["pokemon"]
        collection.insert_many([{"name": "testmon", "url": "http://test.com"}])
        result = list(collection.find({"name": "testmon"}))
        print("Created:", result)
    except pymongo.errors.PyMongoError as e:
        print(f"Create failed: {e}")

if __name__ == '__main__':
    test_mongo_create()
