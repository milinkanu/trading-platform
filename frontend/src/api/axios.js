import axios from 'axios'
import router from '../router'
import { useAuthStore } from '../store/authStore'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://127.0.0.1:8001' : '/api'),
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

api.interceptors.response.use(response => {
  return response
}, error => {
  if (error.response && error.response.status === 401) {
    const authStore = useAuthStore()
    authStore.logout()
    router.push('/login')
  }
  return Promise.reject(error)
})

export default api
