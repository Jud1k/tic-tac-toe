import type { GameBoard, Cell } from '@/components/Game/types'
import { ref } from 'vue'

export enum GameStatus {
  Waiting = 'WAITING',
  Playing = 'PLAYING',
  Finished = 'FINISHED',
}

type Game = {
  gameId: string | null
  playerXId: string | null
  playerOId: string | null
  status: GameStatus
  board: GameBoard | null
  currentTurn: Cell | null
  createdAt: Date | null
  finishedAt: Date | null
}

const token = localStorage.getItem('access_token')
const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/game?token=${token}`)

export const useMatchmaking = () => {
  const game = ref<Game | null>(null)
  const error = ref<string | null>(null)

  const sendGameState = (gameState: Game) => {
    ws.send(JSON.stringify(gameState))
  }

  const searchGame = () => {
    const newGame: Game = {
      gameId: null,
      playerXId: null,
      playerOId: null,
      status: GameStatus.Waiting,
      board: null,
      currentTurn: null,
      createdAt: null,
      finishedAt: null,
    }
    game.value = newGame
    sendGameState(newGame)
  }

  ws.onerror = (ev) => {
    error.value = null
  }

  ws.onmessage = (ev) => {
    console.log(ev.data)
    game.value = ev.data
  }

  return { game, error, searchGame }
}
