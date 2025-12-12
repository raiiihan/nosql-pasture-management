# End-to-End Demo Setup — Visual Summary

┌─────────────────────────────────────────────────────────────┐
│          End-to-End Data Pipeline Architecture             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Generator                                                  │
│  ├─ 5 field metadata documents                             │
│  └─ 384 sensor readings (48 hrs × 2 fields × 4 sensors)   │
│     ↓                                                       │
│  MongoDB              Cassandra         Redis       Neo4j   │
│  ├─ fields            ├─ Time-series    ├─ Hashes   ├─ Events
│  │  (geospatial)      │  (with TTL)     │  (latest  │ (threshold
│  │  5 docs            │  384 rows       │   metrics)│  crossings)
│  │  ✓ indexes         │  ✓ table        │  ✓ streams
│  └─ 2dsphere         └─ created         └─ created  └─ created
│     index                                                   │
└─────────────────────────────────────────────────────────────┘
```

## Three Ways to Run the Demo

### Option 1: Automated (Recommended)
**Single command runs everything:**
```powershell
python scripts/run_demo.py
```
⏱️ **Time**: ~2-3 minutes for full pipeline

---

### Option 2: Step-by-Step (Most Educational)
Follow `STEP_BY_STEP.md` for 9 detailed phases with verification at each stage.

⏱️ **Time**: ~15 minutes + time to understand each step

---

### Option 3: Quick Copy-Paste
Use `QUICK_START.md` for command-line reference.

⏱️ **Time**: ~10 minutes

---

## Database Setup (Same for All Options)

### Prerequisites
- ✅ Docker Desktop running
- ✅ PowerShell or bash terminal
- ✅ Python 3.9+

### Phase 0: Start Docker Containers (1-2 minutes)

```powershell
# These 4 commands start MongoDB, Cassandra, Redis, Neo4j
docker run -d --name pasture-mongo -p 27017:27017 mongo:7.0
docker run -d --name pasture-cassandra -p 9042:9042 cassandra:4.1
docker run -d --name pasture-redis -p 6379:6379 redis:7-alpine
docker run -d --name pasture-neo4j -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/changeit neo4j:5.15-community
```

**Verify**: `docker ps` (should show 4 containers)

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA GENERATION                         │
│  fields.jsonl (5 documents) + sensors*.jsonl (384 rows)   │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                   BOOTSTRAP PHASE                          │
│  ✓ Create MongoDB indexes (geospatial, farm_id)           │
│  ✓ Create Cassandra table (sensor_data_by_field)          │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ MongoDB  │  │Cassandra │  │  Redis   │
│ INGESTION│  │INGESTION │  │AGGREG.  │
│ 5 fields │  │192 rows  │  │Metrics  │
│          │  │(field_1) │  │         │
│          │  │192 rows  │  │Alerts   │
│          │  │(field_2) │  │         │
└──────────┘  └──────────┘  └──────────┘
        │          │          │
        └──────────┼──────────┘
                   │
        ┌──────────▼──────────┐
        │   Neo4j UPDATES     │
        │ Event nodes created │
        │ (threshold crossings)
        └─────────────────────┘
                   │
        ┌──────────▼──────────────────┐
        │  CROSS-DATABASE QUERIES     │
        ├─────────────────────────────┤
        │ 1. MongoDB low NDVI fields  │
        │ 2. Cassandra time-series avg│
        │ 3. Redis latest metrics     │
        │ 4. Neo4j event relationships
        └─────────────────────────────┘
```

---

## What Each Script Does

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `run_demo.py` | **Run entire pipeline** | None (auto-generates) | All databases populated |
| `ingest_fields_real.py` | Ingest to MongoDB | `fields.jsonl` | 5 field documents |
| `ingest_sensors_real.py` | Ingest to Cassandra | `sensors*.jsonl` | 384 sensor rows |
| `aggregate_to_redis_real.py` | Compute metrics → Redis | `sensors*.jsonl` | Hashes + alerts |
| `update_neo4j_real.py` | Create events | `sensors*.jsonl` | Event nodes |
| `query_mongo_low_quality.py` | Query low NDVI fields | None | List of fields |
| `query_cassandra_timeseries.py` | Query time-series | None | Grass height avg |
| `query_redis_latest.py` | Get latest metrics | None | All metrics + alerts |
| `query_neo4j_relationships.py` | Query graph | None | Events & relationships |

