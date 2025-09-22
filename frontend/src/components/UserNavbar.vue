<template>
  <nav
    :class="['navbar navbar-expand-lg navbar-light shadow-sm px-4 py-2 mx-auto align-items-center main-navbar', { 'search-open': showSearch }]"
    :style="navbarStyle">
    <router-link to="/dashboard" class="navbar-brand d-flex align-items-center">
      <img src="@/assets/logo.png" alt="Logo" width="40" height="40" class="rounded-circle me-2" />
    </router-link>
    <transition name="slide-fade">
      <input
        v-if="showSearch"
        v-model="searchQuery"
        @input="emitSearch"
        type="search"
        placeholder="Type to search..."
        class="form-control d-block d-lg-none mt-2"
        style="border-radius: 30px; width: 240px;"
      />
    </transition>
    <button
      @click="toggleSearch"
      class="border-0 bg-transparent p-2 ms-auto d-block d-lg-none"
      :title="showSearch ? 'Close Search' : 'Search'">
      <i
        :class="showSearch ? 'bi bi-x-lg text-danger' : 'bi bi-search'"
        style="font-size: 1rem;"
      ></i>
    </button>
    <div class="d-flex d-lg-none align-items-center ms-2">
      <button
        @click="toggleTheme"
        class="border-0 bg-transparent p-2"
        title="Toggle Theme">
        <i
          :class="['bi', isDark ? 'bi-sun-fill' : 'bi-moon-fill', isDark ? 'icon-sun' : 'icon-moon']"
          style="font-size: 1.2rem;"
        ></i>
      </button>
      <div class="d-flex d-lg-none dropdown position-relative ms-2">
        <button
          class="border-0 bg-transparent p-2"
          @click="toggleProfileDropdown"
          title="User Menu">
          <img 
            src="https://gifdb.com/images/high/bear-love-bouncing-mocha-with-flowers-n4m0fyne6h4e6y2x.gif" 
            alt="Profile" 
            class="rounded-circle border" 
            style="width: 1.9rem; height: 1.8rem; object-fit: cover;"
          />
        </button>
        <div v-if="showProfileDropdown" class="dropdown-menu-custom shadow">
          <p class="mb-1 text-nowrap">Logged in as <strong>{{ fullNameCapitalized }}</strong></p>
          <hr class="my-1" />
          <button class="dropdown-item" @click="showProfileModal = true">View Profile</button>
          <button class="dropdown-item text-danger" @click="logout">Logout</button>
        </div>
      </div>
      <button
        class="border-0 bg-transparent p-0 ms-2"
        type="button"
        @click="toggleNavbar"
        aria-label="Toggle navigation"
        :class="{ open: isOpen }">
        <svg width="30" height="30" viewBox="0 0 30 30" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <line class="line1" x1="5" y1="7" x2="25" y2="7" />
          <line class="line2" x1="5" y1="15" x2="25" y2="15" />
          <line class="line3" x1="5" y1="23" x2="25" y2="23" />
        </svg>
      </button>
    </div>
    <div
      :class="['collapse navbar-collapse', { show: isOpen }]"
      id="navbarContent"
      v-show="!showSearch">
      <ul class="navbar-nav mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link to="/dashboard" class="nav-link custom-link" @click="isOpen = false">Dashboard</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/grades" class="nav-link custom-link" @click="isOpen = false">Grades</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/insights" class="nav-link custom-link" @click="isOpen = false">Insights</router-link>
        </li>
      </ul>
      <div class="d-none d-lg-flex align-items-center ms-2">
        <transition name="slide-fade">
          <input
            v-if="showSearch"
            v-model="searchQuery"
            @input="emitSearch"
            type="search"
            placeholder="Type to search..."
            class="form-control ms-2"
            style="border-radius: 30px; max-width: 300px;"
          />
        </transition>
        <button
          @click="toggleSearch"
          class="border-0 bg-transparent p-2"
          :title="showSearch ? 'Close Search' : 'Search'">
          <i
            :class="showSearch ? 'bi bi-x-lg text-danger' : 'bi bi-search'"
            style="font-size: 1rem;"
          ></i>
        </button>
      </div>
      <button
        @click="toggleTheme"
        class="border-0 bg-transparent px-2 py-2 fw-semibold hover-shadow ms-2 d-none d-lg-flex align-items-center"
        title="Toggle Theme">
        <i
          :class="['bi', isDark ? 'bi-sun-fill' : 'bi-moon-fill', isDark ? 'icon-sun' : 'icon-moon']"
          style="font-size: 1.2rem;">
        </i>
      </button>
      <div class="d-none d-lg-flex dropdown position-relative ms-2">
        <button
          class="border-0 bg-transparent p-2"
          @click="toggleProfileDropdown"
          title="User Menu">
          <img 
            src="https://gifdb.com/images/high/bear-love-bouncing-mocha-with-flowers-n4m0fyne6h4e6y2x.gif" 
            alt="Profile" 
            class="rounded-circle border" 
            style="width: 2.1rem; height: 2.1rem; object-fit: cover;"
          />
        </button>
        <div v-if="showProfileDropdown" class="dropdown-menu-custom shadow">
          <p class="mb-1 text-nowrap">Logged in as <strong>{{ fullNameCapitalized }}</strong></p>
          <hr class="my-1" />
          <button class="dropdown-item" @click="showProfileModal = true">View Profile</button>
          <button class="dropdown-item text-danger" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </nav>
  <ProfileModal
    v-if="showProfileModal"
    :user="user"
    :scores="scores"
    @close="showProfileModal = false"
  />
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getUserinfo, getUserScores } from '@/services/api.js'
import ProfileModal from '@/components/ProfileModal.vue'

