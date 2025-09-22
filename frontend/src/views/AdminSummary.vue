<template>
  <div class="container mt-5">
    <div class="row mb-4" v-if="summary">
      <div class="col-md-3 mb-3">
        <div class="card shadow text-center p-3 bg-white">
          <h5>Total Subjects</h5>
          <h3 class="text-success fw-bold">{{ summary.totalSubjects }}</h3>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow text-center p-3 bg-white">
          <h5>Total Chapters</h5>
          <h3 class="text-warning fw-bold">{{ summary.totalChapters }}</h3>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow text-center p-3 bg-white">
          <h5>Total Questions</h5>
          <h3 class="text-danger fw-bold">{{ summary.totalQuestions }}</h3>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow text-center p-3 bg-white">
          <h5>Total Users</h5>
          <h3 class="text-info fw-bold">{{ summary.totalUsers }}</h3>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6 mb-4">
        <div class="card shadow-lg p-4">
          <h4 class="text-center mb-3">📊 Quizzes per Subject</h4>
          <div class="chart-wrapper">
            <canvas id="quizChart"></canvas>
          </div>
        </div>
      </div>
      <div class="col-md-6 mb-4">
        <div class="card shadow-lg p-4">
          <h4 class="text-center mb-3">📈 Quizzes per Week</h4>
          <div class="chart-wrapper">
            <canvas id="monthChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';
import { getQuizzes, getSubjects, getChapterss, getUsers, getQuestionss } from '@/services/api';

const summary = ref({
  totalUsers: 0,
  totalSubjects: 0,
  totalChapters: 0,
  totalQuestions: 0
});

onMounted(async () => {
  document.title = 'StudiQ | Insights';
  await loadSummary();
  await loadChartData();
});

const loadSummary = async () => {
  try {
    const [subjectRes, userRes, chapterRes, questionRes] = await Promise.all([getSubjects(), getUsers(), getChapterss(), getQuestionss()]);
    summary.value = {
      totalUsers: userRes?.users?.length || 0,
      totalSubjects: subjectRes?.subjects?.length || 0,
      totalChapters: chapterRes?.chapters?.length || 0,
      totalQuestions: questionRes?.questions?.length || 0 };
  } catch (error) {
    console.error('Error fetching summary data:', error);
  }
};

const loadChartData = async () => {
  try {
    const [subjectRes, chapterRes, quizRes] = await Promise.all([
      getSubjects(),
      getChapterss(),
      getQuizzes()
    ]);

    const subjects = subjectRes.subjects;
    const chapters = chapterRes.chapters;
    const quizzes = quizRes.quizzes;

    // --- Chart 1: Quizzes per Subject ---
    const quizCountBySubject = subjects.map(subject => {
      const subjectChapters = chapters.filter(chap => chap.subject_id === subject.id);
      const totalQuizzes = subjectChapters.reduce((count, chap) => {
        return count + quizzes.filter(quiz => quiz.chapter_id === chap.id).length;
      }, 0);
      return { label: subject.name, count: totalQuizzes };
    });

    const ctx1 = document.getElementById('quizChart').getContext('2d');
    new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: quizCountBySubject.map(item => item.label),
        datasets: [{
          label: 'Quizzes',
          data: quizCountBySubject.map(item => item.count),
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          barThickness: 40,
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: { display: true, text: 'Subjects', font: { weight: 'bold', size: 14 } },
            grid: { display: false }
          },
          y: {
            beginAtZero: true,
            max: Math.max(...quizCountBySubject.map(i => i.count)) + 5,
            ticks: { stepSize: 2 },
            title: { display: true, text: 'Number of Quizzes', font: { weight: 'bold', size: 14 } }
          }
        },
        plugins: { legend: { display: false } }
      }
    });

    // --- Chart 2: Quizzes per Week ---
    const getWeekRangeLabel = (dateStr) => {
      const date = new Date(dateStr);
      const day = date.getDay();
      const diffToMonday = (day + 6) % 7;
      const monday = new Date(date);
      monday.setDate(date.getDate() - diffToMonday);
      const sunday = new Date(monday);
      sunday.setDate(monday.getDate() + 6);
      const options = { month: 'short', day: 'numeric' };
      const rangeLabel = `${monday.toLocaleDateString('en-US', options)} – ${sunday.toLocaleDateString('en-US', options)}`;
      const isoWeekKey = `${monday.getFullYear()}-W${String(Math.ceil((((monday - new Date(monday.getFullYear(), 0, 1)) / 86400000) + 1) / 7)).padStart(2, '0')}`;
      return { isoWeekKey, rangeLabel };
    };

    const weeklyMap = {};
    quizzes.forEach(q => {
      if (q.date_of_quiz) {
        const { isoWeekKey, rangeLabel } = getWeekRangeLabel(q.date_of_quiz);
        if (!weeklyMap[isoWeekKey]) {
          weeklyMap[isoWeekKey] = { count: 0, label: rangeLabel };
        }
        weeklyMap[isoWeekKey].count += 1;
      }
    });

    const sortedKeys = Object.keys(weeklyMap).sort((a, b) => {
      const toDate = (key) => {
        const [year, week] = key.split('-W').map(Number);
        return new Date(year, 0, 1 + (week - 1) * 7);
      };
      return toDate(a) - toDate(b);
    });

    const labels = sortedKeys.map(k => weeklyMap[k].label);
    const dataCounts = sortedKeys.map(k => weeklyMap[k].count);

    const ctx2 = document.getElementById('monthChart').getContext('2d');
    new Chart(ctx2, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Quizzes Posted',
          data: dataCounts,
          fill: false,
          borderColor: 'rgba(75, 192, 192, 1)',
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Week Range',
              font: { weight: 'bold', size: 14 }
            },
            ticks: {
              maxRotation: 60,
              minRotation: 45
            }
          },
          y: {
            beginAtZero: true,
            max: Math.max(...dataCounts) + 2,
            ticks: { stepSize: 1 },
            title: {
              display: true,
              text: 'Posted Quizzes',
              font: { weight: 'bold', size: 14 }
            }
          }
        },
        plugins: { legend: { display: false } }
      }
    });

  } catch (error) {
    console.error('Error loading chart data:', error);
  }
};
</script>

<style scoped>
.chart-wrapper {
  height: 350px;
}
.card {
  border-radius: 16px;
  background: #f8f9fa;
}
</style>