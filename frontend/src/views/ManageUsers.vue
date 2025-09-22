<template>
  <div class="py-5" style="max-width: 500px; margin: auto;">
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div class="rounded-4">
      <li
        v-for="user in filteredUsers"
        :key="user.id"
        class="user-item list-group-item d-flex justify-content-between align-items-center px-4 py-3 mb-1">
        <div>
          <div class="fw-semibold fs-5 text-dark">{{ capitalizeWords(user.full_name) }}</div>
          <div class="text-muted small">{{ user.email }}</div>
        </div>
        <div class="d-flex gap-2">
          <button
            @click="openModal(user)"
            class="btn btn-outline-info rounded-circle p-2 d-flex align-items-center justify-content-center"
            title="View Details"
            style="width: 38px; height: 38px;">
            <i class="bi bi-eye fs-5"></i>
          </button>
        </div>
      </li>
      <li v-if="users.length === 0" class="text-center text-muted py-5 fs-5">
        No users found.
      </li>
    </div>
  </div>
  <UserModal v-if="showModal" :user="selectedUser" @close="closeModal" />
</template>

<script>
import { inject, computed, ref, onMounted } from 'vue'
import { getUsers } from '@/services/api.js'
import UserModal from '@/components/UserModal.vue'

export default {
  name: 'ManageUsers',
  components: { UserModal },
  setup() {
    const users = ref([])
    const loading = ref(true)
    const showModal = ref(false)
    const selectedUser = ref(null)
    const searchQuery = inject('searchQuery', ref(''))

    onMounted(() => {
      document.title = 'StudiQ | Accounts';
    });

    const fetchUsers = async () => {
      try {
        loading.value = true
        const response = await getUsers()
        users.value = response.users
      } catch (error) {
        console.error('Failed to fetch users:', error)
      } finally {
        loading.value = false
      }
    }

    const filteredUsers = computed(() => {
      const rawQuery = searchQuery?.value;
      const query = typeof rawQuery === 'string' ? rawQuery.toLowerCase() : '';

      return users.value.filter(user =>
        user.full_name.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query)
      )
    })

    const openModal = (user) => {
      selectedUser.value = user
      showModal.value = true
    }

    const closeModal = () => {
      showModal.value = false
      selectedUser.value = null
    }
    
    function capitalizeWords(text) {
      return text.replace(/\b\w/g, char => char.toUpperCase());
    }

    onMounted(fetchUsers)

    return {
      users,
      loading,
      showModal,
      selectedUser,
      filteredUsers,
      capitalizeWords,
      openModal,
      closeModal,
    }
  },
}
</script>

<style scoped>
.user-item {
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  border-radius: 0.5rem;
  margin: 0.25rem 1rem;
  background-color:rgb(244, 244, 244);
  border-color:rgb(244, 244, 244);
}
.user-item:hover {
  background-color: #e7f1ff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
}
</style>