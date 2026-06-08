"""
Tests the full pipeline end-to-end using the EC2-hosted MongoDB instance.
Fetches 5 Pokemon from the PokeAPI, stores them in MongoDB on EC2 via SSH tunnel,
reads them back, and prints the result.
Expected: A list of 5 documents printed from MongoDB on EC2.
Requires the EC2 instance to be running and .env configured with EC2_IP and SSH_KEY_PATH.
"""
from main import get_all_pokemon, Mongo

def test_pipeline():
    try:
        data = get_all_pokemon(5)
        assert data, "API fetch returned no data"
        db = Mongo()
        db.reset()
        db.create_data(data)
        result = db.read_data({})
        assert len(result) == 5, f"Expected 5 documents, got {len(result)}"
        print("Pipeline successful:", result)
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == '__main__':
    test_pipeline()
