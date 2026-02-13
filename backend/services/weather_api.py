import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "mock_key")

async def fetch_weather_data(lat, lon):
    """
    Fetches real-time weather data from OpenWeatherMap API.
    If API key is missing or invalid, returns simulated data for demonstration.
    """
    try:
        # Current Weather URL
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            raise Exception("API error")

        # One Call API for UV Index (if available)
        uv_url = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        uv_response = requests.get(uv_url)
        uv_data = uv_response.json()
        
        return {
            "main": {
                "temp": data.get("main", {}).get("temp", 25),
                "feels_like": data.get("main", {}).get("feels_like", 27),
                "humidity": data.get("main", {}).get("humidity", 60)
            },
            "wind": {
                "speed": data.get("wind", {}).get("speed", 5)
            },
            "rain": {
                "1h": data.get("rain", {}).get("1h", 0)
            },
            "uvi": uv_data.get("value", 5)
        }
    except Exception as e:
        # Simulated fallback data
        import random
        return {
            "main": {
                "temp": 25 + random.uniform(-5, 5),
                "feels_like": 27 + random.uniform(-5, 5),
                "humidity": 60 + random.uniform(-10, 10)
            },
            "wind": {
                "speed": 5 + random.uniform(-2, 5)
            },
            "rain": {
                "1h": random.choice([0, 0, 0, 1.5, 0.5])
            },
            "uvi": random.uniform(0, 10)
        }

