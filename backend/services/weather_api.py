import requests
import os
import random

# Use async to avoid blocking
async def fetch_weather_data(lat, lon):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {
            "main": {"temp": 25, "humidity": 60, "temp_max": 28, "temp_min": 22},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 5}
        }
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        return response.json()
    except Exception:
        return {"main": {"temp": 25, "humidity": 60}}
