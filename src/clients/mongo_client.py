import os
from typing import Optional

try:
    from pymongo import MongoClient, GEO2D
except Exception:
    MongoClient = None


class MongoClientWrapper:
    def __init__(self, uri: Optional[str]=None, dry_run: bool=True):
        self.dry_run = dry_run
        self.uri = uri or os.getenv('MONGO_URI')
        self.client = None
        if not dry_run and MongoClient is None:
            raise RuntimeError("pymongo not available")
        if not dry_run:
            self.client = MongoClient(self.uri)

    def get_db(self, name='pasture'):
        if self.dry_run:
            return None
        return self.client[name]

    def insert_field(self, db_name, field_doc):
        if self.dry_run:
            print(f"[mongo dry-run] would insert field into {db_name}: {field_doc.get('_id')}")
            return True
        db = self.get_db(db_name)
        return db.fields.replace_one({'_id': field_doc['_id']}, field_doc, upsert=True)

    def update_latest_metrics(self, db_name, field_id, metric_key, metric_value):
        """Atomically update nested latest_metrics for a field."""
        if self.dry_run:
            print(f"[mongo dry-run] update {db_name}.fields({field_id}) set latest_metrics.{metric_key}={metric_value}")
            return True
        db = self.get_db(db_name)
        return db.fields.update_one({'_id': field_id}, {'$set': {f'latest_metrics.{metric_key}': metric_value}}, upsert=True)

    def create_indexes(self, db_name):
        if self.dry_run:
            print(f"[mongo dry-run] would create 2dsphere index on fields.boundary in {db_name}")
            return
        db = self.get_db(db_name)
        db.fields.create_index([('boundary','2dsphere')])
        db.fields.create_index([('farm_id',1)])
