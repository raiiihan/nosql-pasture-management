# NoSQL for Pasture Management — Final Assignment

This repository contains a complete project scaffold for the final NoSQL assignment: designing and implementing a multi-database pipeline (MongoDB, Cassandra, Redis, Neo4j) to analyze pasture quality and recommend actions for farmers.

## Quick Start (Dry-Run)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Generate sample data:
```bash
python -m src.generator fields --count 3 --out fields.jsonl
python -m src.generator sensors --field-id field_1 --periods 48 --out sensors.jsonl
```

3. Run dry-run pipeline (no databases required):
```bash
python scripts/bootstrap_databases.py --dry
python scripts/ingest_pipeline.py sensors.jsonl
python scripts/aggregate_to_redis.py sensors.jsonl
python scripts/update_neo4j.py sensors.jsonl
```

## End-to-End Demo with Real Databases

For a complete demo with real MongoDB, Cassandra, Redis, and Neo4j instances:

1. **Set up databases** (using Docker):
   - See `[DEMO_SETUP.md](https://github.com/raiiihan/nosql-pasture-management/blob/master/START_HERE.md)` for step-by-step instructions with Docker commands

2. **Copy environment file** and configure connection strings:
```bash
copy env.example .env
# Edit .env with your database connection URIs
```

3. **Run the complete demo** (11 integrated steps):
```bash
python scripts/run_demo.py
```

This will generate data, create schemas, ingest into all four databases, compute aggregates, create events, and run cross-database queries.

## Project Structure

- `README.md` — This file
- `DEMO_SETUP.md` — Detailed setup instructions for real database demo
- `docs/` — Architecture, data models, and example queries
- `src/` — Core modules: generator, client wrappers (with dry-run)
- `scripts/` — Ingestion, aggregation, and query scripts
- `reports/` — Final agronomic analysis and recommendations
- `tests/` — Unit tests and validation scenarios
- `dashboard/` — Dashboard mockup and pipeline architecture
- `presentation/` — Presentation slides outline

See each folder's README for more details.
