package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
	"io"
	"log"
	"net/http"
	"os"
)

func callRaccoonAPI(w http.ResponseWriter, r *http.Request) {
	err := godotenv.Load()
	if err != nil {
		http.Error(w, "Error loading .env file", http.StatusInternalServerError)
		return
	}

	secretKey := os.Getenv("RACCOON_SECRET_KEY")
	raccoonPasscode := r.Header.Get("raccoon-passcode")

	if raccoonPasscode == "" {
		http.Error(w, "Missing 'raccoon-passcode' header", http.StatusBadRequest)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Failed to read request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()

	var requestBody map[string]interface{}
	err = json.Unmarshal(body, &requestBody)
	if err != nil {
		http.Error(w, "Invalid JSON request body", http.StatusBadRequest)
		return
	}

	stream, _ := requestBody["stream"].(bool)

	vars := mux.Vars(r)
	appName := vars["app_name"]
	if appName == "" {
		http.Error(w, "Missing 'app_name' in path parameter", http.StatusBadRequest)
		return
	}

	upstreamURL := fmt.Sprintf("https://api.flyingraccoon.tech/lam/%s/run", appName)

	client := &http.Client{}
	req, err := http.NewRequest("POST", upstreamURL, bytes.NewBuffer(body))
	if err != nil {
		http.Error(w, "Failed to create request", http.StatusInternalServerError)
		return
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("raccoon-passcode", raccoonPasscode)
	req.Header.Set("secret-key", secretKey)

	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	if stream {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(resp.StatusCode)
		_, err := io.Copy(w, resp.Body) // Stream the response body
		if err != nil {
			log.Println("Error streaming response:", err)
		}
	} else {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(resp.StatusCode)
		respBody, err := io.ReadAll(resp.Body)
		if err != nil {
			http.Error(w, "Failed to read response body", http.StatusInternalServerError)
			return
		}
		w.Write(respBody)
	}
}

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/lam/{app_name}/run", callRaccoonAPI).Methods("POST")
	fmt.Println("Go server running on http://localhost:3800")
	log.Fatal(http.ListenAndServe(":3800", r))
}
