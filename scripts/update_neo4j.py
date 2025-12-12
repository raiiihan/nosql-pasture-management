"""Create Neo4j events when fields cross thresholds."""
import json
import sys
import os

# Ensure project root is on sys.path so imports like `from src...` work
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.neo4j_client import Neo4jClientWrapper


def update(jsonl_path, dry_run=True):
    n = Neo4jClientWrapper(dry_run=dry_run)
    with open(jsonl_path) as fh:
        for line in fh:
            row = json.loads(line)
            fid = row['field_id']
            if row['metric_type'] == 'soil_moisture' and row['metric_value'] < 10.0:
                n.create_event_for_field(fid, 'low_soil_moisture', {'value': row['metric_value'], 'ts': row['sensor_ts']})


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: update_neo4j.py <sensor.jsonl>')
        sys.exit(1)
    update(sys.argv[1], dry_run=True)
