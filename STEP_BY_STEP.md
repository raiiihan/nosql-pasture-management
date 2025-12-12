# End-to-End Demo - Complete Step-by-Step Checklist

Follow these steps in order to set up and run the complete end-to-end demo with real databases.

## Prerequisites

- **Docker Desktop** installed and running (recommended approach)
- **PowerShell** (or bash on Linux/Mac)
- **Python 3.9+** installed locally
- **Project folder**: `d:\MCS\NoSQL\no_sql_pasture`

---

## PHASE 1: Database Setup (Using Docker)

### Step 1.1: Start all four databases

Run these commands in PowerShell (one at a time or all together):

```powershell
# Terminal Window 1: Start MongoDB
docker run -d --name pasture-mongo -p 27017:27017 mongo:7.0

# Terminal Window 2: Start Cassandra (takes ~30 seconds to warm up)
docker run -d --name pasture-cassandra -p 9042:9042 cassandra:4.1

# Terminal Window 3: Start Redis
docker run -d --name pasture-redis -p 6379:6379 redis:7-alpine

# Terminal Window 4: Start Neo4j
docker run -d --name pasture-neo4j -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/changeit neo4j:5.15-community
```

### Step 1.2: Verify all containers are running

```powershell
docker ps
```

**Expected output**: 4 containers listed as "Up"

### Step 1.3: Wait for Cassandra to be ready (~30 seconds)

```powershell
docker logs pasture-cassandra | findstr "Listening for thrift"
```

Once you see the message, Cassandra is ready.

---

## PHASE 2: Project Configuration

### Step 2.1: Navigate to project directory

```powershell
cd d:\MCS\NoSQL\no_sql_pasture
```

### Step 2.2: Create .env file with database connection strings

**Option A: Using PowerShell (automated)**

```powershell
$envContent = @"
MONGO_URI=mongodb://localhost:27017
CASSANDRA_CONTACT_POINTS=127.0.0.1
CASSANDRA_KEYSPACE=pasture
REDIS_URL=redis://localhost:6379
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=changeit
"@

$envContent | Out-File -FilePath .env -Encoding UTF8
```

**Option B: Manual (copy env.example and edit)**

```powershell
Copy-Item env.example .env
# Open .env in VS Code and fill in the values
```

### Step 2.3: Install/update Python dependencies

```powershell
pip install -r requirements.txt
```

---

## PHASE 3: Data Generation

### Step 3.1: Generate field metadata (MongoDB documents)

```powershell
python -m src.generator fields --count 5 --out fields.jsonl
```

**Output**: `fields.jsonl` file with 5 field documents

### Step 3.2: Generate sensor time-series for field_1

```powershell
python -m src.generator sensors --field-id field_1 --periods 48 --out sensors_field1.jsonl
```

**Output**: `sensors_field1.jsonl` with 192 sensor readings (48 hours × 4 sensor types)

### Step 3.3: Generate sensor time-series for field_2

```powershell
python -m src.generator sensors --field-id field_2 --periods 48 --out sensors_field2.jsonl
```

**Output**: `sensors_field2.jsonl` with 192 sensor readings

### Step 3.4: (Optional) Generate more fields

```powershell
python -m src.generator fields --count 10 --out fields_extra.jsonl
```

---

## PHASE 4: Database Bootstrap (Create Schemas/Indexes)

### Step 4.1: Create MongoDB indexes and Cassandra tables

```powershell
python scripts/bootstrap_databases.py --real
```

**Expected output**:
- MongoDB indexes created (2dsphere on boundary, 1 on farm_id)
- Cassandra table `sensor_data_by_field` created

### Step 4.2: Verify MongoDB indexes

```powershell
docker exec pasture-mongo mongosh --eval "db.fields.getIndexes()"
```

Should see `boundary_2dsphere` index.

### Step 4.3: Verify Cassandra table

```powershell
docker exec pasture-cassandra cqlsh -e "DESCRIBE TABLE pasture.sensor_data_by_field;"
```

Should show the table schema.

---

## PHASE 5: Data Ingestion

### Step 5.1: Ingest field metadata into MongoDB

```powershell
python scripts/ingest_fields_real.py fields.jsonl
```

**Expected output**: "Inserted field: field_1", "Inserted field: field_2", etc.

### Step 5.2: Ingest sensor data (field_1) into Cassandra

```powershell
python scripts/ingest_sensors_real.py sensors_field1.jsonl
```

**Expected output**: "Ingested 192 sensor rows into Cassandra..."

### Step 5.3: Ingest sensor data (field_2) into Cassandra

```powershell
python scripts/ingest_sensors_real.py sensors_field2.jsonl
```

---

## PHASE 6: Aggregation (Compute Metrics)

