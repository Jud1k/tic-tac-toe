import type { GameResult } from '@/api/game'

export const getWinnerText = (gameResult: GameResult): string => {
  switch (gameResult) {
    case 'x_won':
      return 'X Won!'
    case 'o_won':
      return 'O Won'
    case 'draw':
      return 'Draw'
    default:
      return 'Impossible'
  }
}
