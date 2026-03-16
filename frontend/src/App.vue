<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuth } from './composables/auth'

const authStore = useAuth()

onMounted(async () => {
  if (localStorage.getItem('accessToken')) {
    try {
      await authStore.fetchMe()
    } catch (e) {
      localStorage.removeItem('accessToken')
    }
  }
})
</script>

<template>
  <RouterView />
</template>

<style scoped></style>