---

## Expected Output

After running `python scripts/run_demo.py`, you'll see output like:

```
======================================================================
STEP: Generate 5 field metadata documents
======================================================================
✓ Generate 5 field metadata documents completed successfully

======================================================================
STEP: Generate 48-hour sensor data for field_1
======================================================================
✓ Generate 48-hour sensor data for field_1 completed successfully

[... more steps ...]

======================================================================
CROSS-DATABASE QUERIES
======================================================================
STEP: MongoDB: Find fields with low NDVI
======================================================================
Found 2 fields with NDVI < 0.45:

  Field: field_1
    Name: Pasture field_1
    Farm: farm_1
    NDVI: 0.38
    Soil Type: loam

[... more results ...]

======================================================================
All steps completed successfully!

Your databases now contain:
  • MongoDB: 5 field documents with metadata
  • Cassandra: 384 sensor readings (48 hours × 2 fields × 4 metrics)
  • Redis: Latest metrics and aggregates, plus alert events
  • Neo4j: Event nodes linked to fields (threshold crossings)

Next steps:
  • View Neo4j graph at: http://localhost:7474
  • Explore MongoDB with: mongosh
  • Query Redis with: redis-cli
```

---

## View Results

### MongoDB
- **Tool**: Mongosh or MongoDB Compass
- **Command**: `docker exec pasture-mongo mongosh`
- **Query**: `db.fields.findOne()`

### Cassandra
- **Tool**: cqlsh
- **Command**: `docker exec pasture-cassandra cqlsh`
- **Query**: `SELECT * FROM pasture.sensor_data_by_field LIMIT 10;`

### Redis
- **Tool**: redis-cli
- **Command**: `docker exec pasture-redis redis-cli`
- **Query**: `HGETALL field:field_1`

### Neo4j
- **Tool**: Browser (http://localhost:7474)
- **Credentials**: neo4j / changeit
- **Query**: `MATCH (e:Event) RETURN e LIMIT 20`

---

## Performance Expectations

| Database | Operation | Throughput | Latency |
|----------|-----------|-----------|---------|
| **MongoDB** | Insert field | 1000+ docs/sec | <10ms |
| **Cassandra** | Insert sensor | 10,000+ rows/sec | <5ms |
| **Redis** | HSET latest | 100,000+ ops/sec | <1ms |
| **Neo4j** | Create event | 1000+ nodes/sec | <20ms |

---

## Next Steps

After the demo:

1. **Modify data generation** — Edit `src/generator.py` to create realistic farm scenarios
2. **Add more fields** — Generate 100+ fields and observe multi-field behavior
3. **Implement alerts** — Subscribe to Redis streams for real-time notifications
4. **Build dashboard** — Use Streamlit to visualize results
5. **Geospatial queries** — Use MongoDB's geospatial features to find nearby fields with issues

---

## File Reference

```
DEMO_SETUP.md ..................... Detailed Docker setup guide
STEP_BY_STEP.md ................... Complete step-by-step checklist
QUICK_START.md .................... Quick command reference
README.md ......................... Project overview
scripts/
  ├── run_demo.py ................. Automated end-to-end runner
  ├── ingest_*.py ................. Real-mode ingestion scripts
  ├── aggregate_to_redis_real.py .. Aggregation to Redis
  ├── update_neo4j_real.py ........ Event creation
  ├── query_*.py .................. Cross-DB query examples
```

---

**Ready? Start here:**

```bash
# Option 1 (Easiest):
python scripts/run_demo.py

# Option 2 (Educational):
Read STEP_BY_STEP.md and follow the 9 phases

# Option 3 (Quick Reference):
Use QUICK_START.md to copy-paste commands
```

**Estimated time**: 2-15 minutes (depending on option)
