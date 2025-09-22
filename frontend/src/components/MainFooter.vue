<template>
  <footer class="app-footer border-top w-100 z-10">
    <div class="container py-3 px-4">
      <div class="d-flex justify-content-center align-items-center text-center">
        <p class="footer-text text-muted small mb-0">
          &copy; {{ new Date().getFullYear() }}
          <span class="fw-semibold text-warning"> StudiQ</span>. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'MainFooter',
};
</script>