<script setup lang="ts">
import AppLayout from '@/layouts/AppLayout.vue'
import { Card, CardTitle, CardContent, CardDescription, CardHeader } from '@/components/Card'
import { PlayIcon, UserIcon, ClipboardDocumentListIcon, TrophyIcon } from '@heroicons/vue/24/solid'
import { useAuth } from '@/composables/auth'
import { useAuthModal } from '@/composables/useAuthModal'
import { useRouter } from 'vue-router'
import { useMatchmaking } from '@/composables/useMatchmaking'
import Leaderboard from '@/components/Leaderboard.vue'
import { onMounted, ref } from 'vue'
import { getLeaderboard } from '@/api/player'
import type { Player } from '@/types'
import Spinner from '@/components/Spinner.vue'

const topPlayers = ref<Player[]>([])
const isLoading = ref<boolean>(false)

const { searchGame } = useMatchmaking()
const authStore = useAuth()

const router = useRouter()
const { openAuthModal } = useAuthModal()

const startGame = (mode: 'pvp' | 'pve') => {
  router.push({
    path: 'game',
    query: { mode },
  })
  searchGame()
}

const fetchLeaderboard = async () => {
  isLoading.value = true
  try {
    topPlayers.value = await getLeaderboard()
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  await fetchLeaderboard()
})
</script>

<template>
  <AppLayout>
    <div class="container px-2 py-8">
      <div class="max-w-6xl space-y-8">
        <div class="text-center space-y-4">
          <h1 class="text-5xl font-bold">Tic Tac Toe Arena</h1>
          <p class="text-lg text-gray-400">Challenge yourself and compete for the top spot!</p>
        </div>

        <div class="grid grid-cols-2 gap-5 mx-auto w-max">
          <button
            class="cursor-pointer text-white bg-violet-400 w-full rounded-md text-lg px-8 py-3 flex items-center gap-3 justify-center"
            @click="startGame('pvp')"
          >
            <PlayIcon class="w-6 h-6" />
            Play against people
          </button>
          <button
            class="cursor-pointer text-white bg-violet-400 w-full rounded-md text-lg px-8 py-3 flex items-center gap-3 justify-center"
            @click="startGame('pve')"
          >
            <PlayIcon class="w-6 h-6" />
            Play against AI
          </button>
        </div>

        <div class="grid md:grid-cols-2 gap-12">
          <Card v-if="authStore.isLoggedIn">
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <ClipboardDocumentListIcon class="w-6 h-6" />
                Your Stats
              </CardTitle>
              <CardDescription><p class="text-gray-400">Track your performance</p></CardDescription>
            </CardHeader>
            <CardContent>
              <div class="space-y-4">
                <div class="grid grid-cols-3 gap-4">
                  <div class="text-center p-4 rounded-lg bg-green-200">
                    <p class="text-3xl font-bold text-green-500">0</p>
                    <p class="text-sm text-gray-600">Wins</p>
                  </div>
                  <div class="text-center p-4 rounded-lg bg-red-200">
                    <p class="text-3xl font-bold text-red-500">0</p>
                    <p class="text-sm text-gray-600">Losses</p>
                  </div>
                  <div class="text-center p-4 rounded-lg bg-blue-200">
                    <p class="text-3xl font-bold text-blue-500">0</p>
                    <p class="text-sm text-gray-600">Draws</p>
                  </div>
                </div>
                <div class="text-center p-4 rounded-lg bg-violet-400">
                  <p class="text-2xl font-bold text-white">0</p>
                  <p class="text-sm text-gray-600">Win Rate</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card v-else>
            <CardHeader>
              <CardTitle class="flex items-center gap-2">
                <UserIcon class="w-6 h-6" />
                <h3 class="font-semibold">Create an Account</h3>
              </CardTitle>
              <CardDescription>Track your stats and compete!</CardDescription>
            </CardHeader>
            <CardContent class="space-y-4">
              <p class="text-gray-400">
                Sign up to save your progress, track your wins, and climb the leaderboard!
              </p>
              <button
                class="cursor-pointer text-white w-full py-2 rounded-md items-center bg-violet-400 justify-center"
                @click="openAuthModal('signup')"
              >
                Get Started
              </button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle class="flex items-center gap-2 font-semibold">
                <TrophyIcon class="w-6 h-6 text-yellow-400" />Leaderboard</CardTitle
              >
            </CardHeader>
            <CardContent>
              <div v-if="isLoading" class="flex justify-center items-center py-8">
                <Spinner size="sm"/>
              </div>
              <p v-else-if="topPlayers.length == 0" class="text-gray-400 text-center py-8">
                Leaderboard content will be displayed here
              </p>
              <Leaderboard v-else :players="topPlayers" />
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>How to Play</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="grid md:grid-cols-3 gap-6 text-center">
              <div class="space-y-2">
                <div
                  class="w-12 h-12 bg-blue-200 rounded-full flex items-center justify-center mx-auto"
                >
                  <span class="text-2xl font-bold text-blue-400">1</span>
                </div>
                <h3 class="font-semibold">Choose Your Side</h3>
                <p class="text-sm text-gray-400">Play as X or O against the computer</p>
              </div>
              <div class="space-y-2">
                <div
                  class="w-12 h-12 bg-blue-200 rounded-full flex items-center justify-center mx-auto"
                >
                  <span class="text-2xl font-bold text-blue-400">2</span>
                </div>
                <h3 class="font-semibold">Make Your Move</h3>
                <p class="text-sm text-gray-400">Click on any empty cell to place your mark</p>
              </div>
              <div class="space-y-2">
                <div
                  class="w-12 h-12 bg-blue-200 rounded-full flex items-center justify-center mx-auto"
                >
                  <span class="text-2xl font-bold text-blue-400">3</span>
                </div>
                <h3 class="font-semibold">Win the Game</h3>
                <p class="text-sm text-gray-400">
                  Get three in a row horizontally, vertically, or diagonally
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </AppLayout>
</template>
