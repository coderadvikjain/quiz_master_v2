<template>
  <div
    class="modal fade show"
    tabindex="-1"
    style="display: block; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(3px);"
    role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <form @submit.prevent="submit" class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">  
        <div class="modal-header text-white bg-gradient-quiz px-4 py-3">
          <h5 class="modal-title fw-bold">🧩 Add New Quiz</h5>
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
            <label class="form-label fw-semibold">Select Chapter</label>
            <select
              v-model="selectedChapter"
              class="form-select form-select-lg shadow-sm" required>
              <option value="" disabled>Select a chapter</option>
              <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                {{ chapter.name }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label class="form-label fw-semibold">Date of Quiz</label>
            <input type="date" class="form-control form-control-lg shadow-sm" v-model="date_of_quiz" required />
          </div>
          <div>
            <label class="form-label fw-semibold">Time Duration (in minutes)</label>
            <input type="number" class="form-control form-control-lg shadow-sm" v-model="time_duration" min="1" required />
          </div>
        </div>
        <div class="modal-footer bg-light px-4 py-3">
          <button type="button" class="btn btn-outline-secondary fw-semibold" @click="$emit('close')">
            Cancel
          </button>
          <button type="submit" class="btn btn-success fw-semibold d-flex align-items-center">
            <i class="bi bi-save me-2"></i> Add Quiz
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddQuizModal',
  props: {
    chapters: {
      type: Array,
      required: true
    }
  },
  emits: ['close', 'added'],
  data() {
    return {
      selectedChapter: '',
      date_of_quiz: '',
      time_duration: '',
    };
  },
  methods: {
    submit() {
      if (!this.selectedChapter || !this.date_of_quiz || this.time_duration === '') {
        alert('Please fill all required fields');
        return;
      }
      const selectedDate = new Date(this.date_of_quiz);
      const today = new Date();
      selectedDate.setHours(0, 0, 0, 0);
      today.setHours(0, 0, 0, 0);
      if (selectedDate < today) {
        alert('Quiz date cannot be in the past');
        return;
      }
      if (this.time_duration < 1) {
        alert('Time duration must be positive');
        return;
      }
      const quiz = {
        chapter_id: this.selectedChapter,
        date_of_quiz: this.date_of_quiz,
        time_duration: this.time_duration,
      };
      this.$emit('added', quiz);
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
.bg-gradient-quiz {
  background: linear-gradient(135deg, #a8e063, #56ab2f);
}
.modal-content {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
</style>