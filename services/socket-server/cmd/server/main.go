package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/caarlos0/env/v11"
	"github.com/joho/godotenv"

	"github.com/Jud1k/tic-tac-toe/internal/config"
	"github.com/Jud1k/tic-tac-toe/internal/hub"
	"github.com/Jud1k/tic-tac-toe/internal/integration"
	"github.com/Jud1k/tic-tac-toe/internal/ws"
)

func main() {
	if err := godotenv.Load("../.env"); err != nil {
		log.Fatal("Error loading .env file")
	}

	var config config.Config
	if err := env.Parse(&config); err != nil {
		log.Fatal("Parsing error: ", err)
	}

	gameStoreClient := integration.NewGameStoreClient(config.FastApiUrl, config.InternalServiceKey)
	hub := hub.NewHub(gameStoreClient)
	go hub.Run()
	
	server := ws.Server{Config: config, Hub: hub}
	http.HandleFunc("/api/v1/ws/game", server.HandleWs)
	fmt.Println("Listening on port 8080")

	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
