import os
from typing import Optional

try:
    import redis
except Exception:
    redis = None


class RedisClientWrapper:
    def __init__(self, url: Optional[str]=None, dry_run: bool=True):
        self.dry_run = dry_run
        self.url = url or os.getenv('REDIS_URL')
        self.client = None
        if not dry_run and redis is None:
            raise RuntimeError('redis package not available')
        if not dry_run:
            self.client = redis.from_url(self.url)

    def initialize(self):
        if self.dry_run:
            print('[redis dry-run] initialize (noop)')
            return
        # example: ensure streams exist (no-op for Redis)
        return True

    def get_latest(self, field_id):
        key = f"field:{field_id}"
        if self.dry_run:
            print(f"[redis dry-run] would HGETALL {key}")
            return {}
        return self.client.hgetall(key)

    def hset_latest(self, field_id, mapping: dict):
        key = f"field:{field_id}"
        if self.dry_run:
            print(f"[redis dry-run] HSET {key} {mapping}")
            return True
        return self.client.hset(key, mapping=mapping)

    def push_alert(self, field_id, alert_type, payload: dict):
        if self.dry_run:
            print(f"[redis dry-run] XADD alerts * field {field_id} type {alert_type} payload {payload}")
            return True
        body = { 'field': field_id, 'type': alert_type }
        body.update(payload)
        return self.client.xadd('alerts', body)
