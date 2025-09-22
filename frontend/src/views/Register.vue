<template>
  <div class="container-fluid min-vh-100 d-flex p-0">
    <div class="left-section d-none d-md-flex register-img-section align-items-center justify-content-center">
      <div class="text-center text-white px-5">
        <h1 class="display-4 fw-bold">StudiQ</h1>
        <p class="lead">Sign up to unlock a world of quizzes, knowledge, and fun.</p>
      </div>
    </div>
    <div class="right-section d-flex align-items-center justify-content-center">
      <div class="p-4 w-100" style="max-width: 460px; border-radius: 1rem;">
        <div class="text-center mb-4">
          <img src="@/assets/logo.png" class="mb-3" style="width: 60px;" alt="StudiQ Logo" />
          <h2 class="fw-bold">Sign Up</h2>
        </div>
        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control rounded-pill px-3 py-2" placeholder="jane.doe@StudiQ.com" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input v-model="fullName" type="text" class="form-control rounded-pill px-3 py-2" placeholder="Jane Doe" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" @blur="validatePassword" @input="validatePassword" type="password" class="form-control rounded-pill px-3 py-2" placeholder="Jane@1234" required />
            <div v-if="passwordError" class="text-danger mt-1 small">
              {{ passwordError }}
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Qualification</label>
            <select v-model="qualification" class="form-select rounded-pill px-3 py-2" required>
              <option disabled value="">Select your qualification</option>
              <option>12th</option>
              <option>B.Tech</option>
              <option>B.Sc</option>
              <option>B.Com</option>
              <option>M.Tech</option>
              <option>M.Sc</option>
              <option>MBA</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="form-label">Date of Birth</label>
            <input v-model="dob" type="date" class="form-control rounded-pill px-3 py-2" />
          </div>
          <button type="submit" class="btn btn-dark w-100 rounded-pill py-2 fw-semibold" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Sign Up
          </button>
          <div class="text-center mt-3">
            <small class="text-muted">Already have an account?</small>
            <a href="/SignIn" class="text-primary text-decoration-none fw-semibold ms-1">Sign In →</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { register } from '@/services/api';
import { useRouter } from 'vue-router';

export default {
  name: 'RegisterPage',
  setup() {
    const email = ref('');
    const fullName = ref('');
    const password = ref('');
    const qualification = ref('');
    const dob = ref('');
    const passwordError = ref('');
    const loading = ref(false);
    const router = useRouter();

    onMounted(() => {
      document.title = 'StudiQ | Sign Up';
    });

    const validatePassword = () => {
      const value = password.value;
      if (value.length < 8) {
        passwordError.value = 'Password must be at least 8 characters long.';
      } else if (!/^[A-Z]/.test(value)) {
        passwordError.value = 'Password must start with a capital letter.';
      } else if (!/[0-9]/.test(value)) {
        passwordError.value = 'Password must include at least one number.';
      } else if (!/[@#$%^&+=!]/.test(value)) {
        passwordError.value = 'Password must include at least one special character (@, #, $, etc).';
      } else {
        passwordError.value = '';
      }
    };

    async function handleRegister() {
      validatePassword();
      if (passwordError.value) {
        return;
      }
      loading.value = true;
      try {
        await register({
          email: email.value,
          full_name: fullName.value,
          password: password.value,
          qualification: qualification.value || null,
          dob: dob.value || null,
        });
        alert('Registration successful! Please login.');
        router.push('/SignIn');
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      } finally {
        loading.value = false;
      }
    }

    watch(password, () => {
      validatePassword();
    });

    return {
      email,
      fullName,
      password,
      qualification,
      dob,
      validatePassword,
      passwordError,
      loading,
      handleRegister,
    };
  },
};
</script>

<style scoped>
.left-section {
  flex: 1.3;
  background: url('https://images.unsplash.com/photo-1532074205216-d0e1f4b87368?q=80&w=2200&auto=format&fit=crop') no-repeat center center/cover;
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