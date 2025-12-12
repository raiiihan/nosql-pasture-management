import os
from typing import Optional

try:
    from neo4j import GraphDatabase
except Exception:
    GraphDatabase = None


class Neo4jClientWrapper:
    def __init__(self, uri: Optional[str]=None, user: Optional[str]=None, password: Optional[str]=None, dry_run: bool=True):
        self.dry_run = dry_run
        self.uri = uri or os.getenv('NEO4J_URI')
        self.user = user or os.getenv('NEO4J_USER')
        self.password = password or os.getenv('NEO4J_PASSWORD')
        self.driver = None
        if not dry_run and GraphDatabase is None:
            raise RuntimeError('neo4j package not available')
        if not dry_run:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        if self.driver:
            self.driver.close()

    def create_event_for_field(self, field_id, event_type, props: dict):
        if self.dry_run:
            print(f"[neo4j dry-run] create Event node for {field_id} type={event_type} props={props}")
            return True
        with self.driver.session() as s:
            q = "MERGE (f:Field {id:$field_id}) CREATE (e:Event {props}) CREATE (f)-[:HAS_EVENT]->(e)"
            s.run(q, field_id=field_id, props=props)
