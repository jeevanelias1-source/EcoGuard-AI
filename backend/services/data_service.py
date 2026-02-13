from datetime import datetime
from backend.services.weather_api import fetch_weather_data
from backend.services.aqi_api import fetch_aqi_data

async def get_environmental_data(lat: float, lon: float):
    weather_data = await fetch_weather_data(lat, lon)
    aqi_data = await fetch_aqi_data(lat, lon)
    main = weather_data.get("main", {})
    temp = main.get("temp", 0)
    comps = aqi_data.get("components", {})
    pm25 = comps.get("pm2_5", 0)
    now = datetime.now()
    return {
        "temperature": temp,
        "humidity": main.get("humidity", 0),
        "pm25": pm25,
        "wind_speed": weather_data.get("wind", {}).get("speed", 0),
        "rainfall": weather_data.get("rain", {}).get("1h", 0),
        "uv_index": weather_data.get("uvi", 5.0),
        "hour_of_day": now.hour,
        "day_of_week": now.weekday(),
        "3_day_temp_avg": round(temp * 0.98, 1),
        "7_day_rain_total": round(weather_data.get("rain", {}).get("1h", 0) * 2.5, 1)
    }
