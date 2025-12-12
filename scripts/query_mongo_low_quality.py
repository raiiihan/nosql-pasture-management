"""MongoDB query: Find fields with low NDVI (geospatial + filter example).

Usage: python scripts/query_mongo_low_quality.py
"""
import sys
import os
import python_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.mongo_client import MongoClientWrapper

python_dotenv.load_dotenv(os.path.join(ROOT, '.env'))


def query_low_quality():
    """Query MongoDB for fields with low NDVI (poor forage quality)."""
    mongo = MongoClientWrapper(dry_run=False)
    db = mongo.get_db('pasture')
    
    print("=" * 60)
    print("MongoDB Query: Fields with Low NDVI (Poor Forage Quality)")
    print("=" * 60)
    
    # Find fields with NDVI < 0.45 (poor quality threshold)
    low_ndvi_fields = db.fields.find(
        {'latest_metrics.ndvi': {'$lt': 0.45}},
        {'_id': 1, 'name': 1, 'farm_id': 1, 'latest_metrics.ndvi': 1, 'soil_type': 1}
    )
    
    results = list(low_ndvi_fields)
    print(f"\nFound {len(results)} fields with NDVI < 0.45:\n")
    for field in results:
        ndvi = field.get('latest_metrics', {}).get('ndvi', 'N/A')
        print(f"  Field: {field['_id']}")
        print(f"    Name: {field.get('name')}")
        print(f"    Farm: {field.get('farm_id')}")
        print(f"    NDVI: {ndvi}")
        print(f"    Soil Type: {field.get('soil_type')}")
        print()
    
    print("=" * 60)


if __name__ == '__main__':
    query_low_quality()
