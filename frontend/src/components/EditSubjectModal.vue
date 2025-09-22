<template>
  <div
    class="modal fade show d-block"
    tabindex="-1"
    role="dialog"
    style="background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(5px);">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <form @submit.prevent="submitEdit" class="modal-content shadow-lg rounded-4 border-0 overflow-hidden">
        <div class="modal-header bg-gradient-primary text-white">
          <h5 class="modal-title fw-bold">Edit Course</h5>
          <button
            type="button"
            class="btn-close"
            @click="$emit('close')"
            aria-label="Close"
            title="Close">
          </button>
        </div>
        <div class="modal-body px-4 py-4 bg-white">
          <div class="mb-4">
            <label for="subjectName" class="form-label fw-semibold">Name</label>
            <input
              type="text"
              id="subjectName"
              v-model="form.name"
              class="form-control form-control-lg shadow-sm"
              required
              placeholder="Enter subject name"
            />
          </div>
          <div>
            <label for="subjectDesc" class="form-label fw-semibold">Description</label>
            <textarea
              id="subjectDesc"
              v-model="form.description"
              class="form-control form-control-lg shadow-sm"
              rows="4"
              placeholder="Enter a short description (optional)">
            </textarea>
          </div>
        </div>
        <div class="modal-footer bg-light px-4 py-3">
          <button
            type="button"
            class="btn btn-outline-secondary fw-semibold"
            @click="$emit('close')">
            Cancel
          </button>
          <button type="submit" class="btn btn-primary fw-semibold d-flex align-items-center">
            <i class="bi bi-pencil-square me-2"></i> Update Course
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditSubjectModal',
  props: {
    subject: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        id: this.subject.id,
        name: this.subject.name,
        description: this.subject.description || '',
      },
    };
  },
  methods: {
    submitEdit() {
      this.$emit('updated', { ...this.form });
    },
  },
};
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(45deg, #4facfe, #00f2fe);
}
.modal-content {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.modal-content.showing {
  transform: scale(1);
  opacity: 1;
}
.modal-content.hiding {
  transform: scale(0.95);
  opacity: 0;
}
</style>