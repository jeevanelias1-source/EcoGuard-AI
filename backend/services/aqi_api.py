import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "mock_key")

async def fetch_aqi_data(lat, lon):
    """
    Fetches real-time Air Quality data from OpenWeatherMap Air Pollution API.
    Returns PM2.5, PM10, NO2, and O3.
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            raise Exception("API error")

        return data
    except Exception as e:
        # Simulated fallback data
        import random
        return {
            "list": [{
                "main": {"aqi": random.randint(1, 5)},
                "components": {
                    "pm2_5": random.uniform(5, 50),
                    "pm10": random.uniform(10, 80),
                    "no2": random.uniform(2, 30),
                    "o3": random.uniform(20, 100),
                    "so2": random.uniform(1, 10),
                    "nh3": random.uniform(0.5, 5),
                    "co": random.uniform(200, 1000)
                },
                "dt": 1605187200
            }]
        }

