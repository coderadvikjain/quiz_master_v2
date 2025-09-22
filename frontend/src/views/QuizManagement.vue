<template>
  <div class="container admin-dashboard">
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <br/><br/>
    <div class="row">
      <div v-for="quiz in quizzes" :key="quiz.id" class="col-md-6 mb-4">
        <div class="subject-box rounded border shadow p-4 bg-white">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="mb-0 text-primary">
              {{ getChapterName(quiz.chapter_id) }} {{ quiz.remarks || 'No Remark' }}
            </h5>
            <div>
              <button class="btn btn-sm btn-link text-success" @click="openEditQuizModal(quiz)" title="Edit Quiz">
                <i class="bi bi-pencil-fill"></i>
              </button>
              <button class="btn btn-sm btn-link text-danger" @click="confirmDeleteQuiz(quiz.id)" title="Delete Quiz">
                <i class="bi bi-trash-fill"></i>
              </button>
            </div>
          </div>
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light" style="position: sticky; top: 0; z-index: 2; background-color: white;">
              <tr>
                <th class="ps-4">Statement</th>
                <th class="text-end pe-4">Actions</th>
              </tr>
            </thead>
          </table>
          <div style="max-height: 120px; overflow-y: auto;" class="scroll-chapter-body border-top">
            <table class="table table-hover align-middle mb-0">
              <tbody>
                <tr v-if="!questions[quiz.id] || !questions[quiz.id].length">
                  <td colspan="3" class="text-center text-muted">No question(s) available yet!</td>
                </tr>
                <tr v-for="question in questions[quiz.id]" :key="question.id">
                  <td class="ps-4">{{ getTruncatedStatement(question.question_statement) }}</td>
                  <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary me-2" @click="openEditQuestionModal(question)">
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteQuestion(question.id)">
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="text-center mt-3">
            <button class="btn btn-sm btn-warning" @click="openAddQuestionModal(quiz.id)" title="Add Question">
              <i class="bi bi-card-text"></i>  Add Question
            </button>
          </div>
        </div>
      </div>
    </div>
    <button
      class="btn btn-gradient-primary rounded-circle position-fixed shadow-lg d-flex align-items-center justify-content-center"
      style="width: 60px; height: 60px; bottom: 30px; right: 30px; font-size: 32px; transition: all 0.3s ease;"
      @click="showAddQuizModal = true"
      title="Add Quiz">
      <i class="bi bi-journal-text"></i>
    </button>
  </div>
  <div v-if="quizzes.length === 0 && !loading" class="text-center text-muted py-5 fs-5">
    No quizzes available. Click the button below to add a new quiz.
  </div>
  <AddQuizModal
    v-if="showAddQuizModal"
    :chapters="chapters"
    @close="closeAddQuizModal"
    @added="handleQuizAdded"
  />

  <EditQuizModal
    v-if="showEditQuizModal"
    :chapters="chapters"
    :quiz="editingQuiz"
    @close="closeEditQuizModal"
    @updated="handleQuizUpdated"
  />

  <AddQuestionModal
    v-if="showAddQuestionModal"
    :quizId="currentQuizId"
    @close="closeAddQuestionModal"
    @added="handleQuestionAdded"
  />

  <EditQuestionModal
    v-if="showEditQuestionModal"
    :question="editingQuestion"
    @close="closeEditQuestionModal"
    @updated="handleQuestionUpdated"
  />
</template>

<script>
import { ref, onMounted, inject, watch } from 'vue';
import {
  getChapterss,
  getQuizzes,
  getQuestions,
  addQuiz,
  updateQuiz,
  deleteQuiz,
  addQuestion,
  updateQuestion,
  deleteQuestion,
} from '@/services/api';

import AddQuizModal from '@/components/AddQuizModal.vue';
import EditQuizModal from '@/components/EditQuizModal.vue';
import AddQuestionModal from '@/components/AddQuestionModal.vue';
import EditQuestionModal from '@/components/EditQuestionModal.vue';

