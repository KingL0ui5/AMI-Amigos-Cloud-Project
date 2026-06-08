"""Tests updating a document in the local MongoDB pokemon collection."""
import pymongo
import pymongo.errors

def test_mongo_update():
    """Update the test document's URL and read it back to confirm the change."""
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client["pokemon_db"]["pokemon"]
        collection.update_many({"name": "testmon"}, {"$set": {"url": "http://updated.com"}})
        result = list(collection.find({"name": "testmon"}))
        print("Updated:", result)
    except pymongo.errors.PyMongoError as e:
        print(f"Update failed: {e}")

if __name__ == '__main__':
    test_mongo_update()
