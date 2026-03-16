import api from '@/api/axiosConfig'
import { type Player, type PlayerSummary } from '@/types'
import type { GameResult } from './game'

type PlayerResponse = {
  userId: string
  username: string
  imageUrl: string
  rating: number
  wins: number
  losses: number
  draws: number
  createdAt: string
}

export type PlayerWithRank = PlayerResponse & {
  rank: number
}

export type GameDetails = {
  id: string
  result: GameResult
  duration: number
  players: [
    {
      gameId: string
      playerId: string
      side: string
      type: string
      player: PlayerSummary | null
    },
  ]
}

export const getPlayerWithRank = async (): Promise<PlayerWithRank> => {
  const response = await api.get<PlayerWithRank>('/players/me/rank')
  return response.data
}

export const getPlayer = async (): Promise<Player> => {
  const response = await api.get<Player>('/players/me')
  return response.data
}

export const updatePlayer = async (player: Partial<Player>): Promise<Player> => {
  const response = await api.patch<Player>('/players/me', player)
  return response.data
}

export const getLeaderboard = async (): Promise<PlayerWithRank[]> => {
  const response = await api.get<PlayerWithRank[]>('/players/leaderboard')
  return response.data
}

export const getRecentGames = async (): Promise<GameDetails[]> => {
  const response = await api.get<GameDetails[]>('/players/me/recent-games')
  return response.data
}
