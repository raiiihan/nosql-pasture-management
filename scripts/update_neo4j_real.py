"""Create Neo4j events when thresholds crossed (real mode).

Usage: python scripts/update_neo4j_real.py sensors.jsonl
"""
import json
import sys
import os
import python_dotenv

# Add project root to sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.neo4j_client import Neo4jClientWrapper

# Load .env
python_dotenv.load_dotenv(os.path.join(ROOT, '.env'))


def update_neo4j_real(jsonl_path):
    """Read sensor JSONL and create Neo4j events for threshold crossings."""
    n = Neo4jClientWrapper(dry_run=False)  # Real mode
    
    event_count = 0
    with open(jsonl_path) as fh:
        for line in fh:
            row = json.loads(line)
            fid = row['field_id']
            
            # Create event for low soil moisture
            if row['metric_type'] == 'soil_moisture' and row['metric_value'] < 10.0:
                n.create_event_for_field(
                    fid,
                    'low_soil_moisture',
                    {
                        'value': row['metric_value'],
                        'ts': row['sensor_ts'],
                        'severity': 'high' if row['metric_value'] < 8.0 else 'medium'
                    }
                )
                event_count += 1
            
            # Create event for NDVI drop
            if row['metric_type'] == 'ndvi' and row['metric_value'] < 0.40:
                n.create_event_for_field(
                    fid,
                    'low_ndvi',
                    {
                        'value': row['metric_value'],
                        'ts': row['sensor_ts'],
                        'baseline': 0.55
                    }
                )
                event_count += 1
            
            # Create event for high air temperature
            if row['metric_type'] == 'air_temp' and row['metric_value'] > 30.0:
                n.create_event_for_field(
                    fid,
                    'high_temperature',
                    {
                        'value': row['metric_value'],
                        'ts': row['sensor_ts']
                    }
                )
                event_count += 1
            
            # Create event for low grass height
            if row['metric_type'] == 'grass_height' and row['metric_value'] < 4.0:
                n.create_event_for_field(
                    fid,
                    'low_grass_height',
                    {
                        'value': row['metric_value'],
                        'ts': row['sensor_ts']
                    }
                )
                event_count += 1
    
    print(f"Neo4j events created: {event_count}")
    n.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: update_neo4j_real.py <sensors.jsonl>')
        sys.exit(1)
    update_neo4j_real(sys.argv[1])
