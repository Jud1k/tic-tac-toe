export type PlayerSymbol = 'X' | 'O'
export type Cell = PlayerSymbol | null
export type Winner = PlayerSymbol | 'Draw'
export type GameBoard = Cell[]