# 🚀 Frontend Deployment Guide

Complete guide to deploying the Pasture Manager Vue 3 PWA frontend.

## Quick Deploy (5 minutes)

### Option 1: Vercel (Easiest for PWA)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. From frontend/ directory
cd frontend

# 3. Deploy
vercel

# 4. Follow prompts (link to project if first time)
```

**Result:** Instant HTTPS, PWA optimized, auto-deploys on git push

### Option 2: Netlify

```bash
# 1. Build frontend
npm run build

# 2. Install Netlify CLI
npm install -g netlify-cli

# 3. Deploy
netlify deploy --prod --dir=dist
```

### Option 3: Docker + Container Registry

```bash
# Build and push to Docker Hub
docker build -t yourusername/pasture-manager:latest .
docker push yourusername/pasture-manager:latest

# Deploy to any container platform (AWS, DigitalOcean, etc)
```

## Local Testing Before Deploy

### 1. Build Optimized Production Bundle

```bash
npm run build
```

**Output:** `dist/` folder ready for serving

### 2. Test Production Build Locally

```bash
npm run preview
# Opens http://localhost:4173 with production code
```

### 3. Test PWA Installation

1. Open DevTools (F12)
2. Go to **Application → Manifest**
3. Check manifest loads correctly
4. Go to **Application → Service Workers**
5. Verify service worker registered
6. Offline test: DevTools → Network → Throttle to "Offline"
7. Try navigating—should work without network

## Production Configuration

### Backend API Connection

Update `.env.production.local` or set environment variable:

```env
VITE_API_URL=https://api.yourdomain.com
```

**Options:**

| Setup | Backend URL |
|-------|-------------|
| Local testing | http://localhost:8000 |
| Same server | https://api.yourdomain.com/api |
| Lambda/Serverless | https://lambda-id.region.amazonaws.com |

### HTTPS & Security

✅ **Required for PWA:**
- All traffic must be HTTPS
- Valid SSL certificate
- No mixed content (http + https)

✅ **Headers to set:**
```
Content-Security-Policy: default-src 'self' https://api.yourdomain.com
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Referrer-Policy: no-referrer-when-downgrade
```

### CORS Configuration

Backend must allow requests from frontend origin:

```python
# FastAPI Example
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deployment Platforms

### ✅ Vercel (Recommended for PWA)

**Pros:**
- Built for Vue/React apps
- Automatic PWA optimization
- Edge functions for serverless
- Zero-config deployment
- Free tier available

**Setup:**
```bash
cd frontend
vercel link            # Link to Vercel project
vercel env add VITE_API_URL https://api.yourdomain.com
vercel deploy --prod
```

**Cost:** Free tier includes 100GB bandwidth/month

---

### ✅ Netlify

**Pros:**
- Easy GitHub integration
- Automatic deployments
- Form handling
- Edge functions
- Free tier available

**Setup:**
1. Push to GitHub
2. Connect repo to Netlify
3. Set build command: `npm run build`
4. Set publish directory: `dist`
5. Add env variable: `VITE_API_URL`

**Cost:** Free tier includes 300 build minutes/month

---

### ✅ AWS (S3 + CloudFront)

**Pros:**
- Scalable to millions of requests
- CloudFront edge caching
- Full AWS integration
- Pay per use

**Setup:**
```bash
# 1. Create S3 bucket
aws s3 mb s3://pasture-manager-app

# 2. Build and deploy
npm run build
aws s3 sync dist/ s3://pasture-manager-app --delete

# 3. Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id E1234567 \
  --paths "/*"
```

**Cost:** ~$1-5/month for typical usage

---

### ✅ DigitalOcean App Platform

**Pros:**
- Simple pricing ($5/month minimum)
- GitHub integration
- Auto SSL
- Simple scaling

**Setup:**
1. Connect GitHub repo
2. Choose `npm` build command: `npm run build`
3. Set output directory: `dist`
4. Add env: `VITE_API_URL`
5. Deploy

**Cost:** $5/month minimum

---

### ✅ Docker + Your Server

**Pros:**
- Full control
- Run alongside backend
- No vendor lock-in
- Private infrastructure

**Dockerfile:**
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

