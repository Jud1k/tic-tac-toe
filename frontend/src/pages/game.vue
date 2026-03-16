<script lang="ts" setup>
import GameVsAI from '@/components/Game/GameVsAI.vue'
import GameVsPlayer from '@/components/Game/GameVsPlayer.vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

type GameMode = 'pve' | 'pvp'

const route = useRoute()

const mode = computed<GameMode>(() => {
  const m = route.query.mode
  return m === 'pvp' || m === 'pve' ? m : 'pve'
})
</script>

<template>
  <AppLayout>
    <div class="container">
      <GameVsAI v-if="mode == 'pve'" />
      <GameVsPlayer v-else />
    </div>
  </AppLayout>
</template>
