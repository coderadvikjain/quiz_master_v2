<template>
  <div
    class="modal fade show"
    tabindex="-1"
    style="display: block; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(3px);"
    role="dialog"
    @click.self="$emit('close')">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
        <div class="modal-header text-white bg-gradient-user px-4 py-3">
          <h5 class="modal-title fw-bold">👤 User Info</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="$emit('close')"
            aria-label="Close"
            title="Close">
          </button>
        </div>
        <div class="modal-body px-4 py-4 bg-white">
          <div class="mb-3">
            <strong class="text-muted">Full Name:</strong>
            <div class="fs-5 fw-semibold text-capitalize">{{ user.full_name }}</div>
          </div>
          <div class="mb-3">
            <strong class="text-muted">Email:</strong>
            <div>{{ user.email }}</div>
          </div>
          <div class="mb-3">
            <strong class="text-muted">Qualification:</strong>
            <div>{{ user.qualification || 'N/A' }}</div>
          </div>
          <div>
            <strong class="text-muted">Date of Birth:</strong>
            <div>{{ user.dob || 'N/A' }}</div>
          </div>
        </div>
        <div class="modal-footer bg-light px-4 py-3 d-flex justify-content-end">
          <button class="btn btn-secondary fw-semibold" @click="$emit('close')">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserModal',
  props: {
    user: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.bg-gradient-user {
  background: linear-gradient(135deg, #2193b0, #6dd5ed);
}
.modal-content {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
</style>