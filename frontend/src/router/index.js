import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { path: '/', redirect: '/SignIn' },
  { path: '/SignIn', component: () => import('@/views/Login.vue'),meta: { hideLayout: true } },
  { path: '/SignUp', component: () => import('@/views/Register.vue'),meta: { hideLayout: true } },
  {
    path: '/admin/dashboard',
    component: () => import('@/views/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
  path: '/quizzes/:chapterId',
  component: () => import('@/views/ChapterQuizzesView.vue'),
  meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/quizzes',
    component: () => import('@/views/QuizManagement.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/accounts',
    component: () => import('@/views/ManageUsers.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/insights',
    component: () => import('@/views/AdminSummary.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/dashboard',
    component: () => import('@/views/UserDashboard.vue'),
    meta: { requiresAuth: true, requiresUser: true },
  },
  {
    path: '/grades',
    component: () => import('@/views/UserScores.vue'),
    meta: { requiresAuth: true, requiresUser: true },
  },
  {
    path: '/insights',
    component: () => import('@/views/UserSummary.vue'),
    meta: { requiresAuth: true, requiresUser: true },
  },
  { path: '/:pathMatch(.*)*', component: () => import('@/views/PageNotFound.vue'),meta: { hideLayout: true }}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const userRole = localStorage.getItem('user_role');

  if (to.meta.requiresAuth && !token) {
    const cameFromOutside = from.name === null;

    if (cameFromOutside) {
      const redirectPath = to.fullPath !== '/dashboard' ? to.fullPath : '/dashboard';
      return next(`/SignIn?redirect=${encodeURIComponent(redirectPath)}`);
    }

    return next('/SignIn');
  }

  if (to.meta.requiresAuth && !token) {
    return next('/SignIn');
  }

  if (to.meta.requiresAdmin && userRole !== 'admin') {
    return next('/dashboard');
  }

  if (to.meta.requiresUser && userRole === 'admin') {
    return next('/admin/dashboard');
  }
  next();
});
export default router;