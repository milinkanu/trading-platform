import { defineStore } from 'pinia'
import api from '../api/axios'
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin',
    isTrader: (state) => state.user?.role === 'trader' || state.user?.role === 'admin',
    userName: (state) => state.user?.name || state.user?.email?.split('@')[0] || ''
  },
  actions: {
    async login(email, password) {
      const response = await api.post('/auth/login', { email, password })
      this.token = response.data.access_token
      this.user = response.data.user
      localStorage.setItem('token', this.token)
    },
    async register(name, email, password) {
      const response = await api.post('/auth/register', { name, email, password })
      this.token = response.data.access_token
      try {
          const decoded = jwtDecode(this.token)
          this.user = {
              name: name,
              email: decoded.email,
              role: decoded.role
          }
      } catch (err) {
          console.error(err)
      }
      localStorage.setItem('token', this.token)
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    },
    initFromStorage() {
      const storedToken = localStorage.getItem('token')
      if (storedToken) {
        this.token = storedToken
        try {
          const decoded = jwtDecode(storedToken)
          // Just parsing what we need from standard JWT token logic from backend
          this.user = {
            id: decoded.user_id,
            email: decoded.email,
            role: decoded.role,
            name: decoded.name || decoded.email.split('@')[0]
          }
        } catch (e) {
          this.logout()
        }
      }
    }
  }
})
