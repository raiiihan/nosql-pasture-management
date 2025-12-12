import os
from typing import Optional

try:
    from cassandra.cluster import Cluster
except Exception:
    Cluster = None


class CassandraClientWrapper:
    def __init__(self, contact_points=None, keyspace='pasture', dry_run=True):
        self.dry_run = dry_run
        self.contact_points = contact_points or os.getenv('CASSANDRA_CONTACT_POINTS', '127.0.0.1').split(',')
        self.keyspace = keyspace
        self.session = None
        if not dry_run and Cluster is None:
            raise RuntimeError('cassandra-driver not available')
        if not dry_run:
            cluster = Cluster(self.contact_points)
            self.session = cluster.connect()
            # create keyspace if not exists
            self.session.execute("""
                CREATE KEYSPACE IF NOT EXISTS %s
                WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
            """ % self.keyspace)
            self.session.set_keyspace(self.keyspace)

    def ensure_sensor_table(self, table='sensor_data_by_field'):
        if self.dry_run:
            print(f"[cassandra dry-run] would ensure table {table} in keyspace {self.keyspace}")
            return
        q = f"""
        CREATE TABLE IF NOT EXISTS {table} (
          field_id text,
          sensor_ts timestamp,
          sensor_id text,
          metric_type text,
          metric_value double,
          quality_flag int,
          PRIMARY KEY ((field_id), sensor_ts, sensor_id)
        ) WITH CLUSTERING ORDER BY (sensor_ts DESC);
        """
        self.session.execute(q)

    def insert_sensor_row(self, table, row: dict, ttl: Optional[int]=None):
        if self.dry_run:
            print(f"[cassandra dry-run] would insert into {table}: {row} TTL={ttl}")
            return True
        cols = ",".join(row.keys())
        placeholders = ",".join(["%s"]*len(row))
        q = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        if ttl:
            q += f" USING TTL {ttl}"
        prepared = self.session.prepare(q)
        self.session.execute(prepared, tuple(row.values()))
