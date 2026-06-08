"""
Tests reading a file from S3.
Reads AMI-Amigos/sasan-test/test.json from the S3 bucket and prints the contents.
Expected: The JSON content of the file printed to the terminal.
Requires AWS credentials configured and test_s3_create.py to have been run first.
"""
import boto3
from botocore.exceptions import ClientError

BUCKET = "se-data-with-ai-etl-project"
KEY = "AMI-Amigos/sasan-test/test.json"

def test_s3_read():
    try:
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=BUCKET, Key=KEY)
        content = response['Body'].read().decode('utf-8')
        print("S3 read successful:", content)
    except ClientError as e:
        print(f"S3 read failed: {e}")

if __name__ == '__main__':
    test_s3_read()
