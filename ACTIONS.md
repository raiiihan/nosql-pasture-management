# End-to-End Demo: Action Checklist

## 🎯 Complete Action-by-Action Checklist

Copy and paste this into a file or checklist app to track your progress.

---

## PHASE 1: Prerequisites (Before Starting)

- [ ] Docker Desktop is installed and running
- [ ] You can run `docker ps` command successfully
- [ ] Python 3.9+ is installed (`python --version` works)
- [ ] You have access to `d:\MCS\NoSQL\no_sql_pasture` folder

---

## PHASE 2: Start Docker Containers (~2 minutes)

**Run these 4 commands in PowerShell (one at a time or paste all at once):**

```
docker run -d --name pasture-mongo -p 27017:27017 mongo:7.0
docker run -d --name pasture-cassandra -p 9042:9042 cassandra:4.1
docker run -d --name pasture-redis -p 6379:6379 redis:7-alpine
docker run -d --name pasture-neo4j -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/changeit neo4j:5.15-community
```

**Verification:**
- [ ] `docker ps` shows 4 containers with "Up" status
- [ ] Wait ~30 seconds for Cassandra to be ready

---

## PHASE 3: Project Setup (~3 minutes)

**In PowerShell, run:**

```powershell
cd d:\MCS\NoSQL\no_sql_pasture
```

- [ ] Current folder is `d:\MCS\NoSQL\no_sql_pasture`

**Create .env file:**

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

- [ ] `.env` file created in project root

**Install dependencies:**

```powershell
pip install -r requirements.txt
```

- [ ] No errors during pip install
- [ ] All packages installed successfully

---

## PHASE 4: Generate Sample Data (~2 minutes)

**Generate field metadata:**

```powershell
python -m src.generator fields --count 5 --out fields.jsonl
```

- [ ] `fields.jsonl` created (should contain 5 lines)

**Generate sensor time-series for field_1:**

```powershell
python -m src.generator sensors --field-id field_1 --periods 48 --out sensors_field1.jsonl
```

- [ ] `sensors_field1.jsonl` created (should contain 192 lines)

**Generate sensor time-series for field_2:**

```powershell
python -m src.generator sensors --field-id field_2 --periods 48 --out sensors_field2.jsonl
```

- [ ] `sensors_field2.jsonl` created (should contain 192 lines)

---

## PHASE 5: Bootstrap Databases (~1 minute)

**Create MongoDB indexes and Cassandra table:**

```powershell
python scripts/bootstrap_databases.py --real
```

- [ ] No errors; indexes and table created

**Verify MongoDB indexes:**

```powershell
docker exec pasture-mongo mongosh --eval "db.fields.getIndexes()"
```

- [ ] See `boundary_2dsphere` index in output

**Verify Cassandra table:**

```powershell
docker exec pasture-cassandra cqlsh -e "DESCRIBE TABLE pasture.sensor_data_by_field;"
```

- [ ] See table schema in output

---

## PHASE 6: Ingest Data to MongoDB (~1 minute)

**Ingest field metadata:**

```powershell
python scripts/ingest_fields_real.py fields.jsonl
```

- [ ] Output shows "Inserted field: field_1", etc.
- [ ] 5 fields inserted successfully

**Verify in MongoDB:**

```powershell
docker exec pasture-mongo mongosh --eval "db.fields.count()"
```

- [ ] Output: `5`

---

## PHASE 7: Ingest Data to Cassandra (~1 minute)

**Ingest sensor data for field_1:**

```powershell
python scripts/ingest_sensors_real.py sensors_field1.jsonl
```

- [ ] Output shows "Ingested 192 sensor rows..."

**Ingest sensor data for field_2:**

```powershell
python scripts/ingest_sensors_real.py sensors_field2.jsonl
```

- [ ] Output shows "Ingested 192 sensor rows..."

**Verify in Cassandra:**

```powershell
docker exec pasture-cassandra cqlsh -e "SELECT COUNT(*) FROM pasture.sensor_data_by_field;"
```

- [ ] Output: `384` (192 + 192)

---

## PHASE 8: Aggregate to Redis (~1 minute)

