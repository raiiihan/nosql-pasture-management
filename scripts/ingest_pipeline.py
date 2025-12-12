"""Prototype ingestion pipeline: reads generated sensor JSONL and ingests to Cassandra and updates Mongo metadata."""
import json
import sys
import os
from pathlib import Path

# Make project root importable when running script directly
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.mongo_client import MongoClientWrapper
from src.clients.cassandra_client import CassandraClientWrapper


def ingest(jsonl_path, dry_run=True):
    mongo = MongoClientWrapper(dry_run=dry_run)
    cass = CassandraClientWrapper(dry_run=dry_run)
    # ensure table exists in real mode (omitted in dry-run)
    p = Path(jsonl_path)
    with p.open() as fh:
        for line in fh:
            row = json.loads(line)
            field_id = row.get('field_id')
            # insert into cassandra
            cass.insert_sensor_row('sensor_data_by_field', row)
            # update mongo latest_metrics in real pipeline
            # simplified: patch latest_metrics from metric_type
            if row.get('metric_type') in ('ndvi','soil_moisture','grass_height'):
                # upsertField omitted for brevity
                mongo.insert_field('pasture', {'_id': field_id, 'latest_metrics': {row['metric_type']: row['metric_value']}})


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: ingest_pipeline.py <sensor.jsonl>')
        sys.exit(1)
    ingest(sys.argv[1], dry_run=True)
