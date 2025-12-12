# Complete End-to-End Demo Setup Package

## 📋 What's Included

This package provides **everything needed** to run a complete end-to-end demo of a multi-database NoSQL pipeline with real MongoDB, Cassandra, Redis, and Neo4j instances.

### 📁 Documentation Files (Start Here)

1. **README.md** — Project overview and quick start
2. **DEMO_SUMMARY.md** ⭐ — Visual architecture and three ways to run (READ THIS FIRST)
3. **QUICK_START.md** — Copy-paste commands for impatient users
4. **STEP_BY_STEP.md** — Detailed 9-phase checklist for learning
5. **DEMO_SETUP.md** — Complete troubleshooting and verification guide

### 🔧 Automated Demo Runner

- **`scripts/run_demo.py`** — Single command to run entire pipeline (RECOMMENDED)

### 🗄️ Database Setup & Configuration

- **`.env`** — Connection URIs (create from `env.example`)
- **`env.example`** — Template for database connections
- **`scripts/bootstrap_databases.py`** — Create MongoDB indexes and Cassandra tables

### 📊 Real-Mode Data Ingestion Scripts

- **`scripts/ingest_fields_real.py`** — MongoDB ingestion
- **`scripts/ingest_sensors_real.py`** — Cassandra ingestion
- **`scripts/aggregate_to_redis_real.py`** — Redis aggregation and alerts
- **`scripts/update_neo4j_real.py`** — Neo4j event creation

### 🔍 Cross-Database Query Examples

- **`scripts/query_mongo_low_quality.py`** — MongoDB geospatial + filter
- **`scripts/query_cassandra_timeseries.py`** — Cassandra time-series
- **`scripts/query_redis_latest.py`** — Redis latest metrics
- **`scripts/query_neo4j_relationships.py`** — Neo4j graph patterns

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Docker Containers (2 minutes)

```powershell
docker run -d --name pasture-mongo -p 27017:27017 mongo:7.0
docker run -d --name pasture-cassandra -p 9042:9042 cassandra:4.1
docker run -d --name pasture-redis -p 6379:6379 redis:7-alpine
docker run -d --name pasture-neo4j -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/changeit neo4j:5.15-community
```

Wait for Cassandra (~30 seconds). Verify: `docker ps` (should show 4 containers)

### Step 2: Setup Project (1 minute)

```powershell
cd d:\MCS\NoSQL\no_sql_pasture

# Create .env file
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

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run Demo (2-3 minutes)

```powershell
python scripts/run_demo.py
```

**Done!** Your databases now contain:
- ✅ 5 field metadata documents in MongoDB
- ✅ 384 sensor readings in Cassandra
- ✅ Aggregated metrics in Redis with alerts
- ✅ Event nodes in Neo4j

---

## 📚 Documentation Map

Choose your path based on your learning style:

```
START
│
├─→ Want the fastest path?
│   └─→ QUICK_START.md (copy-paste commands)
│
├─→ Want to understand every step?
│   └─→ STEP_BY_STEP.md (9 detailed phases)
│
├─→ Want to see the big picture?
│   └─→ DEMO_SUMMARY.md (visual architecture)
│
├─→ Prefer one command?
│   └─→ python scripts/run_demo.py
│
└─→ Having problems?
    └─→ DEMO_SETUP.md (troubleshooting section)
```

---

## 🎯 What Each Demo File Does

### QUICK_START.md
**For**: Copy-paste enthusiasts
**Content**: 
- All commands in one place
- 10-15 minute walkthrough
- No explanations, just code

**When to use**: You understand NoSQL and just want to see it working

---

### STEP_BY_STEP.md
**For**: Learners and documentation-first people
**Content**:
- 9 detailed phases
- What happens at each step
- Verification commands
- Troubleshooting for each phase

**When to use**: You want to understand the architecture and learn each step

---

### DEMO_SUMMARY.md
**For**: Visual learners and architects
**Content**:
- ASCII diagrams of data flow
- Three different ways to run demo
- Table of what each script does
- Performance expectations
- Expected output samples

**When to use**: You want the bird's eye view before diving in

---

### DEMO_SETUP.md
**For**: Advanced users, Docker newbies, troubleshooters
**Content**:
- Detailed Docker instructions
- Option A (Docker) vs Option B (Local Install)
- Verification commands for each service
- Comprehensive troubleshooting
- Detailed explanations of each step

**When to use**: 
- You're new to Docker
- You want to install databases locally instead
- Something isn't working and you need to debug

---

### README.md
**For**: Project overview
**Content**:
- What this project is
- Quick start (dry-run and real modes)
- Project structure overview
- Links to detailed docs

**When to use**: You're new to the project

---

## 🗂️ Project Structure

```
no_sql_pasture/
├── README.md ....................... Project overview
├── QUICK_START.md .................. Copy-paste commands
├── STEP_BY_STEP.md ................. 9-phase detailed walkthrough
├── DEMO_SETUP.md ................... Complete setup guide
├── DEMO_SUMMARY.md ................. Visual architecture
│
├── env.example ..................... Database connection template
├── requirements.txt ................ Python dependencies
│
├── src/ ............................ Source code
│   ├── generator.py ................ Data generator (CLI)
│   └── clients/ .................... DB client wrappers
│       ├── mongo_client.py
│       ├── cassandra_client.py
│       ├── redis_client.py
│       └── neo4j_client.py
│
├── scripts/ ........................ Pipeline scripts
│   ├── run_demo.py ................. ⭐ Automated demo (run this!)
│   ├── ingest_fields_real.py ....... MongoDB ingestion
│   ├── ingest_sensors_real.py ...... Cassandra ingestion
│   ├── aggregate_to_redis_real.py .. Redis aggregation
│   ├── update_neo4j_real.py ........ Neo4j events
│   ├── query_mongo_low_quality.py .. MongoDB queries
│   ├── query_cassandra_timeseries.py Cassandra queries
│   ├── query_redis_latest.py ....... Redis queries
│   └── query_neo4j_relationships.py Neo4j queries
│
├── docs/ ........................... Documentation
│   ├── data_models.md .............. Schema designs for all 4 DBs
│   └── queries.md .................. Example queries (CQL, Cypher, etc)
│
├── tests/ .......................... Unit tests
│   └── test_generator.py
│
├── reports/ ........................ Deliverables
│   └── final_report.md ............. Agronomic recommendations (placeholder)
│
├── presentation/ ................... Slides
│   └── slides.md ................... 12-slide outline
│
└── dashboard/ ...................... UI mockups
    └── README.md ................... Architecture diagram
