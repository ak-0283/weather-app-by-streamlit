import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt

# ---------------------------
# Function to get weather data
# ---------------------------
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# ---------------------------
# Streamlit App
# ---------------------------
st.title("🌤️ Weather Dashboard")

api_key = "f3adfe79b4626ab87abfd07fb6516a96"   # Replace with your OpenWeather API key
city = st.text_input("Enter city name:", "London")

if st.button("Get Weather"):
    data = get_weather(city, api_key)

    if data["cod"] != "200":
        st.error("City not found!")
    else:
        # Current weather
        st.subheader(f"Current Weather in {city}")
        current_temp = data["list"][0]["main"]["temp"]
        current_humidity = data["list"][0]["main"]["humidity"]
        description = data["list"][0]["weather"][0]["description"].title()
        wind_speed = data["list"][0]["wind"]["speed"]

        st.write(f"🌡️ Temperature: {current_temp} °C")
        st.write(f"💧 Humidity: {current_humidity}%")
        st.write(f"🌬️ Wind Speed: {wind_speed} m/s")
        st.write(f"☁️ Condition: {description}")

        # Forecast chart (next 5 days, every 3 hours)
        st.subheader("5-Day Temperature Forecast")
        temps = []
        dates = []
        for entry in data["list"]:
            temps.append(entry["main"]["temp"])
            dates.append(datetime.datetime.fromtimestamp(entry["dt"]))

        plt.figure(figsize=(10,4))
        plt.plot(dates, temps, marker="o")
        plt.xticks(rotation=45)
        plt.xlabel("Date/Time")
        plt.ylabel("Temperature (°C)")
        plt.title(f"Temperature Forecast for {city}")
        st.pyplot(plt)
