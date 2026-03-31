package matchmaking

import (
	"encoding/json"
	"log"
	"time"

	"github.com/Jud1k/tic-tac-toe/internal/client"
	"github.com/Jud1k/tic-tac-toe/internal/dto"
	"github.com/google/uuid"
)

var lines = [][]int{
  {0, 1, 2},
  {3, 4, 5},
  {6, 7, 8},
  {0, 3, 6},
  {1, 4, 7},
  {2, 5, 8},
  {0, 4, 8},
  {2, 4, 6},
}

type Game struct {
	Id string `json:"gameId"`
	Players []*client.Client
	PlayerSide map[*client.Client]string
	Board [9]string
	Turn string
	Status string
	Winner string
	StartTime time.Time
}

func NewGame(player1, player2 *client.Client) *Game {
	return &Game{
		Id: uuid.New().String(),
		Players: []*client.Client{player1, player2},
		PlayerSide: map[*client.Client]string{
			player1: "X",
			player2: "O",
		},
		Board: [9]string{"", "", "", "", "", "", "", "", ""},
		Status: "playing",
		Turn: "X",
		StartTime: time.Now(),
	}
}

func (g *Game) send(client *client.Client, data interface{}) {
	bytes,err := json.Marshal(data)
	if err != nil {
		log.Println(err)
		return
	}
	client.Send <- bytes
}

func (g *Game) broadcast(data interface{}) {
	for _, player := range g.Players {
		g.send(player,data)
	}
}

func (g *Game) broadcastState() {
	msg:= dto.GameState{
		Type: "gameState",
		Payload: dto.GameStatePayload{
			Board: g.Board[:],
			Turn: g.Turn,
		},
	}
	g.broadcast(msg)
}

func (g *Game) broadcastGameOver(winner string, winningLine []int) {
	msg := dto.GameOver{
		Type: "gameOver",
		Payload: dto.GameOverPayload{
			Winner: winner,
			WinningLine: winningLine,
		},
	}
	g.broadcast(msg)
}

func (g *Game) Start() {
	playerX := g.Players[0]
	playerY := g.Players[1]

	msgX := dto.GameStarted{
		Type: "gameStarted",
		Payload: dto.GameStartedPayload{
			GameID: g.Id,
			YourSide: "X",
			OpponentId: playerY.UserId,
			Turn: g.Turn,
		},
	}

	msgO := dto.GameStarted{
		Type: "gameStarted",
		Payload: dto.GameStartedPayload{
			GameID: g.Id,
			YourSide: "O",
			OpponentId: playerX.UserId,
			Turn: g.Turn,
		},
	}

	g.send(playerX,msgX)
	g.send(playerY,msgO)

	// g.broadcastState()
}

func (g *Game) HandleMove(player *client.Client, index int) {
	if g.Status != "playing" || g.Board[index] != "" || index < 0 || index > 8 {
		return
	}

	symbol := g.PlayerSide[player]
	if g.Turn != symbol {
		return
	}

	g.Board[index] = symbol
	isWin, winner, winningLine := g.checkWinner()
	if isWin {
		g.Status = "finished"
		g.Winner = winner
		g.broadcastState()
		g.broadcastGameOver(winner, winningLine)
		return
	}

    isDraw := true
    for _, v := range g.Board {
        if v == "" { isDraw = false; break }
    }
    if isDraw {
        g.Status = "finished"
		g.Winner = winner
		g.broadcastState()
        g.broadcastGameOver("draw", nil)
        return
	}

	if g.Turn == "X" { g.Turn = "O" } else { g.Turn = "X" }
	g.broadcastState()
}

func (g *Game) checkWinner() (bool,string,[]int) {
	for _, line := range lines {
		var a, b, c int
		a = line[0]
		b = line[1]
		c = line[2]
		s := g.Board[a]
		if s != "" && s == g.Board[b] && s == g.Board[c] {
			return true,s,line
		}
	}
	return false,"",nil
}