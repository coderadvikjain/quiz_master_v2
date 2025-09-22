<template>
  <div
    class="modal fade show"
    tabindex="-1"
    style="display: block; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(3px);"
    role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <form @submit.prevent="submit" class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
        <div class="modal-header text-white bg-gradient-chapter px-4 py-3">
          <h5 class="modal-title fw-bold">📄 Add New Chapter</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="handleCancel"
            aria-label="Close"
            title="Close">
          </button>
        </div>
        <div class="modal-body px-4 py-4 bg-white">
          <div class="mb-4">
            <label class="form-label fw-semibold">Name</label>
            <input
              v-model="chapter.name"
              type="text"
              maxlength="100"
              class="form-control form-control-lg shadow-sm"
              placeholder="Eg. Introduction to Algebra"
              :class="{ 'is-invalid': error && !chapter.name.trim() }"
              required
            />
            <div class="invalid-feedback" v-if="error && !chapter.name.trim()">
              {{ error }}
            </div>
          </div>
          <div>
            <label class="form-label fw-semibold">Description</label>
            <textarea
              v-model="chapter.description"
              maxlength="300"
              class="form-control form-control-lg shadow-sm"
              rows="4"
              placeholder="Eg. This chapter includes basic concepts, formulas, and problem sets."
              :class="{ 'is-invalid': error && !chapter.description.trim() }" required>
            </textarea>
            <div class="invalid-feedback" v-if="error && !chapter.description.trim()">
              {{ error }}
            </div>
          </div>
        </div>
        <div class="modal-footer bg-light px-4 py-3">
          <button type="button" class="btn btn-outline-secondary fw-semibold" @click="handleCancel">
            Cancel
          </button>
          <button type="submit" class="btn btn-warning fw-semibold d-flex align-items-center text-white">
            <i class="bi bi-save me-2"></i> Add Chapter
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddChapterModal',
  props: {
    visible: Boolean,
    subjectId: Number,
  },
  emits: ['close', 'added'],
  data() {
    return {
      chapter: {
        name: '',
        description: '',
      },
      error: '',
    };
  },
  methods: {
    submit() {
      const name = this.chapter.name.trim();
      const description = this.chapter.description.trim();
      if (!name || !description) {
        this.error = 'Both name and description are required.';
        return;
      }
      this.error = '';
      this.$emit('added', { name, description, subject_id: this.subjectId });
      this.resetForm();
    },

    handleCancel() {
      this.resetForm();
      this.$emit('close');
    },

    resetForm() {
      this.chapter = { name: '', description: '' };
      this.error = '';
    },
  },
};
</script>

<style scoped>
.bg-gradient-chapter {
  background: linear-gradient(135deg, #f7971e, #ffd200); /* orange-yellow gradient */
}
.modal-content {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
</style>