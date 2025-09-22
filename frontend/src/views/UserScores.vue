<template>
  <div class="container py-5">
    <div v-if="loading" class="text-muted">Loading scores...</div>
    <div v-else-if="noScores" class="alert alert-warning rounded-3">No scores available yet.</div>
    <div
      v-for="(score, index) in filteredScores"
      :key="index"
      class="card quiz-score-card mb-4 shadow-sm rounded-4 overflow-hidden border-0">
      <div class="row g-0">
        <div class="col-md-4 bg-light d-flex flex-column justify-content-center text-center p-4 text-dark">
          <h5 class="fw-bold mb-2 text-my">
            {{ capitalizeWords(score.chapter) }} {{ score.remarks }}
          </h5>
          <small class="text-muted d-block">📘 {{ capitalizeWords(score.subject) }}</small>
          <small class="text-muted d-block">🕒 {{ score.duration }} mins</small>
          <small class="text-muted">📅 {{ formatDate(score.date_of_quiz) }}</small>
        </div>
        <div class="col-md-8 p-4 bg-white">
          <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center">
            <div class="mb-2 mb-md-0">
              <h6 class="mb-1 text-muted">Score</h6>
              <div class="fs-5 fw-bold text-primary">
                {{ score.total_scored }} / {{ score.total_questions }}
              </div>
            </div>
            <div class="mb-2 mb-md-0">
              <h6 class="mb-1 text-muted">Percentage</h6>
              <div class="fs-5 fw-bold text-success">
                {{ ((score.total_scored / score.total_questions) * 100).toFixed(2) }}%
              </div>
            </div>
            <div>
              <h6 class="mb-1 text-muted">Time Taken</h6>
              <div class="fs-5 fw-bold text-info">
                {{ formatTime(score.time_taken) }}
              </div>
            </div>
              <span
                class="quiz-tag"
                :class="getPerformanceTag((score.total_scored / score.total_questions) * 100).class">
                {{ getPerformanceTag((score.total_scored / score.total_questions) * 100).label }}
              </span>
            <div class="mt-2">
              <span
                class="badge rounded-pill"
                :class="getgradeTag((score.total_scored / score.total_questions) * 100).class">
                {{ getgradeTag((score.total_scored / score.total_questions) * 100).label }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject, computed } from 'vue'
import { getUserScores } from '@/services/api'

const scores = ref([])
const loading = ref(true)
const searchQuery = inject('searchQuery')

onMounted(() => {
  document.title = 'StudiQ | Grades'
})

const formatDate = (iso) => new Date(iso).toLocaleDateString()
const formatTime = (minutes) => {
  const totalSeconds = Math.round(minutes * 60)
  const min = Math.floor(totalSeconds / 60)
  const sec = totalSeconds % 60
  if (min === 0) return `${sec} sec`
  if (sec === 0) return `${min} min`
  return `${min} min ${sec} sec`
}

const filteredScores = computed(() => {
  const term = searchQuery?.value?.toLowerCase().trim() || ''
  if (!term) return scores.value
  return scores.value.filter(score =>
    score.chapter.toLowerCase().includes(term) ||
    score.subject.toLowerCase().includes(term)
  )
})

const getPerformanceTag = (percentage) => {
  if (percentage >= 90) return { label: 'Excellent', class: 'bg-success' }
  if (percentage >= 50) return { label: 'Good', class: 'bg-warning' }
  return { label: 'Can Improve', class: 'bg-danger' }
}

const getgradeTag = (percentage) => {
  if (percentage >= 90) {
    return { label: 'S (Excellent)', class: 'bg-success text-white' };
  } else if (percentage >= 80) {
    return { label: 'A (Very Good)', class: 'bg-primary text-white' };
  } else if (percentage >= 60) {
    return { label: 'B (Good)', class: 'bg-info text-dark' };
  } else if (percentage >= 50) {
    return { label: 'C (Satisfactory)', class: 'bg-warning text-dark' };
  } else {
    return { label: 'E (Keep Practicing)', class: 'bg-danger text-white' };
  }
};

const noScores = computed(() => Array.isArray(scores.value) && scores.value.length === 0)

onMounted(async () => {
  try {
    const response = await getUserScores()
    scores.value = response.scores
  } catch (err) {
    console.error('Failed to load scores', err)
    scores.value = []
  } finally {
    loading.value = false
  }
})

function capitalizeWords(text) {
  return text.replace(/\b\w/g, char => char.toUpperCase());
}
</script>

<style scoped>
.quiz-score-card {
  transition: all 0.3s ease;
  position: relative;
}
.quiz-score-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}
.quiz-tag {
  position: absolute;
  top: 15px;
  left: -9px;
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
@media (max-width: 576px) {
  .quiz-tag {
    font-size: 10px;
    padding: 6px 12px 4px 12px;
    top: 10px;
  }
  .quiz-score-card .col-md-4 {
    padding-left: 24px;
  }
}
</style>