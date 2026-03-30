package hub

import (
	"encoding/json"
	"log"

	"github.com/Jud1k/tic-tac-toe/internal/client"
	"github.com/Jud1k/tic-tac-toe/internal/dto"
	"github.com/Jud1k/tic-tac-toe/internal/integration"
	"github.com/Jud1k/tic-tac-toe/internal/matchmaking"
)


type Hub struct {
	Clients map[*client.Client]bool
	Register chan *client.Client
	Unregister chan *client.Client
	Incoming chan client.Message
	WaitingQueue  []*client.Client
	ClientGames map[*client.Client]*matchmaking.Game

	GameStoreClient *integration.GameStoreClient
}

func NewHub(gameStoreClient *integration.GameStoreClient) *Hub {
	return &Hub{
		Clients:       make(map[*client.Client]bool),
		Register:      make(chan *client.Client),
		Unregister:    make(chan *client.Client),
		Incoming: make(chan client.Message),
		WaitingQueue:  []*client.Client{},
		ClientGames:   make(map[*client.Client]*matchmaking.Game),
		GameStoreClient: gameStoreClient,
	}
}

func (h *Hub) handleMessage(message client.Message) {
	var base struct {
		Type string `json:"type"`
	}
	err := json.Unmarshal(message.Data, &base)
	if err != nil {
		log.Println("Error unmarshalling message: ", err)
		return
	}
	switch base.Type {
	case "joinQueue":
		h.addToWaitingQueue(message.Client)
	case "makeMove":
		game := h.ClientGames[message.Client]
		if game == nil {
			log.Println("No game found for client")
			return
		}
		var request dto.MakeMoveRequest
		err := json.Unmarshal(message.Data, &request)
		if err != nil {
			log.Println("Error unmarshalling message: ", err)
			return
		}
		game.HandleMove(message.Client, request.Payload.Index)
		if game.Status == "finished" {
			go func (){
				err := h.GameStoreClient.SaveGame(*game)
				if err != nil {
					log.Println(err)
				}
			}()
			for _, player := range game.Players {
				delete(h.ClientGames, player)
			}
		}
	case "leaveQueue":
		h.removeFromWaitingQueue(message.Client)
		log.Printf("User %s left from waiting queue", message.Client.UserId)
	default:
		log.Println("Unknown message type: ", base.Type)
	}

}	

func (h *Hub) Run() {
	for {
		select {
		case client := <-h.Register:
			h.Clients[client] = true
		case client := <-h.Unregister:
			if _, ok := h.Clients[client]; ok {
				delete(h.Clients, client)
				h.removeFromWaitingQueue(client)
				close(client.Send)
			}
		case msg := <-h.Incoming:
			log.Println(string(msg.Data))
			h.handleMessage(msg)
		}
	}
}

func(h *Hub) addToWaitingQueue(client *client.Client){
	h.WaitingQueue = append(h.WaitingQueue, client)

	msg := dto.SearchingOpponent{
		Type: "searchingOpponent",
	}
	bytes,err := json.Marshal(msg)
	if err != nil {
		log.Println(err)
		return
	}
	client.Send <- bytes
	log.Println(len(h.WaitingQueue))
	if len(h.WaitingQueue) >= 2 {
		player1, player2 := h.WaitingQueue[0], h.WaitingQueue[1]
		if player1.UserId == player2.UserId {
			h.WaitingQueue = h.WaitingQueue[1:]
			return
		}
		h.WaitingQueue = h.WaitingQueue[2:]

		game := matchmaking.NewGame(player1, player2)
		log.Println("Game created: ", game.Id)
		h.ClientGames[player1] = game
		h.ClientGames[player2] = game

		game.Start()
	}
}

func (h *Hub) removeFromWaitingQueue(client *client.Client) {
	for i, waitingClient := range h.WaitingQueue {
		if waitingClient == client {
			h.WaitingQueue = append(h.WaitingQueue[:i], h.WaitingQueue[i+1:]...)
			log.Printf("User %s left from waiting queue", client.UserId)
			return
		}
	}
}