```

---

## 🔄 Three Ways to Run the Demo

### Option 1: Automated (RECOMMENDED) ⭐
```powershell
python scripts/run_demo.py
```
**Time**: 2-3 minutes  
**Effort**: Minimal  
**Learning**: Medium

---

### Option 2: Step-by-Step 
Follow the 9 phases in `STEP_BY_STEP.md`

**Time**: 10-15 minutes  
**Effort**: High (but educational!)  
**Learning**: High

---

### Option 3: Copy-Paste
Use `QUICK_START.md` for all commands

**Time**: 5-10 minutes  
**Effort**: Low  
**Learning**: Low

---

## ✅ Verification Checklist

After running the demo, verify each database:

```powershell
# MongoDB: Count fields
docker exec pasture-mongo mongosh --eval "db.fields.count()"
# Expected: 5

# Cassandra: Count sensor rows
docker exec pasture-cassandra cqlsh -e "SELECT COUNT(*) FROM pasture.sensor_data_by_field;"
# Expected: 384

# Redis: List field keys
docker exec pasture-redis redis-cli KEYS "field:*"
# Expected: field:field_1, field:field_2, ...

# Neo4j: Browser (http://localhost:7474)
# Login: neo4j / changeit
# Query: MATCH (e:Event) RETURN COUNT(e)
# Expected: > 0
```

---

## 🐛 Troubleshooting

**Common issues and solutions:**

1. **"Connection refused"**
   - Check Docker containers: `docker ps`
   - Restart container: `docker restart pasture-cassandra`

2. **"Cassandra not ready"**
   - Wait 30 seconds after starting
   - Check: `docker logs pasture-cassandra | findstr "Listening"`

3. **"ModuleNotFoundError"**
   - Reinstall: `pip install -r requirements.txt`

4. **"Table already exists"**
   - Safe to ignore; it means bootstrap ran twice

5. **"Neo4j login fails"**
   - Default: `neo4j / changeit`
   - Update `.env` if changed

See `DEMO_SETUP.md` for detailed troubleshooting.

---

## 📞 File Locations

| What | File | Location |
|------|------|----------|
| Quick commands | QUICK_START.md | Root folder |
| Step-by-step | STEP_BY_STEP.md | Root folder |
| Architecture | DEMO_SUMMARY.md | Root folder |
| Deep dive | DEMO_SETUP.md | Root folder |
| Automated runner | run_demo.py | scripts/ |
| Project info | README.md | Root folder |

---

## 🎓 Learning Path

1. **First time?** → Read `DEMO_SUMMARY.md` (10 min)
2. **Ready to start?** → Use `QUICK_START.md` (5 min setup)
3. **Run demo** → `python scripts/run_demo.py` (3 min)
4. **Explore results** → View MongoDB, Cassandra, Redis, Neo4j
5. **Dig deeper?** → Read `STEP_BY_STEP.md` and modify scripts

---

## 📊 What You'll Learn

By completing this demo, you'll understand:

✅ How to set up four different NoSQL databases  
✅ How to integrate them into a single pipeline  
✅ Data flow: generation → ingestion → aggregation → queries  
✅ MongoDB: document storage + geospatial queries  
✅ Cassandra: high-throughput time-series storage  
✅ Redis: real-time aggregation and alerts  
✅ Neo4j: relationship graphs and event tracking  
✅ How to query across multiple databases  

---

## 🚦 Next Steps After Demo

1. **Modify data** — Edit `src/generator.py` for realistic scenarios
2. **Expand analysis** — Add more aggregation logic in `scripts/aggregate_to_redis_real.py`
3. **Build dashboard** — Create a Streamlit UI using the queries
4. **Add alerts** — Subscribe to Redis streams for notifications
5. **Scale up** — Test with 1000+ fields and millions of sensor readings

---

## 💡 Key Files to Remember

- **Run everything**: `python scripts/run_demo.py`
- **Quick commands**: `QUICK_START.md`
- **Step-by-step**: `STEP_BY_STEP.md`
- **Visual guide**: `DEMO_SUMMARY.md`
- **Troubleshooting**: `DEMO_SETUP.md`

---

## 🎉 You're Ready!

Start with `DEMO_SUMMARY.md` or run:

```powershell
python scripts/run_demo.py
```

**Good luck!** 🚀
