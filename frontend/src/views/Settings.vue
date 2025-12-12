<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Settings</h2>
      <p class="text-gray-600 dark:text-gray-400">Configure preferences and system settings</p>
    </div>

    <!-- Settings Navigation -->
    <div class="card">
      <div class="flex gap-2 flex-wrap">
        <button
          v-for="tab in ['general', 'notifications', 'thresholds', 'integration']"
          :key="tab"
          @click="activeTab = tab"
          :class="activeTab === tab ? 'btn btn-primary' : 'btn btn-secondary'"
        >
          {{ capitalizeFirst(tab) }}
        </button>
      </div>
    </div>

    <!-- General Settings -->
    <div v-if="activeTab === 'general'" class="space-y-6">
      <div class="card">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-6">General Settings</h3>
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Farm Name</label>
            <input v-model="settings.farmName" type="text" class="input-field" />
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Display name for your farm</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Location</label>
            <input v-model="settings.location" type="text" placeholder="City, State" class="input-field" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Total Area (hectares)</label>
              <input v-model="settings.totalArea" type="number" class="input-field" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Timezone</label>
              <select v-model="settings.timezone" class="input-field">
                <option>UTC</option>
                <option>EST</option>
                <option>CST</option>
                <option>MST</option>
                <option>PST</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Preferred Units</label>
            <div class="space-y-2">
              <label class="flex items-center gap-2">
                <input v-model="settings.units" type="radio" value="metric" />
                <span class="text-gray-700 dark:text-gray-300">Metric (°C, mm, kg)</span>
              </label>
              <label class="flex items-center gap-2">
                <input v-model="settings.units" type="radio" value="imperial" />
                <span class="text-gray-700 dark:text-gray-300">Imperial (°F, in, lb)</span>
              </label>
            </div>
          </div>

          <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
            <button class="btn btn-primary">💾 Save Changes</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Notification Settings -->
    <div v-if="activeTab === 'notifications'" class="space-y-6">
      <div class="card">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-6">Notification Preferences</h3>
        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div>
              <p class="font-semibold text-gray-900 dark:text-white">Email Notifications</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">Receive alerts via email</p>
            </div>
            <input v-model="notifications.email" type="checkbox" class="w-4 h-4" />
          </div>

          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div>
              <p class="font-semibold text-gray-900 dark:text-white">Push Notifications</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">Browser push alerts</p>
            </div>
            <input v-model="notifications.push" type="checkbox" class="w-4 h-4" />
          </div>

          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div>
              <p class="font-semibold text-gray-900 dark:text-white">Critical Alerts</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">Always notify for critical events</p>
            </div>
            <input v-model="notifications.critical" type="checkbox" class="w-4 h-4" />
          </div>

          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div>
              <p class="font-semibold text-gray-900 dark:text-white">Daily Summary</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">Receive daily email digest</p>
            </div>
            <input v-model="notifications.dailySummary" type="checkbox" class="w-4 h-4" />
          </div>

          <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
            <button class="btn btn-primary">💾 Save Preferences</button>
          </div>
        </div>
      </div>

      <div class="card">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Quiet Hours</h3>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Start Time</label>
            <input v-model="notifications.quietStart" type="time" class="input-field" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">End Time</label>
            <input v-model="notifications.quietEnd" type="time" class="input-field" />
          </div>
        </div>
      </div>
    </div>

    <!-- Alert Thresholds -->
    <div v-if="activeTab === 'thresholds'" class="space-y-6">
      <div class="card">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-6">Alert Thresholds</h3>
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Soil Moisture (%)</label>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Warning Below</p>
                <input v-model="thresholds.moistureWarning" type="number" class="input-field" />
              </div>
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Critical Below</p>
                <input v-model="thresholds.moistureCritical" type="number" class="input-field" />
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Temperature (°C)</label>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Warning Above</p>
                <input v-model="thresholds.tempWarning" type="number" class="input-field" />
              </div>
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Critical Above</p>
                <input v-model="thresholds.tempCritical" type="number" class="input-field" />
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">NDVI Index</label>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Warning Below</p>
                <input v-model="thresholds.ndviWarning" type="number" step="0.01" class="input-field" />
              </div>
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Critical Below</p>
                <input v-model="thresholds.ndviCritical" type="number" step="0.01" class="input-field" />
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Grass Height (cm)</label>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Ready for Harvest</p>
                <input v-model="thresholds.heightHarvest" type="number" class="input-field" />
              </div>
              <div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Minimum Growth</p>
                <input v-model="thresholds.heightMinimum" type="number" class="input-field" />
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
            <button class="btn btn-primary">💾 Save Thresholds</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Integration Settings -->
    <div v-if="activeTab === 'integration'" class="space-y-6">
      <div class="card">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-6">Connected Services</h3>
        <div class="space-y-4">
          <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg flex justify-between items-center">
            <div>
              <p class="font-semibold text-gray-900 dark:text-white">MongoDB</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">Field metadata storage</p>
            </div>
            <span class="text-green-600 font-bold">✓ Connected</span>
          </div>

          <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg flex justify-between items-center">
            <div>
              <p class="font-semibold text-gray-900 dark:text-white">Cassandra</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">Time-series sensor data</p>
            </div>
            <span class="text-green-600 font-bold">✓ Connected</span>
          </div>

          <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg flex justify-between items-center">
            <div>
              <p class="font-semibold text-gray-900 dark:text-white">Redis</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">Real-time metrics cache</p>
            </div>
            <span class="text-green-600 font-bold">✓ Connected</span>
          </div>

          <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg flex justify-between items-center">
            <div>
              <p class="font-semibold text-gray-900 dark:text-white">Neo4j</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">Event relationships</p>
            </div>
            <span class="text-green-600 font-bold">✓ Connected</span>
          </div>
        </div>
      </div>

      <div class="card">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-6">API Configuration</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">API Endpoint</label>
            <input v-model="settings.apiEndpoint" type="text" class="input-field" placeholder="http://localhost:8000" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">API Key</label>
            <input v-model="settings.apiKey" type="password" class="input-field" />
          </div>
          <button class="btn btn-secondary">Test Connection</button>
        </div>
      </div>
    </div>

    <!-- Danger Zone -->
    <div class="card border-2 border-red-200 dark:border-red-800">
      <h3 class="text-lg font-bold text-red-600 mb-4">Danger Zone</h3>
      <div class="space-y-3">
        <button class="btn btn-secondary w-full justify-start">📥 Export All Data</button>
        <button class="btn btn-secondary w-full justify-start">🗑️ Clear Cache</button>
        <button class="btn btn-secondary w-full justify-start">↺ Reset Settings to Default</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('general')

const settings = ref({
  farmName: 'Green Valley Farm',
  location: 'Vermont, USA',
  totalArea: 125.5,
  timezone: 'EST',
  units: 'metric',
  apiEndpoint: 'http://localhost:8000',
  apiKey: ''
})

const notifications = ref({
  email: true,
  push: true,
  critical: true,
  dailySummary: false,
  quietStart: '22:00',
  quietEnd: '08:00'
})

const thresholds = ref({
  moistureWarning: 35,
  moistureCritical: 20,
  tempWarning: 26,
  tempCritical: 30,
  ndviWarning: 0.45,
  ndviCritical: 0.35,
  heightHarvest: 12,
  heightMinimum: 5
})

const capitalizeFirst = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<style scoped>
.input-field {
  @apply w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500;
}
</style>