export default {
  name: 'UserNavbar',
  emits: ['toggleTheme', 'logout', 'search'],
  components: { ProfileModal },
  setup(_, { emit }) {
    const isOpen = ref(false)
    const isDark = ref(false)
    const user = ref(null)
    const showSearch = ref(false)
    const showProfileDropdown = ref(false)
    const showProfileModal = ref(false)
    const searchQuery = ref('')
    const scores = ref([])
    const router = useRouter()
    const toggleNavbar = () => {
      isOpen.value = !isOpen.value
    }

    const toggleTheme = () => {
      isDark.value = !isDark.value
      const theme = isDark.value ? 'dark' : 'light'
      document.documentElement.setAttribute('data-theme', theme)
      localStorage.setItem('theme', theme)
    }

    const fullNameCapitalized = computed(() => {
      if (!user.value?.full_name) return ''
      return user.value.full_name
        .split(' ')
        .map(w => w.charAt(0).toUpperCase() + w.slice(1))
        .join(' ')
    })

    const fetchUser = async () => {
      try {
        const res = await getUserinfo()
        user.value = res

        const scoreRes = await getUserScores()
        scores.value = scoreRes.scores
        console.log('User scores fetched:', scores.value)
      } catch (err) {
        console.error('User info or score fetch error', err)
      }
    }

    const logout = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('user')
      user.value = null
      router.push('/SignIn')
    }

    const toggleProfileDropdown = () => {
      showProfileDropdown.value = !showProfileDropdown.value
    }

    const viewProfile = () => {
      showProfileDropdown.value = false
      router.push('/profile')
    }

    const toggleSearch = () => {
      showSearch.value = !showSearch.value
      if (!showSearch.value) {
        searchQuery.value = ''
        emit('search', '')
      }
    }

    const emitSearch = () => {
      emit('search', searchQuery.value)
    }

    onMounted(() => {
      const savedTheme = localStorage.getItem('theme') || 'light'
      isDark.value = savedTheme === 'dark'
      document.documentElement.setAttribute('data-theme', savedTheme)

      const userData = localStorage.getItem('user')
      if (userData) {
        try {
          user.value = JSON.parse(userData)
        } catch {
          console.error('Invalid user data in localStorage')
        }
      }
      fetchUser()
    })

    const navbarStyle = ref({})
    watch(showSearch, (val) => {
      navbarStyle.value = {
        maxWidth: val ? '800px' : '600px',
        position: 'sticky',
        top: '1rem',
        zIndex: '1030',
        backdropFilter: 'blur(52px)',
        borderRadius: '40px',
        transition: 'max-width 0.4s ease',
      }
    },
    { immediate: true })

    return {
      isOpen,
      isDark,
      user,
      scores,
      fullNameCapitalized,
      fetchUser,
      viewProfile,
      showProfileDropdown,
      toggleProfileDropdown,
      showProfileModal,
      showSearch,
      searchQuery,
      toggleNavbar,
      toggleTheme,
      logout,
      toggleSearch,
      emitSearch,
      navbarStyle,
    }
  },
}
</script>

<style scoped>
button {
  cursor: pointer;
  transition: transform 0.3s ease;
}
.line1,
.line2,
.line3 {
  transition: all 0.3s ease;
  stroke: #333;
}
.open .line1 {
  transform-origin: 50% 50%;
  transform: rotate(40deg) translate(5px, 5px);
}
.open .line2 {
  opacity: 0;
}
.open .line3 {
  transform-origin: 50% 50%;
  transform: rotate(-30deg) translate(5px, -5px);
}
.custom-link {
  position: relative;
  padding: 0.5rem 1rem;
  font-weight: 500;
  color: #212529 !important;
  transition: all 0.3s ease-in-out;
  border-radius: 50px;
}
.custom-link:hover {
  color: #6f42c1 !important;
  background-color: rgba(111, 66, 193, 0.08);
}
.icon-sun {
  color: #f1c40f !important;
}
.icon-moon {
  color: #6ab0f5 !important;
}
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
.dropdown-menu-custom {
  position: absolute;
  top: 100%;
  right: 0;
  min-width: 180px;
  background-color: white;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  z-index: 9999;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>