**Aggregate field_1 metrics:**

```powershell
python scripts/aggregate_to_redis_real.py sensors_field1.jsonl
```

- [ ] Output shows "Fields processed: 1" and alerts triggered
- [ ] Output shows "Metrics written to Redis"

**Aggregate field_2 metrics:**

```powershell
python scripts/aggregate_to_redis_real.py sensors_field2.jsonl
```

- [ ] Output shows "Fields processed: 1"

**Verify in Redis:**

```powershell
docker exec pasture-redis redis-cli HGETALL field:field_1
```

- [ ] Output shows keys like `latest_ndvi`, `latest_soil_moisture`, etc.

---

## PHASE 9: Create Neo4j Events (~1 minute)

**Create events for field_1:**

```powershell
python scripts/update_neo4j_real.py sensors_field1.jsonl
```

- [ ] Output shows "Neo4j events created: X"

**Create events for field_2:**

```powershell
python scripts/update_neo4j_real.py sensors_field2.jsonl
```

- [ ] Output shows "Neo4j events created: X"

**View Neo4j graph:**

Open browser: **http://localhost:7474**

- [ ] Neo4j login page appears
- [ ] Log in: Username `neo4j`, Password `changeit`
- [ ] Run query: `MATCH (e:Event) RETURN e LIMIT 20`
- [ ] See Event nodes displayed

---

## PHASE 10: Run Cross-Database Queries (~2 minutes)

**Query MongoDB for low NDVI fields:**

```powershell
python scripts/query_mongo_low_quality.py
```

- [ ] Output shows fields with NDVI < 0.45

**Query Cassandra time-series:**

```powershell
python scripts/query_cassandra_timeseries.py
```

- [ ] Output shows grass height readings and average

**Query Redis latest metrics:**

```powershell
python scripts/query_redis_latest.py
```

- [ ] Output shows latest metrics for each field and alerts

**Query Neo4j relationships:**

```powershell
python scripts/query_neo4j_relationships.py
```

- [ ] Output shows events and high-risk fields

---

## FINAL VERIFICATION

Check that all databases have data:

```powershell
# MongoDB count
docker exec pasture-mongo mongosh --eval "db.fields.count()"
# Expected: 5
- [ ] Result is 5

# Cassandra count
docker exec pasture-cassandra cqlsh -e "SELECT COUNT(*) FROM pasture.sensor_data_by_field;"
# Expected: 384
- [ ] Result is 384

# Redis keys
docker exec pasture-redis redis-cli KEYS "field:*"
# Expected: field:field_1, field:field_2, ...
- [ ] At least 2 field keys present

# Neo4j events
# Expected: See Event nodes in browser query
- [ ] http://localhost:7474 shows events
```

---

## 🎉 SUCCESS!

You have successfully completed an end-to-end demo with:

✅ MongoDB: 5 field documents with geospatial indexes  
✅ Cassandra: 384 sensor rows with time-series data  
✅ Redis: Aggregated metrics and alerts  
✅ Neo4j: Event nodes linked to fields  

---

## 🔧 Optional: Faster Alternative

Instead of running all steps manually, run everything at once:

```powershell
python scripts/run_demo.py
```

- [ ] All steps completed successfully
- [ ] All databases populated
- [ ] All queries executed

---

## 🛑 Troubleshooting

If any step fails, refer to:

1. **Quick Reference**: `QUICK_START.md`
2. **Detailed Steps**: `STEP_BY_STEP.md`
3. **Setup Guide**: `DEMO_SETUP.md` (troubleshooting section)
4. **Visual Architecture**: `DEMO_SUMMARY.md`

---

## ✅ Sign-Off

**Date Completed**: _______________

**By**: _______________

**Comments**: _______________________________________________

---

**Total Time**: ~15-20 minutes (including Docker startup and verification)

**Next Steps**: 
- [ ] Review the generated data in each database
- [ ] Modify `src/generator.py` to create realistic scenarios
- [ ] Extend queries for more complex analysis
- [ ] Build a dashboard to visualize results

---

**Congratulations! You now have a working multi-database NoSQL system!** 🚀