export default {
  name: 'QuizManagement',
  components: {
    AddQuizModal,
    EditQuizModal,
    AddQuestionModal,
    EditQuestionModal,
  },

  setup() {
    const chapters = ref([]);
    const quizzes = ref([]);
    const questions = ref({});
    const allChapters = ref([]);
    const allQuizzes = ref([]);
    const allQuestions = ref({});
    const loading = ref(false);
    const showAddQuizModal = ref(false);
    const showEditQuizModal = ref(false);
    const showAddQuestionModal = ref(false);
    const showEditQuestionModal = ref(false);
    const currentChapterId = ref(null);
    const currentQuizId = ref(null);
    const editingQuiz = ref(null);
    const editingQuestion = ref(null);
    const searchQuery = inject('searchQuery');

    onMounted(async () => {
      document.title = 'StudiQ | QuizOps';
      await fetchChaptersAndQuizzes();
    });

    async function fetchChaptersAndQuizzes() {
      loading.value = true;
      try {
        const res = await getChapterss();
        chapters.value = res.chapters;
        allChapters.value = res.chapters;

        const quizRes = await getQuizzes();
        quizzes.value = quizRes.quizzes || [];
        allQuizzes.value = quizRes.quizzes || [];

        const questionMap = {};
        for (const quiz of allQuizzes.value) {
          const questionRes = await getQuestions(quiz.id);
          questionMap[quiz.id] = questionRes.questions || [];
        }
        questions.value = questionMap;
        allQuestions.value = questionMap;
      } catch (err) {
        console.error('Error fetching data:', err);
      } finally {
        loading.value = false;
      }
    }

    watch(searchQuery, (newQuery) => {
      if (!newQuery) {
        quizzes.value = allQuizzes.value;
        questions.value = allQuestions.value;
        return;
      }

      const query = typeof newQuery === 'string' ? newQuery.toLowerCase() : '';
      const filteredQuizzes = allQuizzes.value.filter((quiz) => {
        const chapter = allChapters.value.find(c => c.id === quiz.chapter_id);
        const chapterName = chapter?.name?.toLowerCase?.() || '';
        const questionsInQuiz = allQuestions.value[quiz.id] || [];
        const questionMatch = questionsInQuiz.some(q =>
          (q?.question_statement?.toLowerCase?.() || '').includes(query)
        );
        return chapterName.includes(query) || questionMatch;
      });

      const updatedQuestionsMap = {};
      filteredQuizzes.forEach(quiz => {
        const allQs = allQuestions.value[quiz.id] || [];
        updatedQuestionsMap[quiz.id] = allQs.filter(q =>
          (q?.question_statement?.toLowerCase?.() || '').includes(query)
        );
      });

      quizzes.value = filteredQuizzes;
      questions.value = updatedQuestionsMap;
    });

    async function handleQuizAdded(newQuiz) {
      try {
        await addQuiz(newQuiz);
        closeAddQuizModal();
        await fetchChaptersAndQuizzes();
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      }
    }

    async function handleQuizUpdated(updatedQuiz) {
      try {
        await updateQuiz(updatedQuiz.id, updatedQuiz);
        closeEditQuizModal();
        await fetchChaptersAndQuizzes();
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      }
    }

    async function confirmDeleteQuiz(quizId) {
      if (confirm("You're about to remove this quiz. Are you sure?")) {
        try {
          await deleteQuiz(quizId);
          await fetchChaptersAndQuizzes();
        } catch {
          alert('Failed to delete quiz');
        }
      }
    }

    async function handleQuestionAdded(newQuestion) {
      try {
        await addQuestion(newQuestion);
        closeAddQuestionModal();
        questions.value[newQuestion.quiz_id] = (await getQuestions(newQuestion.quiz_id)).questions;
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      }
    }

    async function handleQuestionUpdated(updatedQuestion) {
      try {
        await updateQuestion(updatedQuestion.id, updatedQuestion);
        closeEditQuestionModal();
        await fetchChaptersAndQuizzes();
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      }
    }

    async function confirmDeleteQuestion(questionId) {
      if (confirm("You're about to remove this question. Are you sure?")) {
        try {
          await deleteQuestion(questionId);
          await fetchChaptersAndQuizzes();
        } catch {
          alert('Failed to delete question');
        }
      }
    }

    function getChapterName(id) {
      const chapter = chapters.value.find(c => c.id === parseInt(id));
      const name = chapter ? chapter.name : `Chapter ${id}`;
      return name.charAt(0).toUpperCase() + name.slice(1);
    }
    function getTruncatedStatement(statement) {
      if (typeof statement !== 'string') return '';
      const truncated = statement.length > 50 ? statement.slice(0, 50) + '...' : statement;
      return truncated.charAt(0).toUpperCase() + truncated.slice(1);
    }
    function openAddQuizModal() {
      showAddQuizModal.value = true;
    }
    function closeAddQuizModal() {
      showAddQuizModal.value = false;
    }
    function openEditQuizModal(quiz) {
      editingQuiz.value = quiz;
      showEditQuizModal.value = true;
    }
    function closeEditQuizModal() {
      showEditQuizModal.value = false;
      editingQuiz.value = null;
    }
    function openAddQuestionModal(quizId) {
      currentQuizId.value = quizId;
      showAddQuestionModal.value = true;
    }
    function closeAddQuestionModal() {
      showAddQuestionModal.value = false;
    }
    function openEditQuestionModal(question) {
      editingQuestion.value = question;
      showEditQuestionModal.value = true;
    }
    function closeEditQuestionModal() {
      showEditQuestionModal.value = false;
      editingQuestion.value = null;
    }

    return {
      quizzes,
      chapters,
      questions,
      loading,
      getChapterName,
      openAddQuizModal,
      closeAddQuizModal,
      openEditQuizModal,
      closeEditQuizModal,
      openAddQuestionModal,
      closeAddQuestionModal,
      openEditQuestionModal,
      closeEditQuestionModal,
      confirmDeleteQuiz,
      confirmDeleteQuestion,
      getTruncatedStatement,
      handleQuizAdded,
      handleQuestionAdded,
      handleQuizUpdated,
      handleQuestionUpdated,
      currentChapterId,
      currentQuizId,
      editingQuiz,
      editingQuestion,
      showAddQuizModal,
      showEditQuizModal,
      showAddQuestionModal,
      showEditQuestionModal,
    };
  },
};
</script>

<style scoped>
.subject-box {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.subject-box:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}
button.btn i {
  transition: transform 0.2s ease;
}
button.btn:hover i {
  transform: scale(1.2);
}
.btn-warning:hover {
  background-color: #f7b731;
  color: white;
  transform: translateY(-1px);
}
.scroll-chapter-body::-webkit-scrollbar {
  width: 6px;
}
.scroll-chapter-body::-webkit-scrollbar-thumb {
  background: #dee2e6;
  border-radius: 4px;
}
</style>