import type { PlayerCreate, PlayerSummary } from "@/types"
import api from "./axiosConfig"

export type GameResult = 'x_won' | 'o_won' | 'draw'

type GameCreate = {
  id: string
  result: GameResult
  players: PlayerCreate[]
  duration: number
}

type Game = {
  id: string
  result: GameResult
  players: PlayerSummary[]
  duration: number
}

export const createGame = async (game: GameCreate): Promise<Game> => {
  const response = await api.post<Game>('/games', game)
  return response.data
}