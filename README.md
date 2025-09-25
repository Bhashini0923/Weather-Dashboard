# New Zealand Weather Dashboard

## Overview
An interactive dashboard built with **Streamlit** to explore both **live weather data** (via OpenWeather API) and **historical climate data** from New Zealand.  
The project demonstrates data collection, API integration, data visualization, and dashboard design.

## Features
- Fetches **live weather data** by city name (temperature, humidity, wind speed, conditions).
- Displays **historical climate data** for North and South New Zealand (CSV input).  
- Combines real-time and historical insights into a single dashboard.  
- Built using Python, Streamlit, pandas, matplotlib, and OpenWeather API.  

## Tech Stack
- **Python Libraries:** Streamlit, pandas, matplotlib, requests  
- **API:** OpenWeather API (for live weather data)  
- **Data:** Historical CSV files for North and South NZ (temperature, rainfall, etc.)

## API Key Setup
This project uses the [OpenWeather API](https://openweathermap.org/api) for live weather data.

1. Sign up at OpenWeather to get a free API key.  
2. Create an environment variable on your system:  

   **Mac/Linux (bash/zsh):**  
   ```bash
   export OPENWEATHER_API_KEY="your_api_key_here"

## Setup & Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Bhashini0923/weather-dashboard.git
   cd weather-dashboard
