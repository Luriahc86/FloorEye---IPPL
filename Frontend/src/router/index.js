import { createRouter, createWebHistory } from 'vue-router'

// Auth
const Login = () => import('@/views/Login.vue')
const Forgot = () => import('@/views/Forgot.vue')
const Register = () => import('@/views/Register.vue')

// Pages (tanpa layout)
const Dashboard = () => import('@/views/Dashboard.vue')
const KelolaStaff = () => import('@/views/KelolaStaff.vue')
const KelolaCCTV = () => import('@/views/KelolaCCTV.vue')
const Laporan = () => import('@/views/Laporan.vue')

const routes = [
  // AUTH PAGES
  { path: '/', name: 'Login', component: Login },
  { path: '/forgot-password', name: 'Forgot', component: Forgot },
  { path: '/register', name: 'Register', component: Register },

  // PAGES BIASA, TIDAK ADA LAYOUT TERBUNGKUS
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/kelola-staff', name: 'KelolaStaff', component: KelolaStaff },
  { path: '/kelola-cctv', name: 'KelolaCCTV', component: KelolaCCTV },
  { path: '/laporan', name: 'Laporan', component: Laporan },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
