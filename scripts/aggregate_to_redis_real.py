"""Aggregate sensor data to Redis (real mode).

Usage: python scripts/aggregate_to_redis_real.py sensors.jsonl
"""
import json
import sys
import os
from collections import defaultdict, deque
import python_dotenv

# Add project root to sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.redis_client import RedisClientWrapper

# Load .env
python_dotenv.load_dotenv(os.path.join(ROOT, '.env'))


def aggregate_to_redis(jsonl_path):
    """Read sensor JSONL, compute rolling metrics, write to Redis."""
    r = RedisClientWrapper(dry_run=False)  # Real mode
    r.initialize()
    
    # Track rolling windows per field per metric
    windows = defaultdict(lambda: defaultdict(lambda: deque(maxlen=7)))
    
    alert_count = 0
    with open(jsonl_path) as fh:
        for line in fh:
            row = json.loads(line)
            fid = row['field_id']
            mt = row['metric_type']
            val = row['metric_value']
            
            # Compute rolling average for soil_moisture
            if mt == 'soil_moisture':
                windows[fid]['soil_moisture'].append(val)
                if len(windows[fid]['soil_moisture']) > 0:
                    avg = sum(windows[fid]['soil_moisture']) / len(windows[fid]['soil_moisture'])
                    r.hset_latest(fid, {'latest_soil_moisture': avg, 'soil_moisture_7day_avg': avg})
                    
                    # Alert if low
                    if avg < 12.0:
                        r.push_alert(fid, 'low_soil_moisture', {'value': avg, 'threshold': 12.0})
                        alert_count += 1
            
            # Track NDVI
            if mt == 'ndvi':
                windows[fid]['ndvi'].append(val)
                baseline = 0.55
                r.hset_latest(fid, {'latest_ndvi': val})
                
                # Alert if NDVI drops significantly
                if val < baseline - 0.15:
                    r.push_alert(fid, 'ndvi_drop', {'value': val, 'baseline': baseline})
                    alert_count += 1
            
            # Track air temperature
            if mt == 'air_temp':
                r.hset_latest(fid, {'latest_air_temp': val})
            
            # Track grass height
            if mt == 'grass_height':
                windows[fid]['grass_height'].append(val)
                if len(windows[fid]['grass_height']) > 0:
                    avg_height = sum(windows[fid]['grass_height']) / len(windows[fid]['grass_height'])
                    r.hset_latest(fid, {'latest_grass_height': val, 'grass_height_7day_avg': avg_height})
    
    print(f"Aggregation complete:")
    print(f"  Fields processed: {len(windows)}")
    print(f"  Alerts triggered: {alert_count}")
    print(f"  Metrics written to Redis")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: aggregate_to_redis_real.py <sensors.jsonl>')
        sys.exit(1)
    aggregate_to_redis(sys.argv[1])
