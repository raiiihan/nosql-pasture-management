"""End-to-end demo runner: generates data, bootstraps DBs, ingests, aggregates, queries.

Usage: python scripts/run_demo.py

This script runs the complete pipeline:
1. Generate fields and sensor data
2. Bootstrap databases (create indexes/tables)
3. Ingest field metadata to MongoDB
4. Ingest sensor data to Cassandra
5. Aggregate metrics to Redis
6. Create events in Neo4j
7. Run cross-DB queries
"""
import subprocess
import sys
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def run_cmd(cmd, description):
    """Run a command and report status."""
    print("\n" + "=" * 70)
    print(f"STEP: {description}")
    print("=" * 70)
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with exit code {e.returncode}")
        return False


def main():
    print("\n" + "*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  NoSQL Pasture Management - End-to-End Demo".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    
    steps = [
        ("python -m src.generator fields --count 5 --out fields.jsonl", 
         "Generate 5 field metadata documents"),
        
        ("python -m src.generator sensors --field-id field_1 --periods 48 --out sensors_field1.jsonl",
         "Generate 48-hour sensor data for field_1"),
        
        ("python -m src.generator sensors --field-id field_2 --periods 48 --out sensors_field2.jsonl",
         "Generate 48-hour sensor data for field_2"),
        
        ("python scripts/bootstrap_databases.py --real",
         "Bootstrap databases (create MongoDB indexes and Cassandra tables)"),
        
        ("python scripts/ingest_fields_real.py fields.jsonl",
         "Ingest field metadata into MongoDB"),
        
        ("python scripts/ingest_sensors_real.py sensors_field1.jsonl",
         "Ingest sensor data (field_1) into Cassandra"),
        
        ("python scripts/ingest_sensors_real.py sensors_field2.jsonl",
         "Ingest sensor data (field_2) into Cassandra"),
        
        ("python scripts/aggregate_to_redis_real.py sensors_field1.jsonl",
         "Aggregate metrics for field_1 and write to Redis"),
        
        ("python scripts/aggregate_to_redis_real.py sensors_field2.jsonl",
         "Aggregate metrics for field_2 and write to Redis"),
        
        ("python scripts/update_neo4j_real.py sensors_field1.jsonl",
         "Create Neo4j events for field_1 threshold crossings"),
        
        ("python scripts/update_neo4j_real.py sensors_field2.jsonl",
         "Create Neo4j events for field_2 threshold crossings"),
    ]
    
    failed_steps = []
    
    for cmd, description in steps:
        if not run_cmd(cmd, description):
            failed_steps.append(description)
            print(f"Continuing with remaining steps...")
        time.sleep(0.5)  # Small delay between steps
    
    print("\n" + "=" * 70)
    print("CROSS-DATABASE QUERIES")
    print("=" * 70)
    
    query_steps = [
        ("python scripts/query_mongo_low_quality.py",
         "MongoDB: Find fields with low NDVI"),
        
        ("python scripts/query_cassandra_timeseries.py",
         "Cassandra: Time-series grass height analysis"),
        
        ("python scripts/query_redis_latest.py",
         "Redis: Latest aggregated metrics and alerts"),
        
        ("python scripts/query_neo4j_relationships.py",
         "Neo4j: Field relationships and events"),
    ]
    
    for cmd, description in query_steps:
        run_cmd(cmd, description)
    
    # Summary
    print("\n" + "*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  Demo Complete!".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    
    if failed_steps:
        print(f"\n⚠ {len(failed_steps)} steps failed:")
        for step in failed_steps:
            print(f"  - {step}")
        print("\nNote: Ensure all databases are running (see DEMO_SETUP.md for Docker setup)")
    else:
        print("\n✓ All steps completed successfully!")
        print("\nYour databases now contain:")
        print("  • MongoDB: 5 field documents with metadata")
        print("  • Cassandra: 384 sensor readings (48 hours × 2 fields × 4 metrics)")
        print("  • Redis: Latest metrics and aggregates, plus alert events")
        print("  • Neo4j: Event nodes linked to fields (threshold crossings)")
        print("\nNext steps:")
        print("  • View Neo4j graph at: http://localhost:7474")
        print("  • Explore MongoDB with: mongosh")
        print("  • Query Redis with: redis-cli")


if __name__ == '__main__':
    main()
