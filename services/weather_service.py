import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):

    if not API_KEY:
        return {"error": "OpenWeather API key is not configured"}

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    print("OpenWeather status:", response.status_code)
    print("OpenWeather response:", response.text)

    if response.status_code == 401:
        return {"error": "Invalid OpenWeather API key"}

    if response.status_code == 404:
        return {"error": "City not found"}

    if response.status_code != 200:
        return {"error": "Unable to fetch weather data"}

    data = response.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "feels_like": data["main"]["feels_like"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }