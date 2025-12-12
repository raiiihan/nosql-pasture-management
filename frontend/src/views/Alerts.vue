<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Alerts & Events</h2>
        <p class="text-gray-600 dark:text-gray-400">Real-time notifications and threshold events</p>
      </div>
      <div class="flex gap-2">
        <button @click="filterSeverity = ''" :class="filterSeverity === '' ? 'btn btn-primary' : 'btn btn-secondary'">
          All ({{ alerts.length }})
        </button>
        <button @click="filterSeverity = 'danger'" :class="filterSeverity === 'danger' ? 'btn btn-primary' : 'btn btn-secondary'">
          Critical ({{ criticalCount }})
        </button>
        <button @click="filterSeverity = 'warning'" :class="filterSeverity === 'warning' ? 'btn btn-primary' : 'btn btn-secondary'">
          Warnings ({{ warningCount }})
        </button>
      </div>
    </div>

    <!-- Alert Summary -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card border-l-4 border-red-500">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm">Critical Alerts</p>
            <p class="text-3xl font-bold text-red-600 mt-2">{{ criticalCount }}</p>
          </div>
          <span class="text-4xl">🚨</span>
        </div>
      </div>

      <div class="card border-l-4 border-yellow-500">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm">Warnings</p>
            <p class="text-3xl font-bold text-yellow-600 mt-2">{{ warningCount }}</p>
          </div>
          <span class="text-4xl">⚠️</span>
        </div>
      </div>

      <div class="card border-l-4 border-green-500">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-600 dark:text-gray-400 text-sm">Resolved</p>
            <p class="text-3xl font-bold text-green-600 mt-2">{{ resolvedCount }}</p>
          </div>
          <span class="text-4xl">✅</span>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="card flex gap-2 flex-wrap">
      <button class="btn btn-secondary">🔔 Enable Notifications</button>
      <button class="btn btn-secondary">📧 Email on Critical</button>
      <button class="btn btn-secondary">📋 View Alert Rules</button>
      <button @click="markAllAsRead" class="btn btn-secondary">✓ Mark All Read</button>
    </div>

    <!-- Alerts List -->
    <div class="space-y-3">
      <div v-if="filteredAlerts.length === 0" class="card text-center py-12">
        <p class="text-gray-500 dark:text-gray-400 text-lg">✓ No alerts</p>
        <p class="text-gray-400 dark:text-gray-500 text-sm">All systems operating normally</p>
      </div>

      <div v-for="alert in filteredAlerts" :key="alert.id" :class="['card', 'border-l-4', `border-${getSeverityColor(alert.severity)}-500`, alert.read ? 'opacity-60' : '']">
        <div class="flex gap-4">
          <!-- Icon -->
          <div class="flex-shrink-0 text-3xl">{{ alert.icon }}</div>

          <!-- Content -->
          <div class="flex-1">
            <div class="flex items-start justify-between mb-2">
              <div>
                <h4 class="font-bold text-gray-900 dark:text-white">{{ alert.title }}</h4>
                <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">{{ alert.message }}</p>
              </div>
              <span :class="`badge badge-${alert.severity}`">{{ formatSeverity(alert.severity) }}</span>
            </div>

            <!-- Details -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3 py-3 border-t border-gray-200 dark:border-gray-700">
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400">Field</p>
                <p class="font-semibold text-gray-900 dark:text-white">{{ alert.field }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400">Metric</p>
                <p class="font-semibold text-gray-900 dark:text-white">{{ alert.metric }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400">Value</p>
                <p class="font-semibold text-gray-900 dark:text-white">{{ alert.value }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400">Time</p>
                <p class="font-semibold text-gray-900 dark:text-white">{{ alert.time }}</p>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-2 mt-3">
              <button v-if="!alert.read" @click="toggleRead(alert.id)" class="text-sm btn btn-secondary px-3 py-1">
                Mark as Read
              </button>
              <button class="text-sm btn btn-secondary px-3 py-1">View History</button>
              <button class="text-sm btn btn-secondary px-3 py-1">Send Reminder</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Event History -->
    <div class="card">
      <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Event History</h3>
      <div class="space-y-2">
        <div v-for="event in eventHistory" :key="event.id" class="py-3 px-4 bg-gray-50 dark:bg-gray-700 rounded flex justify-between items-center">
          <div>
            <p class="font-semibold text-gray-900 dark:text-white text-sm">{{ event.title }}</p>
            <p class="text-xs text-gray-600 dark:text-gray-400">{{ event.description }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ event.time }}</p>
            <span :class="`badge badge-${event.type}`">{{ event.status }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const filterSeverity = ref('')

const alerts = ref([
  {
    id: 1,
    icon: '🌡️',
    title: 'High Temperature Alert',
    message: 'Temperature exceeded safe threshold for forage growth',
    severity: 'danger',
    field: 'North Pasture',
    metric: 'Air Temperature',
    value: '28.5°C',
    time: '5 min ago',
    read: false
  },
  {
    id: 2,
    icon: '💧',
    title: 'Low Soil Moisture',
    message: 'Soil moisture below optimal range for grazing',
    severity: 'warning',
    field: 'East Pasture',
    metric: 'Soil Moisture',
    value: '28%',
    time: '12 min ago',
    read: false
  },
  {
    id: 3,
    icon: '📉',
    title: 'NDVI Drop Detected',
    message: 'Forage quality declining rapidly in South Pasture',
    severity: 'warning',
    field: 'South Pasture',
    metric: 'NDVI Index',
    value: '0.42',
    time: '28 min ago',
    read: false
  },
  {
    id: 4,
    icon: '✂️',
    title: 'Grass Ready for Harvest',
    message: 'Grass height optimal for cutting and hay production',
    severity: 'success',
    field: 'Center Plot',
    metric: 'Grass Height',
    value: '13.2 cm',
    time: '1 hour ago',
    read: true
  },
  {
    id: 5,
    icon: '🚨',
    title: 'Critical Threshold Breach',
    message: 'Soil moisture critical - immediate irrigation needed',
    severity: 'danger',
    field: 'East Pasture',
    metric: 'Soil Moisture',
    value: '15%',
    time: '2 hours ago',
    read: true
  }
])

const eventHistory = ref([
  {
    id: 1,
    title: 'Temperature Spike',
    description: 'Max temp 28.5°C recorded in North Pasture',
    time: 'Today 2:34 PM',
    type: 'danger',
    status: 'Resolved'
  },
  {
    id: 2,
    title: 'Irrigation Started',
    description: 'Manual irrigation deployed in East Pasture',
    time: 'Today 2:10 PM',
    type: 'success',
    status: 'Active'
  },
  {
    id: 3,
    title: 'Sensor Calibrated',
    description: 'Moisture sensors recalibrated in South Pasture',
    time: 'Today 1:45 PM',
    type: 'success',
    status: 'Complete'
  }
])

const filteredAlerts = computed(() => {
  if (!filterSeverity.value) return alerts.value
  return alerts.value.filter(a => a.severity === filterSeverity.value)
})

const criticalCount = computed(() => alerts.value.filter(a => a.severity === 'danger').length)
const warningCount = computed(() => alerts.value.filter(a => a.severity === 'warning').length)
const resolvedCount = computed(() => alerts.value.filter(a => a.severity === 'success').length)

const toggleRead = (id) => {
  const alert = alerts.value.find(a => a.id === id)
  if (alert) alert.read = !alert.read
}

const markAllAsRead = () => {
  alerts.value.forEach(a => a.read = true)
}

const getSeverityColor = (severity) => {
  const colors = {
    danger: 'red',
    warning: 'yellow',
    success: 'green'
  }
  return colors[severity] || 'gray'
}

const formatSeverity = (severity) => {
  const formats = {
    danger: 'Critical',
    warning: 'Warning',
    success: 'Info'
  }
  return formats[severity] || severity
}
</script>
