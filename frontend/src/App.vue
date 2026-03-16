<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <router-view></router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './store/authStore'

const authStore = useAuthStore()

onMounted(() => {
  authStore.initFromStorage()
})
</script>
