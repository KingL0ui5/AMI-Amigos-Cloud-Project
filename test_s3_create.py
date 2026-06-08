"""
Tests uploading a file to S3.
Uploads a test JSON document to AMI-Amigos/sasan-test/test.json in the S3 bucket.
Expected: True printed on success, and the file visible in the S3 console.
Requires AWS credentials configured.
"""
import json
from main import S3

def test_s3_create():
    try:
        s3 = S3()
        data = json.dumps([{"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"}])
        result = s3.upload_data(data, "sasan-test/test.json")
        assert result, "Upload returned False"
        print("S3 create successful")
    except Exception as e:
        print(f"S3 create failed: {e}")

if __name__ == '__main__':
    test_s3_create()
