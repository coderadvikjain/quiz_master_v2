<template>
  <div v-if="isReady" class="d-flex flex-column min-vh-100">
    <AdminNavbar
      v-if="showAdminNavbar"
      @toggle-theme="toggleTheme"
      @logout="logout"
      @search="updateSearchQuery"
    />

    <UserNavbar
      v-else-if="showUserNavbar"
      @toggle-theme="toggleTheme"
      @logout="logout"
      @search="updateSearchQuery"
    />

    <main class="flex-grow-1">
      <router-view />
    </main>

    <MainFooter v-if="showFooter" />
  </div>
</template>

<script setup>
import { computed, ref, provide, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import AdminNavbar from '@/components/AdminNavbar.vue'
import UserNavbar from '@/components/UserNavbar.vue'
import MainFooter from '@/components/MainFooter.vue'

const route = useRoute()
const userRole = ref(localStorage.getItem('user_role'))
const isReady = ref(false)
const searchQuery = ref('')

provide('searchQuery', searchQuery)
const updateSearchQuery = (query) => (searchQuery.value = query)

const isDark = ref(localStorage.getItem('theme') === 'dark')
document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')

const toggleTheme = () => {
  isDark.value = !isDark.value
  const theme = isDark.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

const logout = () => {
  localStorage.clear()
  window.location.href = '/SignIn'
}

watch(() => route.path,() => {
    userRole.value = localStorage.getItem('user_role')},
  { immediate: true }
)

const hideLayout = computed(() => route.meta.hideLayout === true)

const showAdminNavbar = computed(() =>
  userRole.value === 'admin' && !hideLayout.value
)

const showUserNavbar = computed(() =>
  userRole.value === 'user' && !hideLayout.value
)

const showFooter = computed(() => !hideLayout.value)


onMounted(() => {
  userRole.value = localStorage.getItem('user_role')
  isReady.value = true
})
</script>