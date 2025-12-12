"""Ingest sensor data into Cassandra (real mode).

Usage: python scripts/ingest_sensors_real.py sensors.jsonl
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

from src.clients.cassandra_client import CassandraClientWrapper

# Load .env
python_dotenv.load_dotenv(os.path.join(ROOT, '.env'))


def ingest_sensors(jsonl_path):
    """Read sensor JSONL and write to Cassandra."""
    cass = CassandraClientWrapper(dry_run=False)  # Real mode
    cass.ensure_sensor_table('sensor_data_by_field')
    
    p = Path(jsonl_path)
    count = 0
    with p.open() as fh:
        for line in fh:
            row = json.loads(line)
            cass.insert_sensor_row('sensor_data_by_field', row, ttl=7776000)  # 90 days TTL
            count += 1
    
    print(f"Ingested {count} sensor rows into Cassandra from {jsonl_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: ingest_sensors_real.py <sensors.jsonl>')
        sys.exit(1)
    ingest_sensors(sys.argv[1])
