<template>
  <div v-if="show" class="modal fade show" tabindex="-1" style="display: block; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(3px);" role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">        
        <div class="modal-body px-4 py-4 bg-white">
          <div class="d-flex justify-content-between mb-3" v-if="!finished">
            <strong>Question {{ progress + 1 }} / {{ quizQuestionCount }}</strong>
            <span class="text-danger">⏱️ {{ formattedTime }}</span>
          </div>
          <div v-if="loading" class="text-center my-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          <div v-else-if="!finished">
            <p class="form-control form-control-lg shadow-sm"><strong>Q{{ progress + 1 }}:</strong> {{ question.text }}</p>
            <div
              v-for="(option, index) in question.options"
              :key="index"
              class="rounded-3 px-3 py-2 mb-3 option-box"
              :class="{ 'bg-light border-warning': selectedOption === index + 1 }"
              style="cursor: pointer;"
              @click="selectedOption = index + 1">
              <div class="form-check">
                <input
                  class="form-check-input me-2 bg-warning border-warning"
                  type="radio"
                  :id="`option-${index}`"
                  name="quizOption"
                  :value="index + 1"
                  v-model="selectedOption"
                  style="pointer-events: none;"
                />
                <label class="form-check-label fw-medium w-100" :for="`option-${index}`">
                  {{ option }}
                </label>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-4">
            <img
              src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3aG93c3N1c2hqMmhqdXRrbm90OTR4a2VpZ2gyNGk2bGhvbXljc3drMCZlcD12MV9zdGlja2Vyc19yZWxhdGVkJmN0PXM/t4IdxQS5RRgPlGFF7Z/giphy.gif"
              alt="Quiz Completed"
              class="img-fluid mb-3"
              style="max-height: 180px; border-radius: 12px;"
            />
            <h4
              v-if="score >= Math.ceil(totalQuestions * 0.9)"
              class="fw-bold text-primary">
              🏆 Outstanding Performance!
            </h4>
            <h4
              v-else-if="score >= Math.ceil(totalQuestions * 0.5)"
              class="fw-bold text-success">
              🎉 Great Job! Keep it up!
            </h4>
            <h4
              v-else
              class="fw-bold text-warning">
              📚 Keep Practicing! You'll get there!
            </h4>
            <p class="mb-1 fs-5">🔢 <strong>Score:</strong> {{ score }} / {{ totalQuestions }}</p>
            <p class="fs-6">⏱️ <strong>Time Taken:</strong> {{ formattedTimeTaken }} mins</p>
          </div>
        </div>
        <div class="modal-footer bg-light px-4 py-3">
          <button
            v-if="!finished"
            type="button"
            class="btn btn-outline-danger fw-semibold"
            :disabled="progress === 0"
            @click="goToPreviousQuestion">
            Previous
          </button>
          <button
            v-if="!finished"
            type="button"
            class="btn fw-semibold text-white"
            :class="isLastQuestion ? 'btn-success' : 'btn-primary'"
            @click="submitCurrentAnswer">
            {{ isLastQuestion ? 'Submit Quiz' : 'Next' }}
          </button>
          <button
            v-else
            type="button"
            class="btn btn-outline-success fw-semibold"
            @click="close">
            Done
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
import { getUserDashboard, getQuizQuestion, submitAnswer as submitAnswerApi, saveQuizResult } from '@/services/api'

