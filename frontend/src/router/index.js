import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/authStore'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import ChartView from '../views/ChartView.vue'
import AdminView from '../views/AdminView.vue'
import RiskProfileView from '../views/RiskProfileView.vue'
import SIPTrackerView from '../views/SIPTrackerView.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: LoginView },
  { 
    path: '/dashboard', 
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/chart/:symbol',
    component: ChartView,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    component: AdminView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/risk-profile',
    component: RiskProfileView
  },
  {
    path: '/sip-tracker',
    component: SIPTrackerView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize from storage if not already
  if (!authStore.token) {
    authStore.initFromStorage()
  }

  const isLoggedIn = !!authStore.token
  const isAdmin = authStore.user?.role === 'admin'

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.meta.requiresAdmin && !isAdmin) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
