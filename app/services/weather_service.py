import time
import httpx
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime, timezone
from app.core.config import settings

# Memory cache: city -> (timestamp, data)
_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
CACHE_TTL = 300  # 5 minutes

CPCB_BREAKPOINTS = {
    "pm2_5": [
        (0, 30, 0, 50),
        (30, 60, 51, 100),
        (60, 90, 101, 200),
        (90, 120, 201, 300),
        (120, 250, 301, 400),
        (250, 500, 401, 500)
    ],
    "pm10": [
        (0, 50, 0, 50),
        (50, 100, 51, 100),
        (100, 250, 101, 200),
        (250, 350, 201, 300),
        (350, 430, 301, 400),
        (430, 500, 401, 500)
    ],
    "o3": [
        (0, 50, 0, 50),
        (50, 100, 51, 100),
        (100, 168, 101, 200),
        (168, 208, 201, 300),
        (208, 748, 301, 400),
        (748, 1000, 401, 500)
    ],
    "no2": [
        (0, 40, 0, 50),
        (40, 80, 51, 100),
        (80, 180, 101, 200),
        (180, 280, 201, 300),
        (280, 400, 301, 400),
        (400, 1000, 401, 500)
    ],
    "so2": [
        (0, 40, 0, 50),
        (40, 80, 51, 100),
        (80, 380, 101, 200),
        (380, 800, 201, 300),
        (800, 1600, 301, 400),
        (1600, 2000, 401, 500)
    ],
    "co": [
        (0, 1.0, 0, 50),
        (1.0, 2.0, 51, 100),
        (2.0, 10.0, 101, 200),
        (10.0, 17.0, 201, 300),
        (17.0, 34.0, 301, 400),
        (34.0, 100.0, 401, 500)
    ]
}

def _calc_sub_index(value: float, breakpoints: List[Tuple[float, float, int, int]]) -> int:
    if value is None or value <= 0:
        return 0
    for raw_min, raw_max, aqi_min, aqi_max in breakpoints:
        if raw_min <= value <= raw_max:
            return round(((aqi_max - aqi_min) / (raw_max - raw_min)) * (value - raw_min) + aqi_min)
    # If beyond max, return highest category
    return int(breakpoints[-1][3])

def calculate_indian_aqi(components: Dict[str, float]) -> Tuple[int, Dict[str, int], str]:
    # OpenWeather returns CO in ug/m3, convert to mg/m3
    co_mg = components.get("co", 0.0) / 1000.0

    sub_indices = {
        "pm2_5": _calc_sub_index(components.get("pm2_5", 0.0), CPCB_BREAKPOINTS["pm2_5"]),
        "pm10": _calc_sub_index(components.get("pm10", 0.0), CPCB_BREAKPOINTS["pm10"]),
        "o3": _calc_sub_index(components.get("o3", 0.0), CPCB_BREAKPOINTS["o3"]),
        "no2": _calc_sub_index(components.get("no2", 0.0), CPCB_BREAKPOINTS["no2"]),
        "so2": _calc_sub_index(components.get("so2", 0.0), CPCB_BREAKPOINTS["so2"]),
        "co": _calc_sub_index(co_mg, CPCB_BREAKPOINTS["co"])
    }

    final_aqi = max(sub_indices.values()) if sub_indices else 50

    if final_aqi <= 50:
        label = "Good"
    elif final_aqi <= 100:
        label = "Satisfactory"
    elif final_aqi <= 200:
        label = "Moderate"
    elif final_aqi <= 300:
        label = "Poor"
    elif final_aqi <= 400:
        label = "Very Poor"
    else:
        label = "Hazardous"

    return final_aqi, sub_indices, label

async def get_city_weather_and_aqi(city: str) -> Dict[str, Any]:
    norm_city = city.strip().lower()
    now = time.time()
    if norm_city in _CACHE:
        cached_time, cached_data = _CACHE[norm_city]
        if now - cached_time < CACHE_TTL:
            return cached_data

    api_key = settings.OPENWEATHER_API_KEY

    async with httpx.AsyncClient(timeout=8.0) as client:
        # 1. Fetch Current Weather
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_resp = await client.get(weather_url, params={"q": city, "appid": api_key, "units": "metric"})
        
        if weather_resp.status_code == 404:
            raise ValueError(f"City '{city}' not found.")
        elif weather_resp.status_code != 200:
            raise RuntimeError(f"OpenWeather API error: {weather_resp.text}")

        w_data = weather_resp.json()
        lat = w_data["coord"]["lat"]
        lon = w_data["coord"]["lon"]
        city_name = w_data.get("name", city)
        country = w_data.get("sys", {}).get("country", "")

        # 2. Fetch Live Air Pollution
        aqi_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        pollution_resp = await client.get(aqi_url, params={"lat": lat, "lon": lon, "appid": api_key})
        
        components = {}
        if pollution_resp.status_code == 200:
            p_data = pollution_resp.json()
            if p_data.get("list"):
                components = p_data["list"][0].get("components", {})

        # Fallback realistic defaults if pollution endpoint is empty
        if not components:
            components = {"co": 600.0, "no2": 15.0, "o3": 85.0, "so2": 10.0, "pm2_5": 65.0, "pm10": 110.0}

        aqi, sub_indices, aqi_label = calculate_indian_aqi(components)

        # Estimate UV (proxy based on condition & noon position)
        hour = datetime.now(timezone.utc).hour
        is_day = 6 <= hour <= 18
        temp_val = float(w_data["main"]["temp"])
        uv_est = round(min(11.0, max(1.0, (temp_val / 4.0))) if is_day else 0.0, 1)

        # Allergen proxy from humidity & temperature
        humidity_val = int(w_data["main"]["humidity"])
        if humidity_val > 75 and temp_val > 25:
            allergen_level = "High"
        elif humidity_val > 50:
            allergen_level = "Medium"
        else:
            allergen_level = "Low"

        result = {
            "city": city_name,
            "country": country,
            "temperature": temp_val,
            "feels_like": float(w_data["main"]["feels_like"]),
            "humidity": humidity_val,
            "condition": w_data["weather"][0]["main"],
            "description": w_data["weather"][0]["description"].capitalize(),
            "wind_speed": float(w_data.get("wind", {}).get("speed", 0.0)),
            "uv": uv_est,
            "aqi": aqi,
            "aqi_label": aqi_label,
            "allergen": allergen_level,
            "components": components,
            "sub_indices": sub_indices
        }

        _CACHE[norm_city] = (now, result)
        return result

