import os
import logging
from typing import List, Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks, HTTPException
from pydantic import BaseModel

try:
    from src.clients.mongo_client import MongoClientWrapper
except Exception:
    MongoClientWrapper = None

try:
    from src.clients.cassandra_client import CassandraClientWrapper
except Exception:
    CassandraClientWrapper = None

from src.generator import generate_field

app = FastAPI(title="Pasture Manager API")

# CORS - allow frontend origins via env or allow all in dev
allow_origins = [o.strip() for o in os.getenv('FRONTEND_ORIGINS', '*').split(',')] if os.getenv('FRONTEND_ORIGINS') else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger('pasture.api')
logging.basicConfig(level=logging.INFO)


@app.get('/health')
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get('/api/fields', response_model=List[Dict[str, Any]])
def get_fields() -> List[Dict[str, Any]]:
    """Return list of fields.

    Attempts to read from MongoDB if configured; otherwise returns generated sample fields.
    """
    # Try to use MongoDB client if available and MONGO_URI is set
    mongo_uri = os.getenv('MONGO_URI')
    if MongoClientWrapper is not None and mongo_uri:
        try:
            client = MongoClientWrapper(dry_run=False, uri=mongo_uri)
            db = client.get_db('pasture')
            if db is not None:
                docs = []
                for d in db.fields.find({}):
                    # Convert _id to string if needed
                    if '_id' in d:
                        try:
                            d['_id'] = str(d['_id'])
                        except Exception:
                            pass
                    docs.append(d)
                logger.info(f"Returned {len(docs)} fields from MongoDB")
                return docs
        except Exception as e:
            logger.warning(f"Could not connect to MongoDB (MONGO_URI provided): {e}")

    # Fallback: return generated sample fields
    samples = [generate_field(field_id=f"field_{i+1}", farm_id=f"farm_{(i//5)+1}", center=(0.0 + i*0.01, 0.0 + i*0.005)) for i in range(5)]
    logger.info(f"Returning {len(samples)} sample fields")
    return samples



@app.get('/api/fields/{field_id}', response_model=Dict[str, Any])
def get_field(field_id: str) -> Dict[str, Any]:
    """Return single field by id. Try MongoDB first, otherwise generate a sample."""
    mongo_uri = os.getenv('MONGO_URI')
    if MongoClientWrapper is not None and mongo_uri:
        try:
            client = MongoClientWrapper(dry_run=False, uri=mongo_uri)
            db = client.get_db('pasture')
            if db is not None:
                doc = db.fields.find_one({'_id': field_id})
                if doc:
                    try:
                        doc['_id'] = str(doc['_id'])
                    except Exception:
                        pass
                    return doc
        except Exception as e:
            logger.warning(f"Could not fetch field {field_id} from MongoDB: {e}")

    # Fallback
    return generate_field(field_id=field_id)


@app.get('/api/fields/{field_id}/timeseries')
def get_field_timeseries(field_id: str, metric: str = None, periods: int = 48) -> List[Dict[str, Any]]:
    """Return time-series for a field. If Cassandra is configured, query it; otherwise generate sample series."""
    contact = os.getenv('CASSANDRA_CONTACT_POINTS')
    table = os.getenv('CASSANDRA_TABLE', 'sensor_data_by_field')
    if CassandraClientWrapper is not None and contact:
        try:
            client = CassandraClientWrapper(contact_points=contact.split(','), dry_run=False)
            session = client.session
            if session is not None:
                # Query sensor rows for field_id
                q = f"SELECT field_id, sensor_ts, sensor_id, metric_type, metric_value FROM {table} WHERE field_id=%s LIMIT %s"
                prepared = session.prepare(q)
                rows = session.execute(prepared, (field_id, periods))
                result = []
                for r in rows:
                    result.append({
                        'field_id': r.field_id,
                        'sensor_ts': getattr(r, 'sensor_ts', None).isoformat() if getattr(r, 'sensor_ts', None) else None,
                        'sensor_id': getattr(r, 'sensor_id', None),
                        'metric_type': getattr(r, 'metric_type', None),
                        'metric_value': getattr(r, 'metric_value', None),
                    })
                return result
        except Exception as e:
            logger.warning(f"Could not query Cassandra for timeseries: {e}")

    # Fallback: generate sample sensor series
    try:
        from src.generator import generate_sensor_series
        rows = generate_sensor_series(field_id=field_id, periods=periods)
        if metric:
            rows = [r for r in rows if r.get('metric_type') == metric]
        return rows
    except Exception as e:
        logger.error(f"Failed to generate sample timeseries: {e}")
        return []


# ------ Ingestion models and endpoints ------


