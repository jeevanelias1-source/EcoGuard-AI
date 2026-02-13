import requests
import os
import random

async def fetch_aqi_data(lat, lon):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"main": {"aqi": 2}, "list": [{"components": {"pm2_5": 30}}]}
    
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception:
        return {"main": {"aqi": 2}}
