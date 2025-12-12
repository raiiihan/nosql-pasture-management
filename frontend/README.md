# 🌾 Pasture Manager - Frontend

Modern, responsive Vue 3 + Tailwind CSS PWA for real-time farm analytics.

## Features

✨ **Modern Design**
- Vue 3 with Composition API
- Tailwind CSS utility-first styling
- Dark mode support with persistent theme
- Fully responsive (mobile, tablet, desktop)

📱 **Progressive Web App**
- Service worker offline support
- Add to homescreen capability
- Installable on all devices
- Fast load times with Vite build

🔄 **Real-Time Analytics**
- Live field metrics and status
- Time-series charting (Chart.js ready)
- Geospatial visualization (Leaflet ready)
- Real-time alert management

📊 **Dashboard Features**
- Farm overview with key metrics
- Field performance table
- Alert prioritization
- Status indicators and badges

## Project Structure

```
frontend/
├── public/
│   └── manifest.json          # PWA manifest
├── src/
│   ├── api/
│   │   └── client.js          # Axios HTTP client
│   ├── components/
│   │   └── [future components]
│   ├── composables/
│   │   └── [future composables]
│   ├── stores/
│   │   └── [future Pinia stores]
│   ├── views/
│   │   ├── Dashboard.vue      # Main dashboard
│   │   ├── Fields.vue         # Field list/grid view
│   │   ├── Analytics.vue      # Time-series analytics
│   │   ├── Alerts.vue         # Alert management
│   │   └── Settings.vue       # User preferences
│   ├── App.vue                # Root component
│   ├── main.js                # App bootstrap
│   ├── router/
│   │   └── index.js           # Vue Router config
│   └── style.css              # Global Tailwind styles
├── index.html                 # PWA entry point
├── vite.config.js             # Vite config with PWA plugin
├── tailwind.config.js         # Tailwind theme
├── postcss.config.js          # PostCSS with Tailwind
├── package.json               # Dependencies
└── README.md                  # This file
```

## Installation

### Prerequisites
- Node.js 16+ (recommend 18 LTS)
- npm or yarn

### Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start dev server:**
   ```bash
   npm run dev
   ```
   Opens at `http://localhost:5173` with hot module reloading

3. **Build for production:**
   ```bash
   npm run build
   ```
   Output in `dist/` directory ready for deployment

4. **Preview production build:**
   ```bash
   npm run preview
   ```

## Configuration

### Environment Variables

Create `.env.local` in the frontend root:

```env
# API endpoint (backend)
VITE_API_URL=http://localhost:8000

# Optional: PWA settings
VITE_PWA_ENABLED=true
```

### Tailwind Customization

Edit `tailwind.config.js` to customize:
- Color palette (emerald green theme preset)
- Typography and spacing
- Dark mode behavior
- Custom animations

### API Configuration

Edit `src/api/client.js` to customize:
- Base URL and timeout
- Request/response interceptors
- Error handling
- Authentication headers

## Architecture

### Components Hierarchy
```
App (nav + routing)
├── Dashboard (overview)
├── Fields (list/grid)
├── Analytics (charts)
├── Alerts (notifications)
└── Settings (preferences)
```

### State Management
- **Pinia stores** (planned): fieldsStore, alertsStore, uiStore
- **Local state**: Component-level with Vue 3 Composition API
- **API caching**: Axios with custom interceptors

### PWA Capabilities
- **Service Worker**: Vite PWA plugin with Workbox
- **Offline**: Precache app shell, runtime cache for API
- **Installation**: Manifest with shortcuts and screenshots
- **Theme**: Emerald green with automatic dark mode

## Development

### Code Style
- Vue 3 Composition API (setup scripts)
- Scoped styles with Tailwind CSS
- PascalCase components
- camelCase functions/variables

### Adding a New View

1. Create `src/views/NewView.vue` with template + script setup
2. Add route to `src/router/index.js`
3. Add navigation link to `App.vue` and mobile nav
4. Use Tailwind classes for styling

### Using Tailwind Components

Pre-defined in `src/style.css`:
```vue
<div class="card">
  <button class="btn btn-primary">Primary</button>
  <button class="btn btn-secondary">Secondary</button>
  <span class="badge badge-success">Success</span>
  <span class="badge badge-danger">Error</span>
</div>
```

### Fetching Data

Use `apiClient` from `src/api/client.js`:

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '@/api/client'

const data = ref(null)

onMounted(async () => {
  try {
    const response = await apiClient.get('/fields')
    data.value = response.data
  } catch (error) {
    console.error('API error:', error)
  }
})
</script>
```

## Performance Optimizations

- ✅ Vite tree-shaking and code splitting
- ✅ Tailwind CSS purging (unused styles removed)
- ✅ Service worker precaching
- ✅ Lazy route loading (Vue Router)
- ✅ Image optimization in PWA manifest

## Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 15+
- ✅ iOS Safari 15+
- ✅ Android Chrome

## Backend API Integration

The frontend expects a REST API at `VITE_API_URL`:

**Endpoints used:**
- `GET /fields` — List all fields with current metrics
- `GET /fields/{id}` — Get field details
- `GET /fields/{id}/timeseries` — Get time-series data (Cassandra)
- `GET /fields/{id}/metrics` — Get aggregated metrics (Redis)
- `GET /alerts` — Get active alerts
- `POST /alerts/{id}/read` — Mark alert as read
- `GET /graph/events` — Get Neo4j events

See `src/api/client.js` for implementation details.

## Troubleshooting

**Port 5173 already in use?**
```bash
npm run dev -- --port 3000
```

**Tailwind styles not applying?**
- Ensure all template paths are in `tailwind.config.js`
- Clear node_modules: `rm -rf node_modules && npm install`
- Rebuild: `npm run build`

**Service worker not updating?**
- Clear browser cache (Dev Tools → Application → Cache Storage)
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

**API connection failing?**
- Check backend is running at `VITE_API_URL`
- Verify CORS headers in backend
- Check browser console for detailed error

## Next Steps

1. **Backend REST API** — Create FastAPI/Flask server with endpoints
2. **Pinia State Management** — Setup stores for fields, alerts, UI
3. **Chart.js Integration** — Real-time analytics charts
4. **Leaflet Maps** — Geospatial field visualization
5. **WebSocket Support** — Real-time push notifications
6. **Testing** — Vitest unit tests + Cypress E2E

## Deployment

### Vercel (Recommended for PWA)
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

### Docker
See `../Dockerfile` for containerized deployment

### Traditional Server
```bash
npm run build
# Upload dist/ to web server root
```

## Resources

- [Vue 3 Docs](https://vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Vite Docs](https://vitejs.dev/)
- [PWA Docs](https://web.dev/progressive-web-apps/)
- [Web Dev Best Practices](https://web.dev/performance/)

## License

Part of the NoSQL Pasture Management project.

## Final Summary

For a concise final-summary of the frontend (features, file locations, run steps, backend integration points, deployment options, and recommended next steps), see `frontend/FINAL_SUMMARY.md` in the repository.

