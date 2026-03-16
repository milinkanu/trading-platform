<template>
  <nav class="bg-gray-950 border-b border-gray-800 px-6 py-3 flex justify-between items-center sticky top-0 z-50">
    <div class="flex items-center space-x-8">
      <router-link to="/dashboard" class="flex items-center space-x-2 group">
        <span class="text-2xl">📈</span>
        <span class="text-xl font-black tracking-tighter text-white group-hover:text-blue-500 transition-colors">
          TradeAI
        </span>
      </router-link>
      
      <div class="hidden md:flex space-x-6 text-sm font-medium">
        <router-link 
          to="/dashboard" 
          class="text-gray-400 hover:text-white transition-colors whitespace-nowrap"
          active-class="text-blue-500"
        >
          Dashboard
        </router-link>
        <router-link 
          to="/sip-tracker" 
          class="text-gray-400 hover:text-white transition-colors whitespace-nowrap"
          active-class="text-blue-500"
        >
          SIP Tracker
        </router-link>
        <router-link 
          to="/risk-profile" 
          class="text-gray-400 hover:text-white transition-colors whitespace-nowrap"
          active-class="text-blue-500"
        >
          Risk Profile
        </router-link>
        <router-link 
          v-if="isAdmin" 
          to="/admin" 
          class="text-gray-400 hover:text-white transition-colors whitespace-nowrap"
          active-class="text-purple-500"
        >
          Admin Panel
        </router-link>
      </div>
    </div>

    <div class="flex items-center space-x-4">
      <div class="flex items-center space-x-3 pr-4 border-r border-gray-800">
        <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-xs font-bold text-white uppercase shadow-lg shadow-blue-500/20">
          {{ initials }}
        </div>
        <div class="hidden sm:block leading-tight">
          <p class="text-sm font-bold text-white">{{ authStore.userName }}</p>
          <span 
            :class="roleBadgeClass"
            class="text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider border"
          >
            {{ authStore.user?.role }}
          </span>
        </div>
      </div>
      
      <button 
        @click="handleLogout"
        class="text-sm font-bold text-gray-400 hover:text-red-500 transition-colors"
      >
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/authStore'

const router = useRouter()
const authStore = useAuthStore()

const isAdmin = computed(() => authStore.isAdmin)

const initials = computed(() => {
  const name = authStore.userName || 'U'
  return name.charAt(0).toUpperCase()
})

const roleBadgeClass = computed(() => {
  return authStore.isAdmin 
    ? 'bg-purple-500/10 text-purple-400 border-purple-500/30' 
    : 'bg-blue-500/10 text-blue-400 border-blue-500/30'
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
