<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 border-gray-800">
    <div class="bg-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-md border border-gray-700">
      <h2 class="text-3xl font-bold mb-6 text-center text-blue-400">
        {{ isLogin ? 'Sign In' : 'Create Account' }}
      </h2>
      
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div v-if="!isLogin">
          <label class="block text-sm font-medium text-gray-400 mb-1">Name</label>
          <input 
            v-model="form.name" 
            type="text" 
            required 
            class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
            placeholder="John Doe"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-400 mb-1">Email</label>
          <input 
            v-model="form.email" 
            type="email" 
            required 
            class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
            placeholder="john@example.com"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-400 mb-1">Password</label>
          <input 
            v-model="form.password" 
            type="password" 
            required 
            class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
            placeholder="••••••••"
          />
        </div>

        <div v-if="errorMsg" class="p-3 bg-red-900/50 border border-red-500 text-red-200 rounded-lg text-sm text-center">
          {{ errorMsg }}
        </div>

        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition duration-200 disabled:opacity-50"
        >
          <span v-if="isLoading">Processing...</span>
          <span v-else>{{ isLogin ? 'Login' : 'Register' }}</span>
        </button>
      </form>
      
      <div class="mt-6 text-center text-gray-400">
        <button @click="toggleMode" class="hover:text-white transition">
          {{ isLogin ? "Don't have an account? Register" : 'Already have an account? Login' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/authStore'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const isLoading = ref(false)
const errorMsg = ref('')

const form = reactive({
  name: '',
  email: '',
  password: ''
})

const toggleMode = () => {
  isLogin.value = !isLogin.value
  errorMsg.value = ''
}

const handleSubmit = async () => {
  errorMsg.value = ''
  isLoading.value = true
  
  try {
    if (isLogin.value) {
      await authStore.login(form.email, form.password)
    } else {
      await authStore.register(form.name, form.email, form.password)
    }
    router.push('/dashboard')
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      errorMsg.value = error.response.data.detail
    } else if (error.message) {
      errorMsg.value = error.message
    } else {
      errorMsg.value = 'An error occurred. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
