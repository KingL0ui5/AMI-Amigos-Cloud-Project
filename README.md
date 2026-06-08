# AMI-Amigos-Cloud-Project

A Python ETL pipeline that fetches Pokemon data from the PokeAPI, stores it in MongoDB hosted on an EC2 instance, and uploads it to AWS S3.

## Pipeline

```
PokeAPI --> Python --> MongoDB (EC2) --> JSON Export --> AWS S3
```

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- An EC2 instance running MongoDB (see EC2 Setup below)
- An EC2 key pair `.pem` file

## Install uv

```bash
pip install uv
```

## Install dependencies

```bash
uv sync
```

This installs:

| Package | Purpose |
|---|---|
| `boto3` | AWS SDK for uploading to S3 |
| `pymongo` | MongoDB driver |
| `requests` | Fetching data from PokeAPI |
| `sshtunnel` | SSH tunnel to reach MongoDB on EC2 |
| `paramiko` | SSH backend used by sshtunnel |
| `cryptography` | Cryptographic support for paramiko |
| `python-dotenv` | Loads environment variables from `.env` |

## Environment Variables

Create a `.env` file in the project root:

```
EC2_IP=your-ec2-public-ip
SSH_KEY_PATH=~/.ssh/your-key-pair.pem
```

## AWS Setup

### Install the AWS CLI

Download and install from: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html

### Configure credentials

```bash
aws configure
```

This will prompt for your access key, secret key, region, and output format. Alternatively, set them manually:

`~/.aws/credentials`:
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

`~/.aws/config`:
```ini
[default]
region = eu-west-1
output = json
```

To verify your credentials are working:

```python
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

s3_client = boto3.client('s3')

try:
    bucket_list = s3_client.list_buckets()
    print("Credentials valid. Buckets:", [b['Name'] for b in bucket_list['Buckets']])
except NoCredentialsError:
    print("No credentials found — check your ~/.aws/credentials file.")
except ClientError as e:
    print("Credentials rejected by AWS:", e.response['Error']['Message'])
```

## EC2 Setup

1. Launch an EC2 instance (Ubuntu 24.04, t3.micro) in the AWS console
2. Create a key pair and download the `.pem` file to `~/.ssh/`
3. In the security group, open the following ports:
   - Port 22 (SSH) — required for the SSH tunnel
   - Port 27017 (MongoDB) — optional, only if connecting directly
4. SSH into the instance:

```bash
ssh -i ~/.ssh/your-key-pair.pem ubuntu@your-ec2-public-ip
```

5. Install MongoDB by running the following on the instance:

```bash
sudo apt update -y && sudo apt upgrade -y
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
sudo apt update -y
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

## Run the pipeline

```bash
uv run main.py
```

This will:
1. Fetch all Pokemon from the PokeAPI
2. Store them in MongoDB on the EC2 instance
3. Export the data as JSON
4. Upload it to the S3 bucket under `AMI-Amigos/pokemon.json`

## CRUD Operations

The `Mongo` class in `main.py` exposes the following operations against the `pokemon` collection:

| Method | Operation | Description |
|---|---|---|
| `create_data(data)` | Create | Inserts a list of documents |
| `read_data(filter)` | Read | Returns documents matching the filter |
| `update_data(filter, new_values)` | Update | Updates all documents matching the filter |
| `delete_data(filter)` | Delete | Deletes all documents matching the filter |
| `reset()` | Delete | Clears the entire collection |

Example usage:

```python
db = Mongo()
db.create_data([{"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"}])
db.read_data({"name": "bulbasaur"})
db.update_data({"name": "bulbasaur"}, {"url": "https://updated.com"})
db.delete_data({"name": "bulbasaur"})
```

## Run CRUD tests (local MongoDB)

Requires MongoDB running locally on port 27017. Run in order:

```bash
uv run test_create.py
uv run test_read.py
uv run test_update.py
uv run test_delete.py
```

## S3 Bucket

Data is uploaded to: `se-data-with-ai-etl-project/AMI-Amigos/`

## Data Notes

Each Pokemon document stored in MongoDB contains only `name` and `url` fields from the PokeAPI. Full details (id, height, weight, base experience, moves, sprites etc.) were intentionally omitted as the full payload per Pokemon is extremely large and would make the dataset impractical to store and export.

The `get_pokemon_details()` function exists in the code but is not called in the main pipeline for this reason.

JSON serialization uses `bson.json_util.dumps` instead of the standard `json.dumps` to correctly handle MongoDB's BSON types (e.g. ObjectId).
