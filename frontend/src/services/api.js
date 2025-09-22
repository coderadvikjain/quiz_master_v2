import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use((response) => {
    if (response.config.responseType === 'blob') {
      return response;
    }
    return response.data;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_role');
      window.location.replace('/SignIn');
    }
    return Promise.reject(error);
  }
);

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// -------- AUTH --------
export const register = (data) => api.post('/auth/register', data);
export const login = (data) => api.post('/auth/login', data);

// -------- ADMIN ROUTES --------
// Users
export const getUsers = () => api.get('/admin/users');

// Subjects
export const getSubjects = () => api.get('/admin/subjects');
export const addSubject = (data) => api.post('/admin/subject', data);
export const updateSubject = (id, data) => api.put(`/admin/subject/${id}`, data);
export const deleteSubject = (id) => api.delete(`/admin/subject/${id}`);

// Chapters
export const getChapterss = () => api.get(`/admin/chapters`);
export const getChapters = (subjectId) => api.get(`/admin/chapters/${subjectId}`);
export const addChapter = (data) => api.post('/admin/chapter', data);
export const updateChapter = (id, data) => api.put(`/admin/chapter/${id}`, data);
export const deleteChapter = (id) => api.delete(`/admin/chapter/${id}`);

// Quizzes
export const getQuizzes = () => api.get(`/admin/quizzes`);
export const getQuizzesbyChapter = (chapterId) => api.get(`/admin/quizzes/${chapterId}`);
export const addQuiz = (data) => api.post('/admin/quiz', data);
export const updateQuiz = (id, data) => api.put(`/admin/quiz/${id}`, data);
export const deleteQuiz = (id) => api.delete(`/admin/quiz/${id}`);

// Questions
export const getQuestionss = () => api.get(`/admin/questions`);
export const getQuestions = (quizId) => api.get(`/admin/questions/${quizId}`);
export const addQuestion = (data) => api.post('/admin/question', data);
export const updateQuestion = (id, data) => api.put(`/admin/question/${id}`, data);
export const deleteQuestion = (id) => api.delete(`/admin/question/${id}`);

// -------- USER ROUTES --------
export const getUserinfo = () => api.get('/user/info');
export const getUserDashboard = () => api.get('/user/dashboard');
export const getQuizQuestion = (quizId, progress = 0) => api.get(`/user/attempt_quiz/${quizId}?progress=${progress}`);
export const submitAnswer = (data) => api.post('/user/submit_answer', data);
export const saveQuizResult = (data) => api.post('/user/quiz_result', data);
export const getUserScores = () => api.get('/user/scores');
export const exportcsv = () => api.post('/user/export_quiz');
export const checkExportStatus = (taskId) => api.get(`/user/check_export_status/${taskId}`);
export const downloadExportedCSV = (filename) => api.get(`/user/downloads/${filename}`, {
  responseType: 'blob'
});

export default api;