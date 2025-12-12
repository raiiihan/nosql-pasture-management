"""Ingest field metadata into MongoDB (real mode).

Usage: python scripts/ingest_fields_real.py fields.jsonl
"""
import json
import sys
import os
from pathlib import Path
import python_dotenv

# Add project root to sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.mongo_client import MongoClientWrapper

# Load .env
python_dotenv.load_dotenv(os.path.join(ROOT, '.env'))


def ingest_fields(jsonl_path):
    """Read field JSONL and write to MongoDB."""
    mongo = MongoClientWrapper(dry_run=False)  # Real mode
    mongo.create_indexes('pasture')
    
    p = Path(jsonl_path)
    count = 0
    with p.open() as fh:
        for line in fh:
            field_doc = json.loads(line)
            mongo.insert_field('pasture', field_doc)
            count += 1
            print(f"Inserted field: {field_doc['_id']}")
    
    print(f"\nTotal fields ingested: {count}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: ingest_fields_real.py <fields.jsonl>')
        sys.exit(1)
    ingest_fields(sys.argv[1])
