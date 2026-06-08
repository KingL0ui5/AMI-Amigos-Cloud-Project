"""Tests reading a document from the local MongoDB pokemon collection."""
import pymongo
import pymongo.errors

def test_mongo_read():
    """Query for the test document inserted by test_create.py and print the result."""
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client["pokemon_db"]["pokemon"]
        result = list(collection.find({"name": "testmon"}))
        print("Read:", result)
    except pymongo.errors.PyMongoError as e:
        print(f"Read failed: {e}")

if __name__ == '__main__':
    test_mongo_read()
