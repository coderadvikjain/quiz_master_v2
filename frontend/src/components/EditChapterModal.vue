<template>
  <div
    class="modal fade show d-block"
    tabindex="-1"
    role="dialog"
    style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <form @submit.prevent="submitEdit" class="modal-content shadow-lg rounded-4 border-0 overflow-hidden">
        <div class="modal-header bg-gradient-yellow text-white">
          <h5 class="modal-title fw-bold">Edit Chapter</h5>
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
            <label for="chapterName" class="form-label fw-semibold">Name</label>
            <input
              type="text"
              id="chapterName"
              v-model="form.name"
              class="form-control form-control-lg shadow-sm"
              required
              placeholder="Enter chapter name"
            />
          </div>
          <div>
            <label for="chapterDescription" class="form-label fw-semibold">Description</label>
            <textarea
              id="chapterDescription"
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
          <button type="submit" class="btn btn-warning fw-semibold d-flex align-items-center text-white">
            <i class="bi bi-pencil-square me-2"></i> Update Chapter
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditChapterModal',
  props: {
    chapter: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        id: this.chapter.id,
        name: this.chapter.name,
        subject_id: this.chapter.subject_id,
        description: this.chapter.description || '',
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
.bg-gradient-yellow {
  background: linear-gradient(45deg, #fceabb, #f8b500);
}
.modal-content {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
</style>