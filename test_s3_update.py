"""
Tests updating a file in S3 by overwriting it with new content.
Replaces AMI-Amigos/sasan-test/test.json with updated data and reads it back to confirm.
Expected: The updated JSON content printed to the terminal.
Requires AWS credentials configured and test_s3_create.py to have been run first.
"""
import boto3
import json
from botocore.exceptions import ClientError

BUCKET = "se-data-with-ai-etl-project"
KEY = "AMI-Amigos/sasan-test/test.json"

def test_s3_update():
    try:
        s3_client = boto3.client('s3')
        updated_data = json.dumps([{"name": "squirtle", "url": "https://pokeapi.co/api/v2/pokemon/7/"}])
        s3_client.put_object(Bucket=BUCKET, Key=KEY, Body=updated_data)
        response = s3_client.get_object(Bucket=BUCKET, Key=KEY)
        content = response['Body'].read().decode('utf-8')
        assert "squirtle" in content, "Update not reflected in file"
        print("S3 update successful:", content)
    except ClientError as e:
        print(f"S3 update failed: {e}")

if __name__ == '__main__':
    test_s3_update()
