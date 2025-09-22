<template>
  <div class="container py-5">
    <div class="row g-4">
      <div
        v-for="quiz in filteredQuizzes"
        :key="quiz.id"
        class="col-md-6 position-relative">
        <div
          class="quiz-card glass-card p-4 rounded-4"
          @mouseover="hover = true"
          @mouseleave="hover = false">
        <div
          v-if="quiz.attempted"
          class="quiz-tag bg-success">
          Attempted
        </div>
          <h5 class="text-my fw-semibold mb-2 text-dark">
            {{ capitalizeWords(quiz.chapter) }} {{ quiz.remarks }}
          </h5>
          <p class="text-muted small"><strong>Course :</strong> {{ capitalizeWords(quiz.subject) }}</p>
          <p class="text-muted small"><strong>No. of Questions :</strong> {{ quiz.questionCount }}</p>
          <div class="d-flex justify-content-between align-items-center mt-3">
            <span
              class="badge px-3 py-1"
              :class="quiz.attempted ? 'bg-success' : 'bg-primary'">
              ⏱️ {{ quiz.duration }} mins
            </span>
            <button
              @click="openQuiz(quiz)"
              class="btn rounded-pill px-3 fw-semibold"
              :class="quiz.attempted ? 'btn-outline-warning' : 'btn-outline-danger'">
              {{ quiz.attempted ? 'Retake Quiz' : 'Start Quiz' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <p v-if="!allQuizzes.length" class="text-muted mt-5 text-center">
      No quizzes found.
    </p>
  </div>
  <QuizModal
    :show="showModal"
    :quizId="selectedQuizId"
    :duration="selectedQuizDuration"
    @close="showModal = false"
    @submitted="handleQuizSubmit"
  />
</template>

<script>
import { ref, onMounted, inject, computed } from 'vue'
import { getUserDashboard, getUserScores } from '@/services/api'
import QuizModal from '@/components/QuizModal.vue'

export default {
  name: 'UserDashboard',
  components: {
    QuizModal,
  },
  setup() {
    const allQuizzes = ref([])
    const showModal = ref(false)
    const selectedQuizId = ref(null)
    const selectedQuizDuration = ref(0)
    const searchQuery = inject('searchQuery')
    const loading = ref(false)

    onMounted(() => {
      document.title = 'StudiQ | Dashboard'
      fetchQuizzes()
    })

    async function fetchQuizzes() {
      loading.value = true
      try {
        const quizRes = await getUserDashboard()
        let scoreRes = []
        try {
          scoreRes = await getUserScores()
        } catch (scoreErr) {
          console.warn('Could not load scores:', scoreErr)
        }
        
        const scores = scoreRes.scores
        const attemptedIds = scores.map((s) => s.quiz_id)
        const today = new Date().toISOString().split('T')[0]

        allQuizzes.value = quizRes
          .filter(
            (quiz) =>
              quiz.date_of_quiz &&
              quiz.date_of_quiz <= today &&
              quiz.questionCount > 0
          )
          .map((quiz) => ({
            ...quiz,
            attempted: attemptedIds.includes(quiz.id),
          }))
      } catch (err) {
        console.error('Failed to load dashboard:', err)
      } finally {
        loading.value = false
      }
    }

    const handleQuizSubmit = () => {
      showModal.value = false
      fetchQuizzes()
    }

    const filteredQuizzes = computed(() => {
      const query = searchQuery?.value?.toLowerCase().trim()
      if (!query) return allQuizzes.value

      return allQuizzes.value.filter((quiz) => {
        const subject = quiz.subject?.toLowerCase() || ''
        const chapter = quiz.chapter?.toLowerCase() || ''
        return subject.includes(query) || chapter.includes(query)
      })
    })

    const openQuiz = (quiz) => {
      selectedQuizId.value = quiz.id
      selectedQuizDuration.value = Number(quiz.duration)
      showModal.value = true
    }

    function capitalizeWords(text) {
      return text.replace(/\b\w/g, (char) => char.toUpperCase())
    }

    return {
      allQuizzes,
      showModal,
      handleQuizSubmit,
      selectedQuizId,
      filteredQuizzes,
      selectedQuizDuration,
      capitalizeWords,
      openQuiz,
      fetchQuizzes,
      loading,
    }
  },
}
</script>

<style scoped>
.quiz-card {
  backdrop-filter: blur(14px);
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  color: white;
}
.quiz-card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.25);
  border-color: rgba(255, 255, 255, 0.3);
}
.quiz-tag {
  position: absolute;
  top: 15px;
  right: -9px;
  background-color: #28a745;
  color: white;
  padding: 6px 16px 6px 12px;
  font-size: 12px;
  font-weight: bold;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  clip-path: polygon(0 0, 100% 0, 90% 50%, 100% 100%, 0 100%);
  z-index: 10;
}
</style>