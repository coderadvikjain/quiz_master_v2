<template>
  <div class="container admin-dashboard">
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <br /><br />
    <div class="row">
      <div v-for="quiz in quizzes" :key="quiz.id" class="col-md-6 mb-4">
        <div class="subject-box rounded border shadow p-4 bg-white">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="mb-0 text-primary">
              {{ chapterName }} {{ quiz.remarks || 'No Remark' }}
            </h5>
          </div>
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light" style="position: sticky; top: 0; z-index: 2; background-color: white;">
              <tr>
                <th>Statement</th>
                <th class="text-end">Action</th>
              </tr>
            </thead>
          </table>
          <div style="max-height: 120px; overflow-y: auto;" class="scroll-chapter-body border-top">
            <table class="table table-hover align-middle mb-0">
              <tbody>
                <tr v-if="!quiz.questions || !quiz.questions.length">
                  <td colspan="2" class="text-center text-muted">No question(s) available yet!</td>
                </tr>
                <tr v-for="question in quiz.questions" :key="question.id" :title="question.question_statement">
                  <td>{{ getTruncatedStatement(question.question_statement) }}</td>
                    <td class="text-end">
                        <a href="/admin/quizzes" class="btn btn-sm btn-outline-warning me-2"  title="View Question">
                        <i class="bi bi-eye"></i>
                        </a>
                    </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getChapterss, getQuizzesbyChapter, getQuestions } from '@/services/api.js';

export default {
  name: 'ChapterQuizzesView',
  data() {
    return {
      quizzes: [],
      questions: {},
      chapterName: '',
      loading: true,
    };
  },

  async mounted() {
    await this.fetchChapterQuizzes();
    document.title = `StudiQ | Dashboard of ${this.chapterName} Quizzes`;
  },

  methods: {
    async fetchChapterQuizzes() {
      const chapterId = this.$route.params.chapterId;
      try {
        const chapterRes = await getChapterss();
        const chapterList = chapterRes.chapters || [];
        const chapter = chapterList.find(c => c.id === parseInt(chapterId));

        if (chapter && chapter.name) {
          this.chapterName = chapter.name.charAt(0).toUpperCase() + chapter.name.slice(1);
        } else {
          this.chapterName = `Chapter ${chapterId}`;
        }

        const response = await getQuizzesbyChapter(chapterId);
        const quizzes = response.quizzes || [];

        for (const quiz of quizzes) {
          const qRes = await getQuestions(quiz.id);
          quiz.questions = qRes.questions || [];
        }

        this.quizzes = quizzes;
      } catch (error) {
        console.error('Failed to load quizzes or questions:', error);
      } finally {
        this.loading = false;
      }
    },

    getTruncatedStatement(statement) {
      if (typeof statement !== 'string') return '';
      const truncated = statement.length > 50 ? statement.slice(0, 50) + '...' : statement;
      return truncated.charAt(0).toUpperCase() + truncated.slice(1);
    }
  }
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
.scroll-chapter-body::-webkit-scrollbar {
  width: 6px;
}
.scroll-chapter-body::-webkit-scrollbar-thumb {
  background: #dee2e6;
  border-radius: 4px;
}
</style>