"""Redis query: Get latest aggregated metrics for a field.

Usage: python scripts/query_redis_latest.py
"""
import sys
import os
import python_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.redis_client import RedisClientWrapper

python_dotenv.load_dotenv(os.path.join(ROOT, '.env'))


def query_latest_metrics():
    """Query Redis for latest aggregated metrics."""
    r = RedisClientWrapper(dry_run=False)
    
    print("=" * 60)
    print("Redis Query: Latest Aggregated Metrics")
    print("=" * 60)
    
    fields = ['field_1', 'field_2']
    
    for field_id in fields:
        latest = r.get_latest(field_id)
        
        if latest:
            print(f"\nField: {field_id}")
            print(f"  Latest NDVI: {latest.get(b'latest_ndvi', b'N/A').decode()}")
            print(f"  Latest Soil Moisture: {latest.get(b'latest_soil_moisture', b'N/A').decode()}")
            print(f"  7-day Soil Moisture Avg: {latest.get(b'soil_moisture_7day_avg', b'N/A').decode()}")
            print(f"  Latest Air Temp: {latest.get(b'latest_air_temp', b'N/A').decode()}")
            print(f"  Latest Grass Height: {latest.get(b'latest_grass_height', b'N/A').decode()}")
        else:
            print(f"\nField: {field_id}")
            print("  No data found. Run aggregation first.")
    
    # Check for alerts
    print("\n" + "-" * 60)
    print("Active Alerts (from Redis Streams):")
    try:
        alerts = r.client.xrange('alerts', count=5)
        if alerts:
            for alert_id, alert_data in alerts:
                print(f"  Alert ID: {alert_id}")
                print(f"    Data: {alert_data}")
        else:
            print("  No alerts recorded")
    except Exception as e:
        print(f"  Could not read alerts: {e}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    query_latest_metrics()
