<script lang="ts" setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useMatchmaking, GameStatus } from '@/composables/useMatchmaking'
import { useTicTacToe } from '@/composables/useTicTacToe'
import GameBoard from './GameBoard.vue'

const { board, currentPlayer, result, makeMove, reset } = useTicTacToe()
const { game, error, searchGame } = useMatchmaking()

const startTime = Date.now()
const now = ref<number>(Date.now())

let timerInterval: ReturnType<typeof setInterval>

const totalSeconds = computed(() => {
  return Math.floor((now.value - startTime) / 1000)
})

const formattedTime = computed(() => {
  const mins = Math.floor(totalSeconds.value / 60)
  const secs = totalSeconds.value % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
})

onMounted(() => {
  timerInterval = setInterval(() => {
    now.value = Date.now()
  }, 1000)
})

onUnmounted(() => {
  clearInterval(timerInterval)
})
</script>

<template>
  <div class="">
    <div v-if="game === null || game?.status==GameStatus.Waiting" class="flex items-center justify-center">
      <span>
        {{ formattedTime }}
      </span>
    </div>
    <GameBoard
      v-else
      :board="board"
      :current-player="currentPlayer"
      :winner="result.winner"
      :winning-line="result.winningLine"
      :disabled="false"
      :status-message="'Hello'"
      @cell-click="makeMove"
      @reset="reset"
    />
  </div>
</template>
