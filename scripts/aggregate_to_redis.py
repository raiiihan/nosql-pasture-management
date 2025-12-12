"""Simple aggregation job: reads sensor JSONL, computes 7-point rolling soil moisture average and NDVI anomaly, writes latest to Redis and pushes alerts."""
import json
import sys
import os
from collections import defaultdict, deque

# Ensure project root is on sys.path so `from src...` works when running this script directly
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.redis_client import RedisClientWrapper


def aggregate(jsonl_path, dry_run=True):
    r = RedisClientWrapper(dry_run=dry_run)
    window = defaultdict(lambda: deque(maxlen=7))
    with open(jsonl_path) as fh:
        for line in fh:
            row = json.loads(line)
            fid = row['field_id']
            mt = row['metric_type']
            val = row['metric_value']
            if mt == 'soil_moisture':
                window[fid].append(val)
                avg = sum(window[fid])/len(window[fid])
                # write latest to redis
                r.hset_latest(fid, {'latest_soil_moisture': avg})
                if avg < 12.0:
                    r.push_alert(fid, 'low_soil_moisture', {'value': avg})
            if mt == 'ndvi':
                # compare to a simple long-term baseline (placeholder)
                baseline = 0.55
                if val < baseline - 0.15:
                    r.hset_latest(fid, {'latest_ndvi': val})
                    r.push_alert(fid, 'ndvi_drop', {'value': val})


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: aggregate_to_redis.py <sensor.jsonl>')
        sys.exit(1)
    aggregate(sys.argv[1], dry_run=True)
