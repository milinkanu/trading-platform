<template>
  <div class="min-h-screen bg-gray-950 text-white font-sans">
    <Navbar />

    <main class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 space-y-8">
      <div class="flex justify-between items-end">
        <div>
          <h1 class="text-3xl font-black tracking-tight">Admin Control Panel</h1>
          <p class="text-gray-500 font-medium">Manage users and platform permissions</p>
        </div>
        <div class="bg-purple-600/10 border border-purple-500/30 px-4 py-2 rounded-xl">
           <span class="text-xs font-black text-purple-400 uppercase tracking-widest">Master Admin</span>
        </div>
      </div>

      <!-- Stats Grid -->
      <div v-if="stats" class="grid grid-cols-1 md:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="bg-gray-900 border border-gray-800 p-6 rounded-3xl space-y-2">
          <span class="text-xs font-black text-gray-500 uppercase tracking-widest">Total Users</span>
          <div class="text-4xl font-black">{{ stats.total_users }}</div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-6 rounded-3xl space-y-2">
          <span class="text-xs font-black text-purple-500 uppercase tracking-widest">Admins</span>
          <div class="text-4xl font-black text-purple-400">{{ stats.total_admins }}</div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-6 rounded-3xl space-y-2">
          <span class="text-xs font-black text-blue-500 uppercase tracking-widest">Traders</span>
          <div class="text-4xl font-black text-blue-400">{{ stats.total_traders }}</div>
        </div>
      </div>

      <!-- Users Table -->
      <div class="bg-gray-900 border border-gray-800 rounded-3xl overflow-hidden shadow-2xl">
        <div class="px-8 py-6 border-b border-gray-800 flex justify-between items-center bg-gray-900/50">
           <h3 class="font-bold text-lg">User Directory</h3>
           <button @click="fetchData" class="text-xs font-bold text-blue-500 hover:text-blue-400 transition-colors">Refresh List</button>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="text-[10px] font-black text-gray-500 uppercase tracking-widest bg-gray-950/50">
                <th class="px-8 py-4">Name & Email</th>
                <th class="px-8 py-4">Role</th>
                <th class="px-8 py-4">Joined Date</th>
                <th class="px-8 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-800">
              <tr v-if="loading" v-for="i in 3" :key="i" class="animate-pulse">
                <td colspan="4" class="px-8 py-6 h-16 bg-gray-900/50"></td>
              </tr>
              <tr v-else v-for="user in users" :key="user.id" class="hover:bg-gray-800/30 transition-colors group">
                <td class="px-8 py-5">
                  <div class="font-bold text-white">{{ user.name }}</div>
                  <div class="text-xs text-gray-500">{{ user.email }}</div>
                </td>
                <td class="px-8 py-5">
                  <span 
                    :class="user.role === 'admin' ? 'bg-purple-500/10 text-purple-400 border-purple-500/30' : 'bg-blue-500/10 text-blue-400 border-blue-500/30'"
                    class="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border"
                  >
                    {{ user.role }}
                  </span>
                </td>
                <td class="px-8 py-5 text-sm text-gray-400 font-mono">
                  {{ formatDate(user.created_at) }}
                </td>
                <td class="px-8 py-5 text-right">
                  <div class="flex justify-end items-center space-x-3">
                    <button 
                      v-if="user.id !== authStore.user?.id"
                      @click="toggleRole(user)"
                      title="Promote/Demote"
                      class="p-2 bg-gray-800 hover:bg-purple-600/20 text-gray-400 hover:text-purple-400 rounded-lg transition-all"
                    >
                      👑
                    </button>
                    <button 
                      v-if="user.id !== authStore.user?.id"
                      @click="deleteUser(user)"
                      title="Delete User"
                      class="p-2 bg-gray-800 hover:bg-red-600/20 text-gray-400 hover:text-red-400 rounded-lg transition-all"
                    >
                      🗑️
                    </button>
                    <span v-else class="text-[10px] font-black text-gray-600 uppercase italic">Your Account</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import api from '../api/axios'
import { useAuthStore } from '../store/authStore'

const authStore = useAuthStore()
const users = ref([])
const stats = ref(null)
const loading = ref(true)

const fetchData = async () => {
  loading.value = true
  try {
    const [usersRes, statsRes] = await Promise.all([
      api.get('/admin/users'),
      api.get('/admin/stats')
    ])
    users.value = usersRes.data
    stats.value = statsRes.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const toggleRole = async (user) => {
  const newRole = user.role === 'admin' ? 'trader' : 'admin'
  if (!confirm(`Are you sure you want to change ${user.name}'s role to ${newRole}?`)) return
  
  try {
    await api.patch(`/admin/users/${user.id}/role`, { role: newRole })
    await fetchData()
  } catch (err) {
    alert(err.response?.data?.detail || 'Update failed')
  }
}

const deleteUser = async (user) => {
  if (!confirm(`Permanently delete user ${user.email}? This cannot be undone.`)) return
  
  try {
    await api.delete(`/admin/users/${user.id}`)
    await fetchData()
  } catch (err) {
    alert(err.response?.data?.detail || 'Delete failed')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric'
  })
}

onMounted(fetchData)
</script>
