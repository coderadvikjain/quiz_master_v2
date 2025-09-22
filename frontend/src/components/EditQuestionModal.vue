<template>
  <div
    class="modal fade show"
    tabindex="-1"
    style="display: block; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(3px);"
    role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <form @submit.prevent="submitEdit" class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
        <div class="modal-header text-white bg-gradient-question px-4 py-3">
          <h5 class="modal-title fw-bold">Edit Question</h5>
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
            <label class="form-label fw-semibold">Question Statement</label>
            <textarea
              v-model="form.question_statement"
              class="form-control form-control-lg shadow-sm"
              placeholder="Enter your question here" required>
            </textarea>
            </div>
            <div class="mb-4">
              <input v-model="form.option1" type="text" class="form-control mb-2" placeholder="Option 1" />
              <input v-model="form.option2" type="text" class="form-control mb-2" placeholder="Option 2" />
              <input v-model="form.option3" type="text" class="form-control mb-2" placeholder="Option 3" />
              <input v-model="form.option4" type="text" class="form-control mb-2" placeholder="Option 4" />
            </div>
            <select v-model="form.correct_option" class="form-select shadow-sm" required>
              <option disabled value="">Select correct option</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
            </select>
          </div>
        <div class="modal-footer bg-light px-4 py-3">
          <button type="button" class="btn btn-outline-secondary fw-semibold" @click="$emit('close')">
            Cancel
          </button>
          <button type="submit" class="btn btn-warning fw-semibold d-flex align-items-center text-white">
            <i class="bi bi-pencil-square me-2"></i> Edit Question
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditQuestionModal',
  props: {
    question: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        id: this.question.id,
        question_statement: this.question.question_statement,
        option1: this.question.option1,
        option2: this.question.option2,
        option3: this.question.option3,
        option4: this.question.option4,
        correct_option: this.question.correct_option,
        quiz_id: this.question.quiz_id,
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
.bg-gradient-question {
  background: linear-gradient(135deg, #f6d365, #fda085);
}
.modal-content {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
</style>