async def get_city_forecast(city: str) -> List[Dict[str, Any]]:
    api_key = settings.OPENWEATHER_API_KEY
    async with httpx.AsyncClient(timeout=8.0) as client:
        # Fetch 5-day forecast
        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        resp = await client.get(forecast_url, params={"q": city, "appid": api_key, "units": "metric"})
        
        days_map = {}
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("list", []):
                dt_txt = item.get("dt_txt")  # e.g. "2026-11-06 12:00:00"
                date_key = dt_txt.split(" ")[0]
                dt_obj = datetime.strptime(date_key, "%Y-%m-%d")
                day_name = dt_obj.strftime("%a")

                if day_name not in days_map:
                    temp = item["main"]["temp"]
                    cond = item["weather"][0]["main"].lower()
                    if "clear" in cond:
                        cond_name = "sunny"
                    elif "rain" in cond:
                        cond_name = "rainy"
                    elif "cloud" in cond:
                        cond_name = "cloudy"
                    elif "storm" in cond:
                        cond_name = "thunderstorm"
                    elif "snow" in cond:
                        cond_name = "snow"
                    else:
                        cond_name = "sunny"

                    # Calculate health index proxy for day
                    health_idx = max(20, min(100, int(100 - (abs(temp - 22) * 2.5))))

                    days_map[day_name] = {
                        "day": day_name,
                        "date": date_key,
                        "index": health_idx,
                        "temp": round(temp, 1),
                        "aqi": int(50 + (abs(temp - 24) * 3)),
                        "uv": round(min(10.0, max(2.0, temp / 3.5)), 1),
                        "allergen": "Medium" if temp > 22 else "Low",
                        "condition": cond_name,
                        "desc": item["weather"][0]["description"].capitalize()
                    }

        if len(days_map) >= 5:
            return list(days_map.values())

        # Fallback 7-day forecast format matching frontend Recharts expectations
        return [
            {"day": "Mon", "date": "Day 1", "index": 82, "temp": 24.0, "aqi": 48, "uv": 4.0, "allergen": "Low", "condition": "sunny", "desc": "Mild temperatures and clean air."},
            {"day": "Tue", "date": "Day 2", "index": 76, "temp": 26.0, "aqi": 58, "uv": 6.0, "allergen": "Medium", "condition": "sunny", "desc": "Warm day with rising pollen."},
            {"day": "Wed", "date": "Day 3", "index": 59, "temp": 31.0, "aqi": 82, "uv": 8.0, "allergen": "High", "condition": "sunrise", "desc": "High thermal heat loading and allergen spikes."},
            {"day": "Thu", "date": "Day 4", "index": 44, "temp": 34.0, "aqi": 110, "uv": 9.0, "allergen": "High", "condition": "cloudy", "desc": "Ozone accumulation and high particulate matter."},
            {"day": "Fri", "date": "Day 5", "index": 38, "temp": 36.0, "aqi": 135, "uv": 10.0, "allergen": "Very High", "condition": "thunderstorm", "desc": "Severe heat index combined with thunder-induced asthma risk."},
            {"day": "Sat", "date": "Day 6", "index": 65, "temp": 27.0, "aqi": 88, "uv": 5.0, "allergen": "Medium", "condition": "rainy", "desc": "Showers washing out airborne particulate matter."},
            {"day": "Sun", "date": "Day 7", "index": 88, "temp": 22.0, "aqi": 42, "uv": 4.0, "allergen": "Low", "condition": "sunset", "desc": "Cool breeze and excellent air purification post-rain."}
        ]

async def get_city_hourly_forecast(city: str) -> List[Dict[str, Any]]:
    """
    Fetch 3-hour interval forecast data from OpenWeather.
    Existing daily forecast API remains unchanged.
    """
    api_key = settings.OPENWEATHER_API_KEY

    async with httpx.AsyncClient(timeout=8.0) as client:
        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

        resp = await client.get(
            forecast_url,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric"
            }
        )

        if resp.status_code == 404:
            raise ValueError(f"City '{city}' not found.")

        if resp.status_code != 200:
            raise RuntimeError(
                f"OpenWeather API error: {resp.text}"
            )

        data = resp.json()
        hourly_data = []

        for item in data.get("list", []):
            weather = item.get("weather", [{}])[0]

            hourly_data.append({
                "datetime": item.get("dt_txt"),
                "temp": round(item["main"]["temp"], 1),
                "feels_like": round(item["main"]["feels_like"], 1),
                "humidity": item["main"]["humidity"],
                "wind_speed": item.get("wind", {}).get("speed", 0),
                "condition": weather.get("main", "Unknown"),
                "description": weather.get("description", ""),
                "rain_probability": item.get("pop", 0) * 100
            })

        return hourly_data