**nginx.conf:**
```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Deploy:**
```bash
docker build -t pasture-manager:latest .
docker run -p 80:80 pasture-manager:latest
```

---

## Full Stack Deployment

### Using Docker Compose

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=http://backend:8000

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGO_URI=mongodb://mongo:27017
      - REDIS_URI=redis://redis:6379
    depends_on:
      - mongo
      - cassandra
      - redis
      - neo4j

  mongo:
    image: mongo:latest
    volumes:
      - mongo_data:/data/db

  cassandra:
    image: cassandra:latest
    environment:
      - CASSANDRA_DC=datacenter1
    volumes:
      - cassandra_data:/var/lib/cassandra

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  neo4j:
    image: neo4j:latest
    environment:
      - NEO4J_AUTH=neo4j/password
    ports:
      - "7687:7687"
    volumes:
      - neo4j_data:/data

volumes:
  mongo_data:
  cassandra_data:
  redis_data:
  neo4j_data:
```

**Deploy:**
```bash
docker compose up -d
# Frontend at http://localhost
# Backend at http://localhost:8000
```

---

## GitHub Actions CI/CD

Automatic deploy on git push:

**.github/workflows/deploy.yml:**
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Install dependencies
        run: cd frontend && npm ci
      
      - name: Build
        run: cd frontend && npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

## Monitoring & Performance

### Google PageSpeed Insights

```bash
# Install Lighthouse CLI
npm install -g @lhci/cli@^0.9.0

# Run audit
lhci autorun
```

**PWA requirements:**
- ✅ Manifest present
- ✅ Service worker installed
- ✅ Works offline
- ✅ HTTPS enabled
- ✅ Responsive design

### Performance Checklist

- [ ] Minified CSS/JS in `dist/`
- [ ] Service worker registered
- [ ] Images optimized
- [ ] Lazy loading configured
- [ ] API caching enabled
- [ ] Dark mode works
- [ ] Mobile responsive
- [ ] Load time < 3 seconds

### Sentry Error Monitoring

```javascript
// src/main.js
import * as Sentry from "@sentry/vue";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.MODE,
  tracesSampleRate: 0.1,
});
```

---

## Troubleshooting

### White screen on load?

```bash
# Check browser console for errors
# Common causes:
1. Wrong VITE_API_URL
2. CORS issue with backend
3. Missing manifest.json
4. Service worker cache issue
```

**Fix:**
```bash
# Clear all caches
npm run build
# Test locally first
npm run preview
```

### Service worker not updating?

```bash
# Hard refresh in browser
Ctrl+Shift+R (Windows)
Cmd+Shift+R (Mac)

# Or uninstall and reinstall PWA
```

### CORS errors from backend?

```python
# Backend must send these headers
Access-Control-Allow-Origin: https://yourdomain.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

### Slow API responses?

1. Check network in DevTools
2. Verify backend connection string
3. Check database query performance
4. Consider caching in Redis
5. Use CDN for static assets

---

## Rollback Procedure

### Vercel
```bash
vercel rollback
# Select previous deployment
```

### GitHub Pages
```bash
git revert <commit-hash>
git push origin main
```

### Manual
```bash
# Keep previous dist/ backup
cp -r dist dist-backup-$(date +%s)
# Deploy previous working version
aws s3 sync dist-previous/ s3://bucket --delete
```

---

## Post-Deployment Checklist

- [ ] Site loads at https://yourdomain.com
- [ ] All API endpoints responding
- [ ] Dark mode toggle works
- [ ] Field list loading data
- [ ] Charts rendering (once API ready)
- [ ] Alerts displaying
- [ ] PWA installable (Add to Home Screen)
- [ ] Service worker active
- [ ] Works offline (cached pages)
- [ ] Mobile responsive on all sizes
- [ ] Error tracking configured
- [ ] Analytics configured
- [ ] Monitoring alerts set up
- [ ] Documentation updated
- [ ] Team notified of live URL

---

## Support & Resources

- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [Vue Production Checklist](https://vuejs.org/guide/best-practices/production-deployment.html)
- [PWA Deployment](https://web.dev/progressive-web-apps/)
- [Your Hosting Platform Docs]

## Next: Backend API Setup

To complete the full stack, deploy the Python backend:
```bash
cd ../
# See DEMO_SETUP.md for Python backend deployment
```
