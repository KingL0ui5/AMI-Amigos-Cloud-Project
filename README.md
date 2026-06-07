# AMI-Amigos-Cloud-Project

A Python ETL pipeline that fetches Pokemon data from the PokeAPI, stores it in MongoDB hosted on an EC2 instance, and uploads it to AWS S3.

## Pipeline

```
PokeAPI --> Python --> MongoDB (EC2) --> JSON Export --> AWS S3
```

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- AWS credentials configured (`aws configure`)
- SSH key for EC2 instance at `~/.ssh/se-louis-key-pair.pem`

## Install dependencies

```bash
uv sync
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
