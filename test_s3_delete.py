"""
Tests deleting a file from S3.
Deletes AMI-Amigos/sasan-test/test.json from the S3 bucket.
Expected: "Deleted" printed on success. The file should no longer appear in the S3 console.
Requires AWS credentials configured and test_s3_create.py to have been run first.
"""
import boto3
from botocore.exceptions import ClientError

BUCKET = "se-data-with-ai-etl-project"
KEY = "AMI-Amigos/sasan-test/test.json"

def test_s3_delete():
    try:
        s3_client = boto3.client('s3')
        s3_client.delete_object(Bucket=BUCKET, Key=KEY)
        print("S3 delete successful")
    except ClientError as e:
        print(f"S3 delete failed: {e}")

if __name__ == '__main__':
    test_s3_delete()