export default {
  name: 'QuizModal',
  props: {
    show: Boolean,
    quizId: Number,
    duration: Number,
  },
  emits: ['close'],
  setup(props, { emit }) {
    const question = ref({})
    const selectedOption = ref(null)
    const loading = ref(false)
    const finished = ref(false)
    const progress = ref(0)
    const visitedQuestions = ref(new Set())
    const answeredQuestions = ref({})
    const score = ref(0)
    const totalQuestions = ref(0)
    const quizQuestionCount = ref(null)
    const startTime = ref(null)
    const timeTaken = ref(0)
    const timeLeft = ref(0)

    let timerInterval = null

    const formattedTime = computed(() => {
      const mins = Math.floor(timeLeft.value / 60).toString().padStart(2, '0')
      const secs = (timeLeft.value % 60).toString().padStart(2, '0')
      return `${mins}:${secs}`
    })

    const loadQuestion = async () => {
      loading.value = true
      selectedOption.value = null
      try {
        const res = await getQuizQuestion(props.quizId, progress.value)
        question.value = res
        selectedOption.value = answeredQuestions.value[progress.value] || null
        if (!visitedQuestions.value.has(progress.value)) {
          totalQuestions.value++
          visitedQuestions.value.add(progress.value)
        }
        loading.value = false
      } catch (err) {
        console.error('No more questions or error:', err)
        finished.value = true
        clearInterval(timerInterval)
      }
    }

    const isLastQuestion = computed(() => {
      return quizQuestionCount.value !== null && totalQuestions.value === quizQuestionCount.value
    })

    const goToPreviousQuestion = async () => {
      if (progress.value === 0) return
      progress.value--
      await loadQuestion()
    }

    const submitCurrentAnswer = async () => {
      try {
        const prevAnswer = answeredQuestions.value[progress.value]
        const newAnswer = selectedOption.value

        answeredQuestions.value[progress.value] = newAnswer

        const res = await submitAnswerApi({
          quiz_id: props.quizId,
          question_id: question.value?.id,
          selected_option: newAnswer,
          start_time: startTime.value.toISOString(),
          progress: progress.value,
          current_score: score.value
        })

        const correctOption = question.value.correct_option
        const prevWasCorrect = prevAnswer === correctOption
        const newIsCorrect = newAnswer === correctOption

        if (prevAnswer !== newAnswer) {
          if (prevWasCorrect && !newIsCorrect) {
            score.value -= 1
          } else if (!prevWasCorrect && newIsCorrect) {
            score.value += 1
          }
        }

        if (res.finished) {
          await finishQuiz(score.value, res.time_taken)
        } else {
          progress.value = res.next_progress
          await loadQuestion()
        }
      } catch (err) {
        console.error('Error submitting answer:', err)
        alert('There was a problem submitting your answer. Please try again.')
      }
    }

    const autoSubmit = async () => {
      console.warn('⏱️ Time is up! Auto-submitting quiz...')
      finished.value = true
      clearInterval(timerInterval)

      const payload = {
        quiz_id: props.quizId,
        question_id: question.value?.id || null,
        selected_option: selectedOption.value ?? null,
        start_time: startTime.value.toISOString(),
        progress: progress.value,
        current_score: score.value,
      }
      try {
          const res = await submitAnswerApi(payload)
          await finishQuiz(score.value, res.time_taken)
        } catch (err) {
          console.error('Auto submit failed:', err)
          alert('Quiz auto-submit failed.')
        }
      }

    const finishQuiz = async (finalScore, timeSpent) => {
      finished.value = true
      timeTaken.value = timeSpent
      score.value = finalScore
      clearInterval(timerInterval)

      await saveQuizResult({
        quiz_id: props.quizId,
        score: score.value,
        total_questions: totalQuestions.value,
        time_taken: timeSpent,
      })
    }

    const formattedTimeTaken = computed(() => {
      const total = Math.round(timeTaken.value)
      const mins = Math.floor(total / 60).toString().padStart(2, '0')
      const secs = (total % 60).toString().padStart(2, '0')
      return `${mins}:${secs}`
    })

    const close = () => {
      clearInterval(timerInterval)
      emit('close')
      emit('submitted')
    }

    watch(() => props.show, async (val) => {
      if (val) {
        score.value = 0
        progress.value = 0
        finished.value = false
        totalQuestions.value = 0
        visitedQuestions.value = new Set()
        answeredQuestions.value = {}
        startTime.value = new Date()
        timeLeft.value = props.duration * 60
        
        const dashboard = await getUserDashboard()
        const quizList = dashboard || []
        const quiz = quizList.find(q => Number(q.id) === Number(props.quizId))
        if (quiz) {
          quizQuestionCount.value = quiz.questionCount
        }
        timerInterval = setInterval(() => {
          if (timeLeft.value > 0) {
            timeLeft.value--
          } else {
            autoSubmit()
          }
        }, 1000)
        await loadQuestion()
      }
    })

    onUnmounted(() => {
      clearInterval(timerInterval)
    })

    const preventBack = () => {
      if (!finished.value) {
        history.pushState(history.state, '', location.href)
        alert('⚠️ Please complete the quiz before exiting.')
      }
    }

    const preventEsc = (e) => {
      if (e.key === 'Escape' && !finished.value) {
        e.preventDefault()
      }
    }

    onMounted(() => {
      history.pushState(history.state, '', location.href)
      window.addEventListener('popstate', preventBack)
      window.addEventListener('keydown', preventEsc)
    })

    onUnmounted(() => {
      window.removeEventListener('popstate', preventBack)
      window.removeEventListener('keydown', preventEsc)
    })

    return {
      question,
      selectedOption,
      loading,
      finished,
      goToPreviousQuestion,
      isLastQuestion,
      score,
      totalQuestions,
      timeTaken,
      formattedTime,
      formattedTimeTaken,
      progress,
      quizQuestionCount,
      close,
      submitCurrentAnswer,
    }
  }
}
</script>

<style scoped>
.quiz-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.quiz-modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}
.option-box:hover {
  background-color: #f8f9fa;
  transition: background-color 0.2s ease-in-out;
}
</style>