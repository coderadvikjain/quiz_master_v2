<template>
  <div
    class="modal fade show"
    tabindex="-1"
    style="display: block; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(3px);"
    role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <form @submit.prevent="submitEdit" class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">        
        <div class="modal-header text-white bg-gradient-quiz px-4 py-3">
          <h5 class="modal-title fw-bold">Edit Quiz</h5>
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
            <label class="form-label fw-semibold">Select Chapter</label>
            <select
              v-model="form.chapter_id"
              class="form-select form-select-lg shadow-sm" required>
              <option value="" disabled>Select a chapter</option>
              <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                {{ chapter.name }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label class="form-label fw-semibold">Date of Quiz</label>
            <input type="date" class="form-control form-control-lg shadow-sm" v-model="form.date_of_quiz" required />
          </div>
          <div>
            <label class="form-label fw-semibold">Time Duration (in minutes)</label>
            <input type="number" class="form-control form-control-lg shadow-sm" v-model="form.time_duration" required />
          </div>
        </div>
        <div class="modal-footer bg-light px-4 py-3">
          <button type="button" class="btn btn-outline-secondary fw-semibold" @click="$emit('close')">
            Cancel
          </button>
          <button type="submit" class="btn btn-success fw-semibold d-flex align-items-center">
            <i class="bi bi-pencil-square me-2"></i> Update Quiz
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditQuizModal',
  props: {
    quiz: {
      type: Object,
      required: true
    },
    chapters: {
      type: Array,
      required: true
    },
  },
  data() {
    let quizDate = '';
    if (this.quiz.date_of_quiz) {
      quizDate = new Date(this.quiz.date_of_quiz).toISOString().split('T')[0];
    }
    return {
      form: {
      id: this.quiz.id,
      chapter_id: this.quiz.chapter_id,
      date_of_quiz: quizDate,
      time_duration: this.quiz.time_duration,
      remarks: this.quiz.remarks || '',
      },
    };
  },
  methods: {
    submitEdit() {
      const selectedDate = new Date(this.form.date_of_quiz);
      const today = new Date();
      selectedDate.setHours(0, 0, 0, 0);
      today.setHours(0, 0, 0, 0);

      if (this.form.time_duration < 1) {
        alert('Time duration must be positive');
        return;
      }

      this.$emit('updated', { ...this.form });
    },
  },
};
</script>

<style scoped>
.bg-gradient-quiz {
  background: linear-gradient(135deg, #43cea2, #185a9d);
}
.modal-content {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
</style>