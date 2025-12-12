<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow">
      <div class="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-emerald-600">🌾 Pasture Manager</h1>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">Real-time NoSQL Analytics</p>
        </div>
        <div class="flex items-center gap-4">
          <button @click="toggleDarkMode" class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
            <span v-if="isDark">☀️</span>
            <span v-else>🌙</span>
          </button>
          <nav class="hidden md:flex gap-4">
            <router-link to="/" class="nav-link">Dashboard</router-link>
            <router-link to="/fields" class="nav-link">Fields</router-link>
            <router-link to="/analytics" class="nav-link">Analytics</router-link>
            <router-link to="/alerts" class="nav-link">Alerts</router-link>
          </nav>
          <button class="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
            ☰
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-8">
      <router-view />
    </main>

    <!-- Mobile Navigation -->
    <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex justify-around">
      <router-link to="/" class="nav-link-mobile">📊</router-link>
      <router-link to="/fields" class="nav-link-mobile">🗺️</router-link>
      <router-link to="/analytics" class="nav-link-mobile">📈</router-link>
      <router-link to="/alerts" class="nav-link-mobile">🔔</router-link>
      <router-link to="/settings" class="nav-link-mobile">⚙️</router-link>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)

const toggleDarkMode = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.theme = 'dark'
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.theme = 'light'
  }
}

onMounted(() => {
  if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>

<style scoped>
.nav-link {
  @apply px-3 py-2 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors font-medium;
}

.nav-link-mobile {
  @apply flex-1 py-4 text-center text-2xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors;
}
</style>
