#!/bin/bash

API_URL="http://api.openweathermap.org/data/2.5/weather"
API_KEY="ac5559a726f0d448e4c774c8fa2c6655"  # Replace with your OpenWeatherMap API key

fetch_weather_data() {
    local city=$1
    local url="${API_URL}?q=${city}&appid=${API_KEY}&units=metric"
    curl -s "${url}"
}

# Prompt user to enter city name
echo "Enter the city for which you want to fetch weather data:"
read CITY
if [ -z "$CITY" ]; then
    echo "Error: City name cannot be empty."
    exit 1
fi

OUTPUT_DIR="$HOME/weather_data"

# Duration and interval settings
DURATION=3600   # 1 hour in seconds
INTERVAL=300    # 5 minutes in seconds

# Start time
START_TIME=$(date +%s)
END_TIME=$((START_TIME + DURATION))

while [ $(date +%s) -lt $END_TIME ]; do
    # Generate timestamp for file name
    TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
    OUTPUT_FILE="$OUTPUT_DIR/weather_data_${TIMESTAMP}.json"

    # Fetch and save weather data
    FETCHED_DATA=$(fetch_weather_data "$CITY")
    echo "$FETCHED_DATA" > "$OUTPUT_FILE"

    # Print status
    echo "Weather data saved to $OUTPUT_FILE"

    # Wait for the next interval
    sleep $INTERVAL
done
