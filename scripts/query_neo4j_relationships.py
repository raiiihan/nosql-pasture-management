"""Neo4j query: Find related fields and events.

Usage: python scripts/query_neo4j_relationships.py
"""
import sys
import os
import python_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.clients.neo4j_client import Neo4jClientWrapper

python_dotenv.load_dotenv(os.path.join(ROOT, '.env'))


def query_relationships():
    """Query Neo4j for field relationships and events."""
    n = Neo4jClientWrapper(dry_run=False)
    
    print("=" * 60)
    print("Neo4j Query: Field Relationships and Events")
    print("=" * 60)
    
    try:
        with n.driver.session() as session:
            # Query 1: Find all events
            print("\n1. All Events in Graph:\n")
            result = session.run("MATCH (e:Event) RETURN e.type as type, e.value as value LIMIT 10")
            events = list(result)
            if events:
                for record in events:
                    print(f"  Event Type: {record['type']}, Value: {record['value']}")
            else:
                print("  No events found. Run update_neo4j_real.py first.")
            
            # Query 2: Find high-risk fields
            print("\n2. Fields with Multiple Events (High Risk):\n")
            result = session.run("""
                MATCH (f:Field)-[:HAS_EVENT]->(e:Event)
                RETURN f.id as field_id, COUNT(e) as event_count
                ORDER BY event_count DESC
                LIMIT 5
            """)
            risk_fields = list(result)
            if risk_fields:
                for record in risk_fields:
                    print(f"  Field: {record['field_id']}, Events: {record['event_count']}")
            else:
                print("  No field-event relationships found.")
            
            # Query 3: Event distribution by type
            print("\n3. Event Distribution by Type:\n")
            result = session.run("""
                MATCH (e:Event)
                RETURN e.type as event_type, COUNT(e) as count
                GROUP BY e.type
            """)
            event_types = list(result)
            if event_types:
                for record in event_types:
                    print(f"  {record['event_type']}: {record['count']} occurrences")
            else:
                print("  No events found.")
    
    except Exception as e:
        print(f"Error querying Neo4j: {e}")
        print("(Make sure Neo4j is running and data has been ingested)")
    
    finally:
        n.close()
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    query_relationships()
