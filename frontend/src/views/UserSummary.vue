<template>
  <div class="container mt-5">
    <div class="row mb-4" v-if="dashboard">
      <div class="col-md-3 mb-3" v-for="item in summaryCards" :key="item.label">
        <div class="card shadow text-center p-3 bg-white">
          <h5>{{ item.label }}</h5>
          <h3 :class="item.color + ' fw-bold'">{{ item.value }}</h3>
        </div>
      </div>
    </div>
    <div class="row gy-4">
      <div
        v-for="(score, index) in filteredScores"
        :key="score.quiz_id"
        class="col-md-4 chart-container">
        <div class="card shadow p-3 bg-white mb-4 w-100">
          <h5 class="text-center mb-3">{{ capitalizeWords(score.chapter) }} {{ score.remarks }}</h5>
          <canvas :id="'quizChart-' + index" height="300"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed, inject } from 'vue';
import Chart from 'chart.js/auto';
import { getUserScores, getUserDashboard } from '@/services/api';

const scores = ref([]);
const dashboard = ref(null);
const searchQuery = inject('searchQuery')

onMounted(async () => {
  document.title = 'StudiQ | Insights';
  await loadSummary();
  await loadChartData();
});

const loadSummary = async () => {
  try {
    dashboard.value = await getUserDashboard();
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  }
};

const loadChartData = async () => {
  try {
    const res = await getUserScores();
    scores.value = res.scores;
    await nextTick();

    scores.value.forEach((score, index) => {
      const correct = score.total_scored ?? 0;
      const total = score.total_questions ?? 1;
      const incorrect = total - correct;

      const ctx = document.getElementById(`quizChart-${index}`)?.getContext('2d');
      if (!ctx) return;

      const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';

      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Correct', 'Incorrect'],
          datasets: [
            {
              label: 'Score',
              data: [correct, incorrect],
              backgroundColor: ['#28a745', '#dc3545'],
              borderColor: isDarkMode ? ['#2f2f41', '#2f2f41'] : ['#fff', '#fff'],
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              callbacks: {
                label: (tooltipItem) => {
                  const value = tooltipItem.raw;
                  const percent = ((value / total) * 100).toFixed(1);
                  return `${tooltipItem.label}: ${value} / ${total} (${percent}%)`;
                }
              }
            },
            legend: {
              display: true,
              position: 'top',
               labels: {
                 color: isDarkMode ? '#fff' : '#000'
              }
            }
          }
        }
      });
    });
  } catch (error) {
    console.error('Error loading user scores:', error);
  }
};

const summaryCards = computed(() => {
  if (!dashboard.value || !scores.value || scores.value.length === 0) return [];

  const validScores = scores.value;
  const totalCorrect = validScores.reduce((sum, score) => sum + (score.total_scored || 0), 0);
  const totalSpent = validScores.reduce((sum, score) => sum + (score.time_taken|| 0), 0);

  const formatTime = (minutesFloat) => {
    const totalSeconds = Math.round(minutesFloat * 60);
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;

    if (mins === 0) return `${secs} sec`;
    return `${mins} min ${secs} sec`;
  };

  return [{
  label: 'Total Quizzes', value: dashboard.value.filter(q => {
    const quizDate = new Date(q.date_of_quiz);
    const today = new Date();
    return q.questionCount > 0 && quizDate && quizDate <= today;}).length, color: 'text-primary'},
    { label: 'Total Attempts', value: validScores.length, color: 'text-success' },
    { label: 'Correct Answers', value: totalCorrect, color: 'text-warning' },
    { label: 'Time Spent', value: formatTime(totalSpent), color: 'text-danger' }
  ];
});
    const filteredScores = computed(() => {
    const query = searchQuery?.value?.toLowerCase().trim();
    if (!query) return scores.value;

    return scores.value.filter((score) => {
      const subject = score.subject?.toLowerCase() || '';
      const chapter = score.chapter?.toLowerCase() || '';
      return subject.includes(query) || chapter.includes(query);
    });
  });
  function capitalizeWords(text) {
    return text.replace(/\b\w/g, char => char.toUpperCase());
  }
</script>

<style scoped>
.chart-container {
  min-height: 350px;
}
canvas {
  display: block;
  max-width: 100%;
  height: 420px !important;
}
.card {
  border-radius: 16px;
  background: #f8f9fa;
}
.card-header {
  font-size: 1rem;
}
</style>