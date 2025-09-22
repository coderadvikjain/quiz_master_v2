<template>
  <div class="container-fluid min-vh-100 d-flex p-0">
    <div class="left-section d-none d-md-flex login-img-section align-items-center justify-content-center">
      <div class="text-center text-white px-5">
        <h1 class="display-4 fw-bold">StudiQ</h1>
        <p class="lead">Challenge your knowledge. Quiz. Compete. Learn.</p>
      </div>
    </div>
    <div class="right-section d-flex align-items-center justify-content-center">
      <div class="p-4 w-100" style="max-width: 420px; border-radius: 1rem;">
        <div class="text-center mb-4">
          <img src="@/assets/logo.png" class="mb-3" style="width: 60px;" alt="StudiQ Logo" />
          <h2 class="fw-bold">Sign In</h2>
        </div>
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control rounded-pill px-3 py-2" placeholder="jane.doe@StudiQ.com" required />
          </div>
          <div class="mb-4">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control rounded-pill px-3 py-2" placeholder="Jane@1234" required />
          </div>
          <button type="submit" class="btn btn-dark w-100 rounded-pill py-2 fw-semibold" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Sign In
          </button>
        </form>
        <div class="text-center mt-3">
          <small class="text-muted">Don’t have an account?</small>
          <a href="/SignUp" class="text-primary text-decoration-none fw-semibold ms-1">Sign Up→</a>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { login, setAuthToken } from '@/services/api';

export default {
  name: 'LoginPage',
  setup() {
    const email = ref('');
    const password = ref('');
    const loading = ref(false);
    const router = useRouter();

    onMounted(() => {
      document.title = 'StudiQ | Sign In';
    });

    const handleLogin = async () => {
      loading.value = true;
      try {
        const res = await login({ email: email.value, password: password.value });
        const token = res?.access_token;
        const role = res?.role;

        if (!token) throw new Error('Token not received');
        localStorage.setItem('access_token', token);
        localStorage.setItem('user_role', role);
        setAuthToken(token);
        
        const urlParams = new URLSearchParams(window.location.search);
        const redirect = urlParams.get('redirect');

        if (redirect && role !== 'admin') {
          router.push(redirect);
        } else {
          router.push(role === 'admin' ? '/admin/dashboard' : '/dashboard');
        }
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      } finally {
        loading.value = false;
      }
    };

    return { email, password, loading, handleLogin };
  },
};
</script>

<style scoped>
.left-section {
  flex: 1.3;
  background: url('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?q=80&w=2128&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D') no-repeat center center/cover;
  position: relative;
  padding: 60px 40px;
}
.left-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  z-index: 1;
}
.left-section > div {
  z-index: 3;
  animation: fadeIn 1.2s ease-in-out both;
}
.right-section {
  flex: 1;
  padding: 20px;
}
.left-section h1 {
  font-size: 3.5rem;
  font-weight: 800;
  letter-spacing: 2px;
  margin-bottom: 1rem;
}
.left-section p {
  font-size: 1.25rem;
  font-weight: 500;
  color: #e0e0e0;
}
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>