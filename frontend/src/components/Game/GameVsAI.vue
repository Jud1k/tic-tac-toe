<script lang="ts" setup>
import { computed, onMounted, ref, watch } from 'vue'
import GameBoard from './GameBoard.vue'
import { useTicTacToe } from '@/composables/useTicTacToe'
import { getAIMove, randomPlayerSymbol } from './utils'
import type { PlayerSymbol } from './types'
import { createGame } from '@/api/game'
import { useAuth } from '@/composables/auth'
import { uuidv7 } from 'uuidv7'

const playerSymbol = ref<PlayerSymbol>(randomPlayerSymbol())
const aiSymbol = computed(() => (playerSymbol.value === 'X' ? 'O' : 'X'))

const { userId } = useAuth()

const { board, currentPlayer, durationInSeconds, result, makeMove, reset } = useTicTacToe()

const handleCellClick = (index: number) => {
  if (currentPlayer.value !== playerSymbol.value) return
  makeMove(index)
}

watch(currentPlayer, (player) => {
  if (player !== aiSymbol.value) return
  if (result.value.winner) return

  setTimeout(() => {
    const aiMove = getAIMove(board.value, aiSymbol.value, playerSymbol.value)
    if (aiMove !== null) {
      makeMove(aiMove)
    }
  }, 500)
})

watch(
  () => result.value.winner,
  async (winner) => {
    if (!winner) return
    const gameResult = winner === 'Draw' ? 'draw' : winner === 'X' ? 'x_won' : 'o_won'
    const isPlayerX = playerSymbol.value === 'X'
    const gameId = uuidv7()
    try {
      await createGame({
        id: gameId,
        result: gameResult,
        duration: durationInSeconds.value,
        players: [
          {
            gameId: gameId,
            playerId: userId,
            side: isPlayerX ? 'X' : 'O',
            type: 'human',
          },
          {
            gameId: gameId,
            playerId: null,
            side: isPlayerX ? 'O' : 'X',
            type: 'ai',
          },
        ],
      })
      console.log('Game saved successfully')
    } catch (error) {
      console.error('Failed to save game:', error)
    }
  },
)

const resetGame = () => {
  const newPlayerSymbol = randomPlayerSymbol()
  playerSymbol.value = newPlayerSymbol
  reset(newPlayerSymbol)
}

const statusMessage = computed(() => {
  if (!result.value.winner)
    return currentPlayer.value !== aiSymbol.value
      ? `Your turn (${currentPlayer.value})`
      : `AI turn... (${currentPlayer.value})`
  if (result.value.winner === 'Draw') return 'Draw'
  return result.value.winner === playerSymbol.value ? 'You win! 🎉' : 'AI win!'
})

onMounted(() => {
  reset(playerSymbol.value)
})
</script>

<template>
  <GameBoard
    :board="board"
    :current-player="currentPlayer"
    :disabled="currentPlayer === aiSymbol"
    :winner="result.winner"
    :winning-line="result.winningLine"
    :status-message="statusMessage"
    @cell-click="handleCellClick"
    @reset="resetGame"
  />
</template>
