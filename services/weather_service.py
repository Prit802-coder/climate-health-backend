import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": "City not found"}

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