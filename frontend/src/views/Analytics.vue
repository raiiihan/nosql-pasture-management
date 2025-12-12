<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Analytics</h2>
      <p class="text-gray-600 dark:text-gray-400">Time-series analysis and trends</p>
    </div>

    <!-- Controls -->
    <div class="card">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Select Field</label>
          <select
            v-model="selectedFieldId"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="1">North Pasture</option>
            <option value="2">East Pasture</option>
            <option value="3">West Pasture</option>
            <option value="4">South Pasture</option>
            <option value="5">Center Plot</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Time Period</label>
          <select
            v-model="timePeriod"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Metric</label>
          <select
            v-model="selectedMetric"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="ndvi">NDVI (Forage Quality)</option>
            <option value="moisture">Soil Moisture</option>
            <option value="temp">Air Temperature</option>
            <option value="height">Grass Height</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Charts Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Line Chart -->
      <div class="card">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">{{ getMetricLabel(selectedMetric) }} Trend</h3>
        <div class="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-700 rounded">
          <div class="text-center">
            <p class="text-gray-500 dark:text-gray-400 mb-2">📈 Chart Area</p>
            <p class="text-gray-400 text-sm">(Chart.js integration when API ready)</p>
          </div>
        </div>
      </div>

      <!-- Summary Stats -->
      <div class="space-y-4">
        <div class="card">
          <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Summary Statistics</h3>
          <div class="space-y-3">
            <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
              <span class="text-gray-600 dark:text-gray-400">Current Value</span>
              <span class="font-bold text-lg">{{ stats.current }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
              <span class="text-gray-600 dark:text-gray-400">Average</span>
              <span class="font-bold text-lg">{{ stats.average }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
              <span class="text-gray-600 dark:text-gray-400">Peak</span>
              <span class="font-bold text-lg text-emerald-600">{{ stats.peak }}</span>
            </div>
            <div class="flex justify-between items-center py-2">
              <span class="text-gray-600 dark:text-gray-400">Low</span>
              <span class="font-bold text-lg text-blue-600">{{ stats.low }}</span>
            </div>
          </div>
        </div>

        <!-- Trend Indicator -->
        <div class="card">
          <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-3">Trend</h3>
          <div class="flex items-center justify-between">
            <span class="text-3xl">📊</span>
            <div class="text-right">
              <p class="text-sm text-gray-600 dark:text-gray-400">Change</p>
              <p class="text-2xl font-bold text-emerald-600">+12.5%</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">vs. 7 days ago</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Comparative Analysis -->
    <div class="card">
      <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Field Comparison</h3>
      <div class="space-y-4">
        <div v-for="field in fieldComparison" :key="field.id" class="pb-4 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
          <div class="flex items-center justify-between mb-2">
            <span class="font-semibold text-gray-900 dark:text-white">{{ field.name }}</span>
            <span :class="`badge badge-${field.trendColor}`">{{ field.trend }}</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <div class="bg-emerald-500 h-3 rounded-full" :style="{ width: field.value + '%' }"></div>
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">{{ field.value }}% — {{ field.status }}</p>
        </div>
      </div>
    </div>

    <!-- Export Options -->
    <div class="card">
      <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Export Data</h3>
      <div class="flex gap-2">
        <button class="btn btn-secondary">📊 Download CSV</button>
        <button class="btn btn-secondary">📈 Generate Report</button>
        <button class="btn btn-secondary">📧 Email Report</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { apiClient } from '@/api/client'

const selectedFieldId = ref('1')
const timePeriod = ref('7d')
const selectedMetric = ref('ndvi')
const fields = ref([])
const timeseriesData = ref([])
const loading = ref(false)

const stats = ref({
  current: 0,
  average: 0,
  peak: 0,
  low: 0
})

const fieldComparison = ref([])

const getMetricLabel = (metric) => {
  const labels = {
    ndvi: 'Forage Quality (NDVI)',
    moisture: 'Soil Moisture',
    temp: 'Air Temperature',
    height: 'Grass Height'
  }
  return labels[metric] || metric
}

const getMetricValue = (row, metric) => {
  const metricMap = {
    ndvi: 'ndvi',
    moisture: 'soil_moisture',
    temp: 'air_temp',
    height: 'grass_height'
  }
  return row[metricMap[metric]] || 0
}

const updateStats = (data) => {
  if (!data || data.length === 0) return
  
  const values = data.map(row => getMetricValue(row, selectedMetric.value))
  const current = values[values.length - 1] || 0
  const average = Math.round((values.reduce((a, b) => a + b, 0) / values.length) * 10) / 10
  const peak = Math.max(...values)
  const low = Math.min(...values)
  
  stats.value = { current, average, peak, low }
}

const loadFieldsAndData = async () => {
  try {
    loading.value = true
    
    // Load fields list
    const fieldsResponse = await apiClient.get('/api/fields')
    const fieldsArray = Array.isArray(fieldsResponse) ? fieldsResponse : fieldsResponse.data || []
    fields.value = fieldsArray.map((f, idx) => ({
      id: String(idx + 1),
      name: f.field_name || `Field ${idx + 1}`
    }))
    
    if (fieldsArray.length > 0 && !selectedFieldId.value) {
      selectedFieldId.value = '1'
    }
    
    // Load comparison data
    fieldComparison.value = fieldsArray.map((f, idx) => ({
      id: idx + 1,
      name: f.field_name || `Field ${idx + 1}`,
      value: Math.round((f.metrics?.ndvi || 0) * 100),
      trend: f.metrics?.ndvi > 0.5 ? '↑ +5%' : f.metrics?.ndvi > 0.4 ? '→ 0%' : '↓ -2%',
      trendColor: f.metrics?.ndvi > 0.5 ? 'success' : f.metrics?.ndvi > 0.4 ? 'warning' : 'danger',
      status: f.metrics?.ndvi > 0.5 ? 'Improving' : f.metrics?.ndvi > 0.4 ? 'Stable' : 'Declining'
    }))
  } catch (error) {
    console.error('Error loading fields:', error)
  } finally {
    loading.value = false
  }
}

const loadTimeseriesData = async () => {
  if (!selectedFieldId.value || fields.value.length === 0) return
  
  try {
    loading.value = true
    const fieldIndex = parseInt(selectedFieldId.value) - 1
    const field = fields.value[fieldIndex]
    
    if (!field) return
    
    // Find original field by name to get field_id
    const fieldsResponse = await apiClient.get('/api/fields')
    const fieldsArray = Array.isArray(fieldsResponse) ? fieldsResponse : fieldsResponse.data || []
    const originalField = fieldsArray[fieldIndex]
    
    if (!originalField || !originalField.field_id) return
    
    const response = await apiClient.get(`/api/fields/${originalField.field_id}/timeseries`)
    const data = Array.isArray(response) ? response : response.data || []
    
    timeseriesData.value = data
    updateStats(data)
  } catch (error) {
    console.error('Error loading timeseries data:', error)
  } finally {
    loading.value = false
  }
}

watch([selectedFieldId, selectedMetric, timePeriod], () => {
  loadTimeseriesData()
})

onMounted(() => {
  loadFieldsAndData()
})
</script>
