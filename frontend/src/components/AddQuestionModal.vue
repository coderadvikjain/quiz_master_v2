<template>
  <div
    class="modal fade show"
    tabindex="-1"
    style="display: block; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(3px);"
    role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <form @submit.prevent="submit" class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
        <div class="modal-header text-white bg-gradient-question px-4 py-3">
          <h5 class="modal-title fw-bold">📋 Add New Question</h5>
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
            <label class="form-label fw-semibold">Question Statement</label>
            <textarea
              v-model="question.question_statement"
              class="form-control form-control-lg shadow-sm"
              placeholder="Enter your question here"
              :class="{ 'is-invalid': error && !question.question_statement.trim() }" required>
            </textarea>
          </div>
          <div class="mb-4">
            <input v-model="question.option1" type="text" class="form-control mb-2" placeholder="Option 1" />
            <input v-model="question.option2" type="text" class="form-control mb-2" placeholder="Option 2" />
            <input v-model="question.option3" type="text" class="form-control mb-2" placeholder="Option 3" />
            <input v-model="question.option4" type="text" class="form-control mb-2" placeholder="Option 4" />
          </div>
          <select v-model="question.correct_option" class="form-select shadow-sm" required>
            <option disabled value="">Select correct option</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
          </select>
        </div>
        <div class="modal-footer bg-light px-4 py-3">
          <button type="button" class="btn btn-outline-secondary fw-semibold" @click="handleCancel">
            Cancel
          </button>
          <button type="submit" class="btn btn-warning fw-semibold d-flex align-items-center text-white">
            <i class="bi bi-save me-2"></i> Add Question
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddQuestionModal',
  props: {
    quizId: Number,
  },
  emits: ['close', 'added'],
  data() {
    return {
      question: {
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: '',
      },
      error: '',
    };
  },
  methods: {
    submit() {
      const { question_statement, option1, option2, option3, option4, correct_option } = this.question;
      if (
        !question_statement.trim() ||
        !option1.trim() ||
        !option2.trim() ||
        !option3.trim() ||
        !option4.trim() ||
        ![1, 2, 3, 4].includes(Number(correct_option)))
        {
        this.error = 'All fields are required, and correct option must be 1, 2, 3, or 4.';
        return;
      }
      this.error = '';
      this.$emit('added', {
        quiz_id: this.quizId,
        question_statement: question_statement.trim(),
        option1: option1.trim(),
        option2: option2.trim(),
        option3: option3.trim(),
        option4: option4.trim(),
        correct_option: Number(correct_option),
      });
      this.resetForm();
    },

    handleCancel() {
      this.resetForm();
      this.$emit('close');
    },

    resetForm() {
      this.question = {
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: '',
      };
      this.error = '';
    },
  },
};
</script>

<style scoped>
.bg-gradient-question {
  background: linear-gradient(135deg, #fdd819, #e8058e);
}
.modal-content {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
</style>