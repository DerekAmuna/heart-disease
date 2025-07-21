package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	"heart-disease/backend/data"
)

func main() {
	heartData, err := data.LoadHeartData("data/heart_processed.csv")
	if err != nil {
		log.Fatalf("Failed to load heart data: %v", err)
	}

	trendsData, err := data.LoadTrendsData("data/trends.csv")
	if err != nil {
		log.Fatalf("Failed to load trends data: %v", err)
	}

	http.HandleFunc("/api/heart-data", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(heartData); err != nil {
			http.Error(w, "Failed to encode data", http.StatusInternalServerError)
		}
	})

	http.HandleFunc("/api/trends-data", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(trendsData); err != nil {
			http.Error(w, "Failed to encode data", http.StatusInternalServerError)
		}
	})

	fs := http.FileServer(http.Dir("./public"))
	http.Handle("/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, err := os.Stat("./public" + r.URL.Path)
		if os.IsNotExist(err) {
			http.ServeFile(w, r, "./public/index.html")
			return
		}
		fs.ServeHTTP(w, r)
	}))

	log.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Could not start server: %v", err)
	}
}
