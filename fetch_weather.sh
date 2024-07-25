#!/bin/bash

# Define the API endpoint of your FastAPI application for posting weather data
FASTAPI_ENDPOINT="http://localhost:8000/weather/"

# Define the OpenWeatherMap API endpoint template
API_TEMPLATE="http://api.openweathermap.org/data/2.5/weather?q={city}&appid=ac5559a726f0d448e4c774c8fa2c6655&units=metric"
LOG_FILE="/mnt/c/Users/HP/Downloads/Internship_Project-main/weather_data/fetch_weather_data.log"


# Prompt user to enter city name
# echo "Enter the city name for which you want to fetch weather data:"
# read CITY

# # Validate city input
# if [ -z "$CITY" ]; then
#     echo "Error: City name cannot be empty."
#     exit 1
# fi

CITY="KOCHI"
API_ENDPOINT=$(echo "$API_TEMPLATE" | sed "s/{city}/$CITY/")
response=$(curl -s -X GET "$API_ENDPOINT")

# Log the response with a timestamp
echo "$(date): $response" >> "$LOG_FILE"
curl -s -X POST "$FASTAPI_ENDPOINT" \
    -H "Content-Type: application/json" \
    -d "{\"city\": \"$CITY\"}" >> "$LOG_FILE"
exit 
