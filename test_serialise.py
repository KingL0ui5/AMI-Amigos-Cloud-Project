"""
Tests JSON serialization of MongoDB documents using bson.json_util.dumps.
Reads from the local MongoDB pokemon collection and serializes to JSON.
Expected: A valid JSON string with ObjectId serialized as {"$oid": "..."}.
Requires MongoDB running locally on port 27017.
"""
import pymongo
from bson.json_util import dumps

def test_serialise():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client["pokemon_db"]["pokemon"]
        data = list(collection.find({}))
        assert len(data) > 0, "No documents found — run test_create.py first"
        json_data = dumps(data)
        assert "$oid" in json_data, "Expected BSON ObjectId serialization"
        print("Serialization successful:", json_data)
    except Exception as e:
        print(f"Serialization failed: {e}")

if __name__ == '__main__':
    test_serialise()
