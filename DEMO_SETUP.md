# End-to-End Demo Setup Guide

This guide walks you through setting up real databases and running a complete end-to-end pipeline demo (not dry-run).

## Option A: Using Docker (Recommended - Fastest)

### Prerequisites
- Docker Desktop installed and running on your machine.

### Step 1: Start all four databases in Docker

Run these commands in PowerShell from any directory (not necessarily the project folder):

```powershell
# Start MongoDB on port 27017
docker run -d --name pasture-mongo -p 27017:27017 mongo:7.0

# Start Cassandra on port 9042 (takes ~30 seconds to be ready)
docker run -d --name pasture-cassandra -p 9042:9042 cassandra:4.1

# Start Redis on port 6379
docker run -d --name pasture-redis -p 6379:6379 redis:7-alpine

# Start Neo4j on port 7687 (bolt) and 7474 (browser)
docker run -d --name pasture-neo4j -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/changeit neo4j:5.15-community
```

**Verify all containers started:**
```powershell
docker ps
```

Expected output: 4 running containers (pasture-mongo, pasture-cassandra, pasture-redis, pasture-neo4j).

**Wait for Cassandra to be ready** (it takes ~30 seconds after container starts):
```powershell
docker logs pasture-cassandra | findstr "Listening for thrift clients"
```
Once you see "Listening for thrift clients", Cassandra is ready.

### Step 2: Update `.env` file

Copy `env.example` to `.env` and fill in the connection strings:

```powershell
cd d:\MCS\NoSQL\no_sql_pasture

# Copy the example env file
Copy-Item env.example -Destination .env

# Edit .env with these values (or use your editor):
# MONGO_URI=mongodb://localhost:27017
# CASSANDRA_CONTACT_POINTS=127.0.0.1
# CASSANDRA_KEYSPACE=pasture
# REDIS_URL=redis://localhost:6379
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=changeit
```

Open `.env` in VS Code and verify the lines above are set (or use PowerShell to set them):

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

### Step 3: Generate sample sensor data

```powershell
# From project root
cd d:\MCS\NoSQL\no_sql_pasture

# Generate 5 fields (MongoDB documents)
python -m src.generator fields --count 5 --out fields.jsonl

# Generate 48 hours of sensor readings for field_1 (Cassandra time-series)
python -m src.generator sensors --field-id field_1 --periods 48 --out sensors_field1.jsonl

# Generate readings for field_2 (to show multiple fields)
python -m src.generator sensors --field-id field_2 --periods 48 --out sensors_field2.jsonl
```

### Step 4: Bootstrap the databases (create schemas, indexes, tables)

This step creates MongoDB indexes and Cassandra tables in the real databases:

```powershell
# Run bootstrap in REAL mode (not dry-run)
python scripts/bootstrap_databases.py --real
```

Expected output: No dry-run tags; scripts will actually create indexes/tables in your Docker containers.

**Verify MongoDB:**
```powershell
docker exec pasture-mongo mongosh --eval "db.fields.getIndexes()"
```

**Verify Cassandra table exists:**
```powershell
docker exec pasture-cassandra cqlsh -e "DESCRIBE TABLE pasture.sensor_data_by_field;"
```

### Step 5: Run the ingestion pipeline

This reads the generated JSONL files and writes to the actual databases:

```powershell
# Create an enhanced ingest script that reads from .env and runs in real mode
# (I'll provide this below in Step 5.1)

# For now, run the scripts with real mode enabled:
# Ingest field metadata into MongoDB
python scripts/ingest_fields_real.py fields.jsonl

# Ingest sensor data into Cassandra
python scripts/ingest_sensors_real.py sensors_field1.jsonl
python scripts/ingest_sensors_real.py sensors_field2.jsonl
```

(See "Real-Mode Scripts" section below to create these scripts.)

### Step 6: Run aggregation job (compute metrics → Redis)

