<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Fields</h2>
        <p class="text-gray-600 dark:text-gray-400">Manage and monitor all your fields</p>
      </div>
      <div class="flex gap-2">
        <button @click="toggleView" class="btn btn-secondary">
          {{ viewMode === 'grid' ? '📋' : '🔲' }} {{ viewMode === 'grid' ? 'List' : 'Grid' }}
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="card">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Search</label>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search fields..."
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Quality Filter</label>
          <select
            v-model="qualityFilter"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="">All Qualities</option>
            <option value="excellent">Excellent (80%+)</option>
            <option value="good">Good (60-79%)</option>
            <option value="fair">Fair (<60%)</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
          <select
            v-model="statusFilter"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="">All Status</option>
            <option value="excellent">Excellent</option>
            <option value="good">Good</option>
            <option value="fair">Fair</option>
            <option value="alert">Alert</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Grid View -->
    <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="field in filteredFields" :key="field.id" class="card hover:shadow-lg transition-shadow cursor-pointer" @click="selectedField = field">
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ field.name }}</h3>
          <span :class="`badge badge-${field.statusColor}`">{{ field.status }}</span>
        </div>

        <div class="space-y-3 mb-4">
          <div>
            <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Forage Quality</p>
            <div class="flex items-center gap-2">
              <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div class="bg-emerald-500 h-2 rounded-full" :style="{ width: field.quality + '%' }"></div>
              </div>
              <span class="text-sm font-semibold text-gray-900 dark:text-white">{{ field.quality }}%</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div class="bg-gray-50 dark:bg-gray-700 p-2 rounded">
              <p class="text-xs text-gray-600 dark:text-gray-400">Soil Moisture</p>
              <p class="text-lg font-bold text-blue-600">{{ field.moisture }}%</p>
            </div>
            <div class="bg-gray-50 dark:bg-gray-700 p-2 rounded">
              <p class="text-xs text-gray-600 dark:text-gray-400">Grass Height</p>
              <p class="text-lg font-bold text-green-600">{{ field.height }}cm</p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div class="bg-gray-50 dark:bg-gray-700 p-2 rounded">
              <p class="text-xs text-gray-600 dark:text-gray-400">Area</p>
              <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ field.area }} ha</p>
            </div>
            <div class="bg-gray-50 dark:bg-gray-700 p-2 rounded">
              <p class="text-xs text-gray-600 dark:text-gray-400">Last Updated</p>
              <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ field.lastUpdated }}</p>
            </div>
          </div>
        </div>

        <button class="btn btn-primary w-full">View Details →</button>
      </div>
    </div>

    <!-- List View -->
    <div v-else class="card">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-700">
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Field Name</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Quality</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Moisture</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Height</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Area</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Status</th>
              <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="field in filteredFields" :key="field.id" class="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <td class="py-3 px-4 font-medium text-gray-900 dark:text-white">{{ field.name }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div class="bg-emerald-500 h-2 rounded-full" :style="{ width: field.quality + '%' }"></div>
                  </div>
                  <span class="text-sm font-semibold">{{ field.quality }}%</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-600 dark:text-gray-400">{{ field.moisture }}%</td>
              <td class="py-3 px-4 text-gray-600 dark:text-gray-400">{{ field.height }} cm</td>
              <td class="py-3 px-4 text-gray-600 dark:text-gray-400">{{ field.area }} ha</td>
              <td class="py-3 px-4">
                <span :class="`badge badge-${field.statusColor}`">{{ field.status }}</span>
              </td>
              <td class="py-3 px-4">
                <button class="text-emerald-600 dark:text-emerald-400 hover:underline">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Field Detail Modal (simplified) -->
    <div v-if="selectedField" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full max-h-96 overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ selectedField.name }}</h3>
            <button @click="selectedField = null" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">✕</button>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Forage Quality</p>
              <p class="text-2xl font-bold text-emerald-600">{{ selectedField.quality }}%</p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Soil Moisture</p>
              <p class="text-2xl font-bold text-blue-600">{{ selectedField.moisture }}%</p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Grass Height</p>
              <p class="text-2xl font-bold text-green-600">{{ selectedField.height }} cm</p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Temperature</p>
              <p class="text-2xl font-bold text-orange-600">{{ selectedField.temp }}°C</p>
            </div>
          </div>
          <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <button @click="selectedField = null" class="btn btn-secondary">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiClient } from '@/api/client'

const viewMode = ref('grid')
const searchQuery = ref('')
const qualityFilter = ref('')
const statusFilter = ref('')
const selectedField = ref(null)
const loading = ref(false)

const fields = ref([])

const formatFieldData = (apiField, index) => {
  const metrics = apiField.metrics || {}
  const quality = Math.round((metrics.ndvi || 0) * 100)
  const moisture = Math.round(metrics.soil_moisture || 0)
  const height = Math.round((metrics.grass_height || 0) * 100) / 100
  const temp = Math.round(metrics.air_temp || 0)
  
  let status = 'Unknown'
  let statusColor = 'secondary'
  if (quality >= 80) {
    status = 'Excellent'
    statusColor = 'success'
  } else if (quality >= 60) {
    status = 'Good'
    statusColor = 'success'
  } else if (quality >= 40) {
    status = 'Fair'
    statusColor = 'warning'
  } else {
    status = 'Alert'
    statusColor = 'danger'
  }
  
  return {
    id: index + 1,
    field_id: apiField.field_id,
    name: apiField.field_name || `Field ${index + 1}`,
    quality,
    moisture,
    height,
    area: apiField.area || (2 + Math.random() * 2).toFixed(1),
    temp,
    status,
    statusColor,
    lastUpdated: 'just now'
  }
}

const loadFields = async () => {
  try {
    loading.value = true
    const response = await apiClient.get('/api/fields')
    const apiFields = Array.isArray(response) ? response : response.data || []
    
    if (apiFields.length > 0) {
      fields.value = apiFields.map(formatFieldData)
    }
  } catch (error) {
    console.error('Error loading fields:', error)
  } finally {
    loading.value = false
  }
}

const filteredFields = computed(() => {
  return fields.value.filter(field => {
    const matchesSearch = field.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesQuality = !qualityFilter.value || 
      (qualityFilter.value === 'excellent' && field.quality >= 80) ||
      (qualityFilter.value === 'good' && field.quality >= 60 && field.quality < 80) ||
      (qualityFilter.value === 'fair' && field.quality < 60)
    const matchesStatus = !statusFilter.value || field.status.toLowerCase() === statusFilter.value.toLowerCase()
    
    return matchesSearch && matchesQuality && matchesStatus
  })
})

const toggleView = () => {
  viewMode.value = viewMode.value === 'grid' ? 'list' : 'grid'
}

onMounted(() => {
  loadFields()
})
</script>
