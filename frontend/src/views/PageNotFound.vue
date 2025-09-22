<template>
  <div class="d-flex flex-column align-items-center justify-content-center text-center min-vh-100">
    <h2 class="my-4 display-5 fw-semibold">Uh-no! Page Not Found</h2>
    <img src="@/assets/404.png" alt="404" class="img-fluid w-75 max-w-600px" />
    <h4 class="my-4 fs-5">Hmm… this link might be broken or outdated.</h4>
    <button class="btn btn-outline-danger fw-bold px-4 py-2 rounded-pill" @click="goHome">
      GO BACK
    </button>
  </div>
</template>

<script>
export default {
  name: "PageNotFound",
  mounted() {
    document.title = 'StudiQ | 404';
  },

  methods: {
    goHome() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.max-w-600px {
  max-width: 600px;
}
@media (max-width: 767px) {
  h2 {
    font-size: 2rem;
  }
  h4 {
    font-size: 1rem;
  }
}
</style>