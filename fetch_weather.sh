#!/bin/bash

# Replace these variables with your actual API URL and city
API_URL="http://127.0.0.1:8000/api"
CITY="kochi"

# Function to fetch weather data
fetch_weather_data() {
    curl -X GET "${API_URL}/weather/${CITY}/" -o weather_data.json
}

# Function to post weather data
post_weather_data() {
    curl -X POST "${API_URL}/weather/" -H "Content-Type: application/json" -d "{\"city\": \"${CITY}\"}"
}

# Call functions
fetch_weather_data
post_weather_data
