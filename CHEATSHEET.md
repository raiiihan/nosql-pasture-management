# 📱 Quick Reference - Developer Cheatsheet

## Frontend Commands

```bash
# From frontend/ directory
npm install              # Install dependencies
npm run dev             # Start dev server (http://localhost:5173)
npm run build           # Production build
npm run preview         # Preview production build
npm run lint            # Lint code
npm run format          # Format with Prettier
```

## Backend Commands

```bash
# From project root
python -m venv venv                          # Create env
source venv/bin/activate                     # Activate (Windows: venv\Scripts\activate)

# Dependencies
pip install -r requirements.txt              # Install all packages
pip freeze > requirements.txt                # Update requirements

# Generator
python src/generator.py generate-field -f "Field Name" -c 10
python src/generator.py generate-series -p 7 --output data.jsonl
python src/generator.py generate-field --help

# Database Setup
python scripts/bootstrap_databases.py        # Dry-run (show operations)
python scripts/bootstrap_databases.py --real # Real (execute)

# Ingestion
python scripts/ingest_fields_real.py
python scripts/ingest_sensors_real.py

# Aggregation
python scripts/aggregate_to_redis_real.py
python scripts/update_neo4j_real.py

# Queries
python scripts/query_mongo_low_quality.py
python scripts/query_cassandra_timeseries.py
python scripts/query_redis_latest.py
python scripts/query_neo4j_relationships.py

# Full Demo
python scripts/run_demo.py                   # 11-step pipeline

# Tests
pytest tests/test_generator.py -v            # Run tests
pytest tests/ --cov=src                      # With coverage
```

## Docker Commands

```bash
# Start all databases
docker compose up -d

# Stop all databases
docker compose down

# View logs
docker compose logs -f mongo
docker compose logs -f cassandra
docker compose logs -f redis
docker compose logs -f neo4j

# Remove all data
docker compose down -v

# Build full stack image
docker build -t pasture-manager:latest .

# Run full stack container
docker run -p 80:80 -p 8000:8000 pasture-manager:latest
```

## Database Connections

### MongoDB
```
URI: mongodb://localhost:27017
Database: pasture
Collections: fields
```

### Cassandra
```
Host: localhost:9042
Keyspace: pasture
Table: sensor_readings
```

### Redis
```
Host: localhost:6379
Database: 0
Streams: alerts_*
Hashes: field_*_latest
```

### Neo4j
```
URI: bolt://localhost:7687
Auth: neo4j / password
Database: neo4j
```

## API Client Usage

### Fetch Data
```javascript
import { apiClient } from '@/api/client'

// GET request
const fields = await apiClient.get('/fields')

// GET with params
const field = await apiClient.get('/fields/1', {
  params: { includeMetrics: true }
})

// POST request
const result = await apiClient.post('/alerts/1/read', { })

// Error handling
try {
  const data = await apiClient.get('/fields')
} catch (error) {
  console.error(error.response?.data || error.message)
}
```

## Vue 3 Composition API

### Basic Component
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)

onMounted(() => {
  console.log('Component mounted')
})

const increment = () => count.value++
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Doubled: {{ doubled }}</p>
    <button @click="increment">+1</button>
  </div>
</template>
```

## Tailwind CSS Classes

```html
<!-- Spacing -->
<div class="p-4 m-2 gap-4">

<!-- Text -->
<p class="text-lg font-bold text-gray-900 dark:text-white">

<!-- Colors -->
<button class="bg-emerald-500 text-white hover:bg-emerald-600">

<!-- Responsive -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

<!-- Components (custom) -->
<div class="card">
<button class="btn btn-primary">
<span class="badge badge-success">
```

## Environment Variables

### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:8000
VITE_PWA_ENABLED=true
```

