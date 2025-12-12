# Quick Reference: End-to-End Demo Commands

## Copy-Paste Friendly Command List

### 1. Start Databases (Docker)

```powershell
docker run -d --name pasture-mongo -p 27017:27017 mongo:7.0
docker run -d --name pasture-cassandra -p 9042:9042 cassandra:4.1
docker run -d --name pasture-redis -p 6379:6379 redis:7-alpine
docker run -d --name pasture-neo4j -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/changeit neo4j:5.15-community
```

### 2. Verify Containers Running

```powershell
docker ps
```

### 3. Setup Project

```powershell
cd d:\MCS\NoSQL\no_sql_pasture
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
pip install -r requirements.txt
```

### 4. Generate Sample Data

```powershell
python -m src.generator fields --count 5 --out fields.jsonl
python -m src.generator sensors --field-id field_1 --periods 48 --out sensors_field1.jsonl
python -m src.generator sensors --field-id field_2 --periods 48 --out sensors_field2.jsonl
```

### 5. Bootstrap Databases

```powershell
python scripts/bootstrap_databases.py --real
```

### 6. Ingest Data

```powershell
python scripts/ingest_fields_real.py fields.jsonl
python scripts/ingest_sensors_real.py sensors_field1.jsonl
python scripts/ingest_sensors_real.py sensors_field2.jsonl
```

### 7. Aggregate to Redis

```powershell
python scripts/aggregate_to_redis_real.py sensors_field1.jsonl
python scripts/aggregate_to_redis_real.py sensors_field2.jsonl
```

### 8. Create Neo4j Events

```powershell
python scripts/update_neo4j_real.py sensors_field1.jsonl
python scripts/update_neo4j_real.py sensors_field2.jsonl
```

### 9. Run Queries

```powershell
python scripts/query_mongo_low_quality.py
python scripts/query_cassandra_timeseries.py
python scripts/query_redis_latest.py
python scripts/query_neo4j_relationships.py
```

### 10. View Neo4j Browser

Open browser: **http://localhost:7474**
- Login: `neo4j / changeit`
- Query: `MATCH (e:Event) RETURN e LIMIT 20`

### 11. OR Run Everything at Once

```powershell
python scripts/run_demo.py
```

## Single Command to Do It All

```powershell
# Windows PowerShell one-liner (after Docker containers started):
cd d:\MCS\NoSQL\no_sql_pasture; `
python -m src.generator fields --count 5 --out fields.jsonl; `
python -m src.generator sensors --field-id field_1 --periods 48 --out sensors_field1.jsonl; `
python -m src.generator sensors --field-id field_2 --periods 48 --out sensors_field2.jsonl; `
python scripts/bootstrap_databases.py --real; `
python scripts/ingest_fields_real.py fields.jsonl; `
python scripts/ingest_sensors_real.py sensors_field1.jsonl; `
python scripts/ingest_sensors_real.py sensors_field2.jsonl; `
python scripts/aggregate_to_redis_real.py sensors_field1.jsonl; `
python scripts/aggregate_to_redis_real.py sensors_field2.jsonl; `
python scripts/update_neo4j_real.py sensors_field1.jsonl; `
python scripts/update_neo4j_real.py sensors_field2.jsonl; `
python scripts/query_mongo_low_quality.py; `
python scripts/query_cassandra_timeseries.py; `
python scripts/query_redis_latest.py; `
python scripts/query_neo4j_relationships.py
```

## Or (Simpler - Recommended)

```powershell
python scripts/run_demo.py
```

---

## Database Connection Verification

### MongoDB
```powershell
docker exec pasture-mongo mongosh --eval "db.fields.count()"
```

### Cassandra
```powershell
docker exec pasture-cassandra cqlsh -e "SELECT COUNT(*) FROM pasture.sensor_data_by_field;"
```

### Redis
```powershell
docker exec pasture-redis redis-cli KEYS "field:*"
```

### Neo4j (Browser)
```
http://localhost:7474
```

---

## Cleanup

```powershell
docker stop pasture-mongo pasture-cassandra pasture-redis pasture-neo4j
docker rm pasture-mongo pasture-cassandra pasture-redis pasture-neo4j
```

---

**Time to complete**: ~10-15 min (including Docker startup)
