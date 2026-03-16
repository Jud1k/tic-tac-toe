export type Player = {
  userId: string
  username: string
  rating: number
  wins: number
  losses: number
  draws: number
  imageUrl: string
  rank: number
  createdAt: string
  updatedAt: string
}

export type PlayerSummary = {
  userId: string
  username: string
  imageUrl: string
}

export type PlayerCreate = {
  gameId: string
  playerId: string | null
  side: string
  type: string
}