### Backend (.env)
```env
MONGO_URI=mongodb://localhost:27017
CASSANDRA_CONTACT_POINTS=localhost
CASSANDRA_KEYSPACE=pasture
REDIS_URI=redis://localhost:6379
NEO4J_URI=bolt://localhost:7687
NEO4J_AUTH_USER=neo4j
NEO4J_AUTH_PASS=password
```

## File Paths

| Path | Purpose |
|------|---------|
| `frontend/src/views/` | Page components |
| `frontend/src/components/` | Reusable components |
| `frontend/src/api/` | API client |
| `frontend/src/router/` | Routes |
| `src/clients/` | DB wrappers |
| `src/generator.py` | Data generation |
| `scripts/` | Pipeline scripts |
| `tests/` | Test files |
| `docs/` | Documentation |

## Common Errors & Fixes

### CORS Error
```
Access-Control-Allow-Origin missing
→ Backend needs CORS middleware configured
```

### Cannot find module
```
ModuleNotFoundError: No module named 'xxx'
→ pip install -r requirements.txt
→ Check PYTHONPATH
```

### Port already in use
```
Address already in use
→ Kill process: lsof -ti:8000 | xargs kill -9
→ Or use different port: npm run dev -- --port 3000
```

### Database connection failed
```
Connection refused
→ docker compose up -d
→ Verify connection string in .env
```

### Service worker not updating
```
Stale cache
→ Hard refresh: Ctrl+Shift+R
→ Clear storage: DevTools → Application → Clear
```

## Performance Tips

- Use `lazy` import for large components
- Implement virtual scrolling for long lists
- Cache API responses with Redis
- Minify images and assets
- Enable gzip compression
- Use CDN for static files

## Debugging

### Frontend
```javascript
// Console logging
console.log('Value:', value)

// DevTools Network tab
// Check API requests/responses

// Vue DevTools extension
// Chrome/Firefox extension for Vue debugging

// Lighthouse audit
// DevTools → Lighthouse
```

### Backend
```python
# Logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Message")

# Database shell
mongosh mongodb://localhost:27017
cqlsh localhost 9042
redis-cli
cypher-shell -a neo4j/password
```

## Git Workflow

```bash
# Clone
git clone <repo>
cd no_sql_pasture

# Branch
git checkout -b feature/new-feature

# Commit
git add .
git commit -m "feat: add new feature"

# Push
git push origin feature/new-feature

# Pull Request
# Create on GitHub

# Merge & Delete
git checkout main
git pull origin main
git branch -d feature/new-feature
```

## Deployment Quick Links

- **Frontend**: `FRONTEND_DEPLOYMENT.md`
- **Backend**: `DEMO_SETUP.md`
- **Full Stack**: `COMPLETE_PROJECT_SETUP.md`
- **Troubleshooting**: `DEMO_SETUP.md`

## Documentation Index

| File | Purpose |
|------|---------|
| README.md | Project overview |
| QUICK_START.md | 5-min setup |
| STEP_BY_STEP.md | 9-phase guide |
| COMPLETE_PROJECT_SETUP.md | Full setup |
| FRONTEND_DEPLOYMENT.md | Deploy frontend |
| DEMO_SETUP.md | Troubleshooting |
| DEMO_SUMMARY.md | Architecture |

## Resources

- [Vue 3 Docs](https://vuejs.org/)
- [Tailwind Docs](https://tailwindcss.com/)
- [Vite Docs](https://vitejs.dev/)
- [MongoDB Docs](https://docs.mongodb.com/)
- [Cassandra Docs](https://cassandra.apache.org/doc/)
- [Redis Docs](https://redis.io/docs/)
- [Neo4j Docs](https://neo4j.com/docs/)
- [PWA Docs](https://web.dev/progressive-web-apps/)

## Need Help?

1. Check relevant .md file (see index)
2. Run demo: `python scripts/run_demo.py`
3. Check Docker: `docker compose ps`
4. Check logs: `docker compose logs -f <service>`
5. Reset: `docker compose down -v && npm install`

---

**Happy coding! 🚀**
