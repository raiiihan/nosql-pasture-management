"""Bootstrap DB artifacts: create mongo indexes and cassandra tables.

Run in dry-run by default. Set DRY_RUN=false in environment or pass --dry to disable dry-run.
"""
import os
import argparse
import sys

# ensure src package can be found when running script directly
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.mongo_client import MongoClientWrapper
from src.clients.cassandra_client import CassandraClientWrapper


def main(dry_run=True):
    mongo = MongoClientWrapper(dry_run=dry_run)
    cass = CassandraClientWrapper(dry_run=dry_run)
    mongo.create_indexes('pasture')
    cass.ensure_sensor_table('sensor_data_by_field')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--dry', dest='dry', action='store_true', help='force dry-run')
    p.add_argument('--real', dest='real', action='store_true', help='perform real operations (use env vars)')
    args = p.parse_args()
    dry = True
    if args.real:
        dry = False
    main(dry_run=dry)