```powershell
# Read sensor data, compute rolling metrics, write to Redis
python scripts/aggregate_to_redis_real.py sensors_field1.jsonl
python scripts/aggregate_to_redis_real.py sensors_field2.jsonl
```

**Verify Redis has data:**
```powershell
docker exec pasture-redis redis-cli HGETALL field:field_1
```

You should see keys like: `latest_ndvi`, `latest_soil_moisture`, etc.

### Step 7: Create graph relationships in Neo4j

```powershell
# Create event nodes and link to fields when thresholds are crossed
python scripts/update_neo4j_real.py sensors_field1.jsonl
python scripts/update_neo4j_real.py sensors_field2.jsonl
```

**View Neo4j graph in browser:**
Open http://localhost:7474 and log in with:
- User: `neo4j`
- Password: `changeit`

Run Cypher query to see events:
```cypher
MATCH (e:Event) RETURN e LIMIT 10
```

### Step 8: Run example queries across all systems

**MongoDB: Find fields with low NDVI**
```powershell
# (See Query Scripts section below)
python scripts/query_mongo_low_quality.py
```

**Cassandra: Time-series aggregation**
```powershell
python scripts/query_cassandra_timeseries.py
```

**Redis: Get latest metrics**
```powershell
python scripts/query_redis_latest.py
```

**Neo4j: Find related fields**
```powershell
python scripts/query_neo4j_relationships.py
```

---

## Option B: Local Installation (If you prefer not to use Docker)

### For each database, install and start the service locally:

**MongoDB:**
- Download: https://www.mongodb.com/try/download/community
- Install and start the service (Windows: `mongod.exe` in MongoDB bin folder)
- Default: `mongodb://localhost:27017`

**Cassandra:**
- Download: https://cassandra.apache.org/download/
- Start: run `bin\cassandra.bat` from Cassandra folder
- Contact point: `127.0.0.1:9042`

**Redis:**
- Download: https://github.com/microsoftarchive/redis/releases (Windows binary)
- Start: `redis-server.exe`
- Default: `redis://localhost:6379`

**Neo4j:**
- Download: https://neo4j.com/download/
- Start the service (Desktop app or command-line)
- Bolt: `bolt://localhost:7687`

Then follow Steps 2–8 above (same as Docker).

---

## Real-Mode Scripts

Below are the three enhanced scripts you need to create. Save these in the `scripts/` folder.

### `scripts/ingest_fields_real.py`
Reads field JSONL and writes to MongoDB (real mode).

### `scripts/ingest_sensors_real.py`
Reads sensor JSONL and writes to Cassandra (real mode).

### `scripts/aggregate_to_redis_real.py`
Reads sensor JSONL, computes metrics, writes to Redis (real mode).

### `scripts/update_neo4j_real.py`
Reads sensor JSONL, creates Neo4j events (real mode).

### Query Scripts

Create these to demonstrate cross-DB queries:

### `scripts/query_mongo_low_quality.py`
MongoDB geospatial + NDVI query.

### `scripts/query_cassandra_timeseries.py`
Cassandra time-series aggregation.

### `scripts/query_redis_latest.py`
Redis hash lookups for latest metrics.

### `scripts/query_neo4j_relationships.py`
Neo4j graph pattern queries.

---

## Troubleshooting

**Cassandra not ready:**
```powershell
docker logs pasture-cassandra
```
Wait for: "Listening for thrift clients on /0.0.0.0:9160"

**MongoDB connection refused:**
```powershell
docker restart pasture-mongo
```

**Neo4j auth failed:**
Default credentials are `neo4j / changeit`. If changed, update `.env`.

**Redis connection issues:**
```powershell
docker exec pasture-redis redis-cli ping
```
Should return `PONG`.

---

## Cleanup (when done)

Stop and remove containers:
```powershell
docker stop pasture-mongo pasture-cassandra pasture-redis pasture-neo4j
docker rm pasture-mongo pasture-cassandra pasture-redis pasture-neo4j
```

---

## Next: I'll create the real-mode scripts below