class FieldDoc(BaseModel):
    _id: str
    farm_id: str
    name: str
    boundary: Dict[str, Any]
    soil_type: str | None = None
    establishment_date: str | None = None
    latest_metrics: Dict[str, Any] | None = None


class SensorRow(BaseModel):
    field_id: str
    sensor_ts: str
    sensor_id: str
    metric_type: str
    metric_value: float
    quality_flag: int | None = 0


def _make_mongo_client():
    uri = os.getenv('MONGO_URI')
    if MongoClientWrapper is None:
        return None
    try:
        return MongoClientWrapper(dry_run=(uri is None), uri=uri)
    except Exception:
        return None


def _make_cassandra_client():
    contact = os.getenv('CASSANDRA_CONTACT_POINTS')
    if CassandraClientWrapper is None:
        return None
    try:
        return CassandraClientWrapper(contact_points=contact.split(',') if contact else None, dry_run=(contact is None))
    except Exception:
        return None


def _make_redis_client():
    url = os.getenv('REDIS_URI') or os.getenv('REDIS_URL')
    if RedisClientWrapper is None:
        return None
    try:
        return RedisClientWrapper(url=url, dry_run=(url is None))
    except Exception:
        return None


def _make_neo4j_client():
    uri = os.getenv('NEO4J_URI')
    user = os.getenv('NEO4J_USER')
    pw = os.getenv('NEO4J_PASSWORD') or os.getenv('NEO4J_AUTH')
    if Neo4jClientWrapper is None:
        return None
    try:
        return Neo4jClientWrapper(uri=uri, user=user, password=pw, dry_run=(uri is None))
    except Exception:
        return None


@app.post('/api/fields', status_code=201)
def ingest_field(field: FieldDoc, background_tasks: BackgroundTasks):
    """Ingest or upsert a field document into MongoDB. Runs insert in background when possible."""
    client = _make_mongo_client()
    if client is None:
        # No Mongo client available; return accepted but not stored
        logger.warning('Mongo client unavailable; skipping persistent storage for field')
        return {"status": "accepted", "stored": False}

    # Use background task to avoid blocking
    def _do_insert(fdoc: dict):
        try:
            client.insert_field('pasture', fdoc)
            logger.info(f"Inserted/updated field {fdoc.get('_id')}")
        except Exception as e:
            logger.error(f"Failed to insert field: {e}")

    background_tasks.add_task(_do_insert, field.dict())
    return {"status": "accepted", "stored": True}


@app.post('/api/fields/{field_id}/ingest-sensors')
def ingest_sensors(field_id: str, rows: List[SensorRow], background_tasks: BackgroundTasks):
    """Accept list of sensor rows and ingest to Cassandra; update Redis latest metrics and push events to Neo4j as needed in background."""
    cass_client = _make_cassandra_client()
    redis_client = _make_redis_client()
    neo4j_client = _make_neo4j_client()

    if cass_client is None and redis_client is None and neo4j_client is None:
        raise HTTPException(status_code=503, detail="No database clients available to ingest data")

    def _process_rows(rlist: List[dict]):
        # Insert into Cassandra
        try:
            table = os.getenv('CASSANDRA_TABLE', 'sensor_data_by_field')
            for r in rlist:
                row = r
                if cass_client is not None:
                    try:
                        cass_client.insert_sensor_row(table, row, ttl=int(os.getenv('SENSOR_TTL_DAYS', 90)) * 24 * 3600)
                    except Exception as e:
                        logger.error(f"Cassandra insert failed for {row}: {e}")

                # Update Redis latest metrics for metric types
                if redis_client is not None:
                    try:
                        # update a simple hash with latest metric value and timestamp
                        redis_client.hset_latest(field_id, {row['metric_type']: row['metric_value'], 'last_ts': row['sensor_ts']})
                    except Exception as e:
                        logger.error(f"Redis update failed for {row}: {e}")

                # Example: push Neo4j event when thresholds are exceeded (simple threshold check)
                if neo4j_client is not None:
                    try:
                        # simple rule: if soil_moisture < critical threshold, create event
                        if row.get('metric_type') == 'soil_moisture' and float(row.get('metric_value', 0)) < float(os.getenv('MOISTURE_CRITICAL', 20)):
                            neo4j_client.create_event_for_field(field_id, 'LOW_MOISTURE', {'value': row.get('metric_value'), 'ts': row.get('sensor_ts')})
                    except Exception as e:
                        logger.error(f"Neo4j event creation failed for {row}: {e}")

        except Exception as e:
            logger.error(f"Background ingestion failed: {e}")

    # schedule background processing
    background_tasks.add_task(_process_rows, [r.dict() for r in rows])
    return {"status": "accepted", "rows": len(rows)}