### Step 6.1: Aggregate metrics for field_1 and write to Redis

```powershell
python scripts/aggregate_to_redis_real.py sensors_field1.jsonl
```

**Expected output**:
- "Fields processed: 1"
- "Alerts triggered: X"
- "Metrics written to Redis"

### Step 6.2: Aggregate metrics for field_2

```powershell
python scripts/aggregate_to_redis_real.py sensors_field2.jsonl
```

### Step 6.3: Verify Redis has data

```powershell
docker exec pasture-redis redis-cli HGETALL field:field_1
```

Should see keys like `latest_ndvi`, `latest_soil_moisture`, etc.

---

## PHASE 7: Event Creation (Neo4j)

### Step 7.1: Create events for field_1 threshold crossings

```powershell
python scripts/update_neo4j_real.py sensors_field1.jsonl
```

**Expected output**: "Neo4j events created: X"

### Step 7.2: Create events for field_2

```powershell
python scripts/update_neo4j_real.py sensors_field2.jsonl
```

### Step 7.3: View Neo4j graph in browser

Open http://localhost:7474 in your web browser and log in:
- **Username**: neo4j
- **Password**: changeit

Run this Cypher query in the browser to see events:
```cypher
MATCH (e:Event) RETURN e LIMIT 20
```

---

## PHASE 8: Cross-Database Queries

### Step 8.1: Query MongoDB for low-quality fields

```powershell
python scripts/query_mongo_low_quality.py
```

**Output**: Lists fields with NDVI < 0.45

### Step 8.2: Query Cassandra time-series

```powershell
python scripts/query_cassandra_timeseries.py
```

**Output**: Grass height readings and average

### Step 8.3: Query Redis latest metrics

```powershell
python scripts/query_redis_latest.py
```

**Output**: Latest aggregated metrics for each field and active alerts

### Step 8.4: Query Neo4j relationships

```powershell
python scripts/query_neo4j_relationships.py
```

**Output**: All events, high-risk fields, event distribution

---

## PHASE 9: Automated End-to-End Demo (Optional)

Instead of running steps manually, run the entire pipeline in one go:

```powershell
python scripts/run_demo.py
```

This runs all steps 3–8 automatically and reports progress.

---

## Verification Checklist

After all steps, verify data is present in each database:

- **MongoDB**: 5 field documents
  ```powershell
  docker exec pasture-mongo mongosh --eval "db.fields.count()"
  ```

- **Cassandra**: 384 sensor rows (2 fields × 48 hours × 4 metrics)
  ```powershell
  docker exec pasture-cassandra cqlsh -e "SELECT COUNT(*) FROM pasture.sensor_data_by_field;"
  ```

- **Redis**: Latest metrics and alerts
  ```powershell
  docker exec pasture-redis redis-cli KEYS "field:*"
  ```

- **Neo4j**: Events linked to fields (view in browser at http://localhost:7474)

---

## Troubleshooting

**Issue: "Connection refused" when running ingestion scripts**

- Verify Docker containers are running: `docker ps`
- Check Cassandra is ready: `docker logs pasture-cassandra | findstr "Listening"`
- Restart container: `docker restart pasture-cassandra`

**Issue: "ModuleNotFoundError: No module named 'pymongo'"**

- Reinstall requirements: `pip install -r requirements.txt`

**Issue: Neo4j login fails**

- Default credentials are `neo4j / changeit`
- If changed, update `.env` file

**Issue: "Table already exists" error in Cassandra**

- This is expected if running bootstrap twice. It's safe to ignore.

---

## Cleanup

When done, stop and remove Docker containers:

```powershell
docker stop pasture-mongo pasture-cassandra pasture-redis pasture-neo4j
docker rm pasture-mongo pasture-cassandra pasture-redis pasture-neo4j
```

---

## Summary of Output Files

After completing all phases, you'll have:

- **Generated data**: `fields.jsonl`, `sensors_field1.jsonl`, `sensors_field2.jsonl`
- **Populated databases**:
  - MongoDB: `pasture.fields` collection
  - Cassandra: `pasture.sensor_data_by_field` table
  - Redis: Hash keys (`field:field_1`, etc.) and Stream (`alerts`)
  - Neo4j: Event nodes and Field nodes with relationships

---

## Next Steps (After Demo)

1. **Expand data**: Generate more fields/sensors and run multi-field analysis
2. **Build analytics**: Add more sophisticated aggregations (e.g., anomaly detection, forecasting)
3. **Create dashboard**: Build a Streamlit/Flask UI to visualize results
4. **Add alerts**: Implement real-time alert notifications
5. **Geospatial analysis**: Use MongoDB geospatial queries to find nearby fields with similar issues

---

**Estimated time to complete**: 10–15 minutes (including Docker startup time)
