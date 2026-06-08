"""Tests deleting a document from the local MongoDB pokemon collection."""
import pymongo
import pymongo.errors

def test_mongo_delete():
    """Delete the test document and confirm the collection no longer contains it."""
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client["pokemon_db"]["pokemon"]
        collection.delete_many({"name": "testmon"})
        result = list(collection.find({"name": "testmon"}))
        print("Deleted, remaining:", result)
    except pymongo.errors.PyMongoError as e:
        print(f"Delete failed: {e}")

if __name__ == '__main__':
    test_mongo_delete()
