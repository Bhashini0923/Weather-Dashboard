import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to convert temperature from Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Function to fetch live weather data from OpenWeather API
def get_weather_data(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
    url = f"{base_url}appid={api_key}&q={city_name}"
    response = requests.get(url)
    return response.json()

# Load historical data for North and South New Zealand
@st.cache_data
def load_historical_data(north_file, south_file):
    north_data = pd.read_csv(north_file)
    south_data = pd.read_csv(south_file)
    return north_data, south_data

# Streamlit UI setup
st.title("Weather Dashboard")

# Section for live weather data
st.subheader("Live Weather Data")

# User input for city name
city_name = st.text_input("Enter city name:")

# Fetch and display current weather data if a city is entered
if city_name:
    weather_data = get_weather_data(city_name)

    # Extract weather information
    temp_kelvin = weather_data['main']['temp']
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    feels_like_kelvin = weather_data['main']['feels_like']
    feels_like_celsius = kelvin_to_celsius(feels_like_kelvin)
    wind_speed = weather_data['wind']['speed']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']

    # Display current weather information
    st.write(f"**Weather in {city_name}**")
    st.write(f"**Temperature:** {temp_celsius:.2f}°C")
    st.write(f"**Feels Like:** {feels_like_celsius:.2f}°C")
    st.write(f"**Humidity:** {humidity}%")
    st.write(f"**Wind Speed:** {wind_speed} m/s")
    st.write(f"**Description:** {description.capitalize()}")

# Section for historical weather data analysis
st.subheader("New Zealand Historical Weather Data")

# Hardcoded file paths for North and South New Zealand CSVs
north_file = "data/North_NZ_2002_2022.csv"
south_file = "data/South_NZ_2002_2022.csv"

# Load the historical data
north_data, south_data = load_historical_data(north_file, south_file)

# Display the loaded data
st.subheader("North New Zealand Data")
st.write(north_data)

st.subheader("South New Zealand Data")
st.write(south_data)

# Function to calculate monthly averages for a specific parameter and year
def calculate_monthly_averages_by_year(data, parameter, year):
    filtered_data = data[(data['PARAMETER'] == parameter) & (data['YEAR'] == year)]
    monthly_averages = filtered_data[['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                                      'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']].mean()
    return monthly_averages

# Dropdown for selecting the parameter to analyze
parameter_options = {
    'Relative Humidity (RH2M)': 'RH2M',
    'Wind Speed (WS2M)': 'WS2M',
    'Max Temperature (T2M_MAX)': 'T2M_MAX',
    'Min Temperature (T2M_MIN)': 'T2M_MIN',
    'Precipitation (PRECTOTCORR)': 'PRECTOTCORR'
}

selected_parameter = st.selectbox("Select a parameter to analyze", list(parameter_options.keys()))

# Dropdown for selecting the year to analyze
years = list(range(2002, 2023))  # Years from 2002 to 2022
selected_year = st.selectbox("Select a year", years)

if selected_parameter and selected_year:
    parameter_code = parameter_options[selected_parameter]

    # Calculate and display monthly averages for North and South New Zealand for the selected year
    st.subheader(f"Monthly Averages for {selected_parameter} in {selected_year}")

    north_monthly_averages = calculate_monthly_averages_by_year(north_data, parameter_code, selected_year)
    south_monthly_averages = calculate_monthly_averages_by_year(south_data, parameter_code, selected_year)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**North New Zealand**")
        st.write(north_monthly_averages)

    with col2:
        st.write("**South New Zealand**")
        st.write(south_monthly_averages)

    # Plot the data for North and South New Zealand
    st.subheader(f"Historical Trends for {selected_parameter} in {selected_year}")
    plt.figure(figsize=(10, 5))

    plt.plot(north_monthly_averages.index, north_monthly_averages.values, marker='o', label="North NZ")
    plt.plot(south_monthly_averages.index, south_monthly_averages.values, marker='x', label="South NZ")

    plt.title(f"Monthly Averages of {selected_parameter} in {selected_year}")
    plt.xlabel("Month")
    plt.ylabel(selected_parameter)
    plt.legend()
    st.pyplot(plt)
