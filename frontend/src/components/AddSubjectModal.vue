<template>
  <div
    class="modal fade show"
    tabindex="-1"
    style="display: block; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(3px);"
    role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <form @submit.prevent="submit" class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
        <div class="modal-header text-white bg-gradient-subject px-4 py-3">
          <h5 class="modal-title fw-bold">📘 Add New Course</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="$emit('close')"
            aria-label="Close"
            title="Close">
          </button>
        </div>
        <div class="modal-body px-4 py-4 bg-white">
          <div class="mb-4">
            <label class="form-label fw-semibold">Name</label>
            <input
              type="text"
              class="form-control form-control-lg shadow-sm"
              v-model="name"
              placeholder="Eg. Mathematics" required/>
          </div>
          <div>
            <label class="form-label fw-semibold">Description</label>
            <textarea
              class="form-control form-control-lg shadow-sm"
              v-model="description"
              rows="4"
              placeholder="E.g. Covers algebra, geometry, trigonometry, and more...">
            </textarea>
          </div>
        </div>
        <div class="modal-footer bg-light px-4 py-3">
          <button type="button" class="btn btn-outline-secondary fw-semibold" @click="$emit('close')">
            Cancel
          </button>
          <button type="submit" class="btn btn-primary fw-semibold d-flex align-items-center">
            <i class="bi bi-save me-2"></i> Add Course
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddSubjectModal',
  emits: ['close', 'added'],
  data() {
    return {
      name: '',
      description: '',
    };
  },
  methods: {
    submit() {
      const name = this.name.trim();
      const description = this.description.trim();
      if (!name || !description) {
        alert('Both name and description are required.');
        return;
      }
      this.$emit('added', { name, description });
      this.name = '';
      this.description = '';
      this.$emit('close');
    },
  },
};
</script>

<style scoped>
.bg-gradient-subject {
  background: linear-gradient(135deg, #667eea, #764ba2); /* blue-violet gradient */
}

.modal-content {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
</style>