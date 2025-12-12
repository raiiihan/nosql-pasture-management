"""Cassandra query: Time-series aggregation (average grass height per field).

Usage: python scripts/query_cassandra_timeseries.py
"""
import sys
import os
from datetime import datetime, timedelta
import python_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.cassandra_client import CassandraClientWrapper

python_dotenv.load_dotenv(os.path.join(ROOT, '.env'))


def query_timeseries():
    """Query Cassandra for time-series grass height data."""
    cass = CassandraClientWrapper(dry_run=False)
    
    print("=" * 60)
    print("Cassandra Query: Grass Height Time-Series (Last 48 Hours)")
    print("=" * 60)
    
    # Query time-series for grass_height metric
    # Note: this is a simplified example; full Cassandra queries would include proper date ranges
    try:
        rows = cass.session.execute("""
            SELECT field_id, sensor_ts, metric_value 
            FROM sensor_data_by_field
            WHERE field_id = 'field_1' AND metric_type = 'grass_height'
            LIMIT 20
        """)
        
        print(f"\nGrass Height readings for field_1:\n")
        data = list(rows)
        if data:
            for row in data[:10]:  # Show first 10
                print(f"  Time: {row.sensor_ts}")
                print(f"  Height (cm): {row.metric_value}")
                print()
            
            if len(data) > 10:
                print(f"  ... and {len(data) - 10} more records")
            
            # Compute simple average
            avg_height = sum(r.metric_value for r in data) / len(data)
            print(f"\nAverage grass height: {avg_height:.2f} cm")
        else:
            print("  No data found. Run ingestion first.")
    
    except Exception as e:
        print(f"Error querying Cassandra: {e}")
        print("(Make sure Cassandra is running and data has been ingested)")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    query_timeseries()
