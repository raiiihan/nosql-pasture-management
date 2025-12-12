<template>
  <div class="space-y-6">
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-emerald-500 to-teal-600 rounded-lg p-8 text-white">
      <h2 class="text-4xl font-bold mb-2">Farm Overview</h2>
      <p class="text-emerald-100">Monitor all your fields in real-time with live metrics and alerts</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="card">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm">Total Fields</p>
            <p class="text-3xl font-bold text-emerald-600 mt-2">{{ stats.totalFields }}</p>
          </div>
          <span class="text-4xl">🌾</span>
        </div>
      </div>

      <div class="card">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm">Avg Forage Quality</p>
            <p class="text-3xl font-bold text-blue-600 mt-2">{{ stats.avgQuality }}%</p>
          </div>
          <span class="text-4xl">📊</span>
        </div>
      </div>

      <div class="card">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm">Active Alerts</p>
            <p class="text-3xl font-bold text-red-600 mt-2">{{ stats.alerts }}</p>
          </div>
          <span class="text-4xl">⚠️</span>
        </div>
      </div>

      <div class="card">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm">Sensor Health</p>
            <p class="text-3xl font-bold text-green-600 mt-2">{{ stats.sensorHealth }}%</p>
          </div>
          <span class="text-4xl">✅</span>
        </div>
      </div>
    </div>

    <!-- Map and Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Map -->
      <div class="lg:col-span-2 card p-0 overflow-hidden">
        <div class="h-96 bg-gray-200 dark:bg-gray-700 flex items-center justify-center relative" id="map">
          <div class="text-center">
            <p class="text-gray-500 dark:text-gray-400 text-lg mb-2">🗺️ Geospatial Map</p>
            <p class="text-gray-400 text-sm">Field boundaries and soil conditions</p>
            <p class="text-gray-400 text-xs mt-4">(Connect to MongoDB for live field data)</p>
          </div>
        </div>
      </div>

      <!-- Recent Alerts -->
      <div class="space-y-4">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white">Recent Alerts</h3>
        <div class="space-y-2 max-h-96 overflow-y-auto">
          <div v-if="recentAlerts.length === 0" class="text-gray-500 dark:text-gray-400 text-sm text-center py-8">
            No active alerts
          </div>
          <div v-for="alert in recentAlerts" :key="alert.id" class="card p-3">
            <div class="flex items-start gap-3">
              <span class="text-2xl">{{ alert.icon }}</span>
              <div class="flex-1">
                <p class="font-semibold text-gray-900 dark:text-white text-sm">{{ alert.title }}</p>
                <p class="text-gray-600 dark:text-gray-400 text-xs">{{ alert.message }}</p>
                <p class="text-gray-400 text-xs mt-1">{{ alert.time }}</p>
              </div>
              <span :class="`badge ${alert.severity}`">{{ alert.severity }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Field Performance -->
    <div class="card">
      <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Field Performance</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-700">
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Field</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Forage Quality</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Soil Moisture</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Grass Height</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="field in fieldPerformance" :key="field.id" class="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <td class="py-3 px-4 font-medium text-gray-900 dark:text-white">{{ field.name }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="w-20 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div class="bg-emerald-500 h-2 rounded-full" :style="{ width: field.quality + '%' }"></div>
                  </div>
                  <span class="text-sm text-gray-600 dark:text-gray-400">{{ field.quality }}%</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-600 dark:text-gray-400">{{ field.moisture }}%</td>
              <td class="py-3 px-4 text-gray-600 dark:text-gray-400">{{ field.height }} cm</td>
              <td class="py-3 px-4">
                <span :class="`badge badge-${field.statusColor}`">{{ field.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiClient } from '@/api/client'

const stats = ref({
  totalFields: 0,
  avgQuality: 0,
  alerts: 0,
  sensorHealth: 96
})

const recentAlerts = ref([])
const fieldPerformance = ref([])
const loading = ref(true)
const error = ref(null)

const calculateStats = (fields) => {
  if (!fields || fields.length === 0) {
    return { totalFields: 0, avgQuality: 0, alerts: 0 }
  }
  
  const totalFields = fields.length
  const avgQuality = Math.round(
    fields.reduce((sum, f) => sum + (f.metrics?.ndvi || 0) * 100, 0) / totalFields
  )
  
  // Count alerts (fields with concerning metrics)
  const alerts = fields.filter(f => {
    const moisture = f.metrics?.soil_moisture || 0
    const ndvi = f.metrics?.ndvi || 0
    return moisture < 20 || ndvi < 0.4 // Low moisture or poor vegetation
  }).length
  
  return { totalFields, avgQuality, alerts }
}

const formatFieldPerformance = (fields) => {
  return fields.map((f, idx) => ({
    id: idx + 1,
    name: f.field_name || `Field ${idx + 1}`,
    quality: Math.round((f.metrics?.ndvi || 0) * 100),
    moisture: Math.round(f.metrics?.soil_moisture || 0),
    height: Math.round((f.metrics?.grass_height || 0) * 100) / 100,
    status: determineStatus(f.metrics),
    statusColor: determineStatusColor(f.metrics)
  }))
}

const determineStatus = (metrics) => {
  if (!metrics) return 'Unknown'
  const { ndvi = 0, soil_moisture = 0 } = metrics
  if (ndvi >= 0.5 && soil_moisture >= 30) return 'Excellent'
  if (ndvi >= 0.4 && soil_moisture >= 20) return 'Good'
  if (ndvi >= 0.3 && soil_moisture >= 15) return 'Fair'
  return 'Poor'
}

const determineStatusColor = (metrics) => {
  const status = determineStatus(metrics)
  const colorMap = {
    'Excellent': 'success',
    'Good': 'success',
    'Fair': 'warning',
    'Poor': 'danger',
    'Unknown': 'secondary'
  }
  return colorMap[status] || 'secondary'
}

const formatAlerts = (fields) => {
  const alerts = []
  fields.forEach((f, idx) => {
    const { soil_moisture = 0, air_temp = 0, ndvi = 0 } = f.metrics || {}
    
    if (soil_moisture < 20) {
      alerts.push({
        id: alerts.length + 1,
        icon: '💧',
        title: 'Low Soil Moisture',
        message: `${f.field_name || `Field ${idx + 1}`}: ${soil_moisture.toFixed(1)}% (below 20% threshold)`,
        time: 'just now',
        severity: 'badge-danger'
      })
    }
    if (air_temp > 28) {
      alerts.push({
        id: alerts.length + 1,
        icon: '🌡️',
        title: 'High Temperature',
        message: `${f.field_name || `Field ${idx + 1}`}: ${air_temp.toFixed(1)}°C (above 28°C)`,
        time: 'just now',
        severity: 'badge-warning'
      })
    }
    if (ndvi < 0.4) {
      alerts.push({
        id: alerts.length + 1,
        icon: '🌾',
        title: 'Low Vegetation Index',
        message: `${f.field_name || `Field ${idx + 1}`}: NDVI ${ndvi.toFixed(2)} (below 0.4)`,
        time: 'just now',
        severity: 'badge-warning'
      })
    }
  })
  return alerts.slice(0, 5) // Show top 5 alerts
}

const loadDashboardData = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await apiClient.get('/api/fields')
    const fields = Array.isArray(response) ? response : response.data || []
    
    if (fields.length > 0) {
      const newStats = calculateStats(fields)
      stats.value = { ...stats.value, ...newStats }
      fieldPerformance.value = formatFieldPerformance(fields)
      recentAlerts.value = formatAlerts(fields)
    }
  } catch (err) {
    console.error('Error loading dashboard data:', err)
    error.value = 'Failed to load dashboard data. Using sample data.'
    // Keep sample data visible as fallback
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboardData()
  // Refresh every 30 seconds
  const interval = setInterval(loadDashboardData, 30000)
  return () => clearInterval(interval)
})
</script>
