from datetime import datetime
try:
    from services.weather_api import fetch_weather_data
    from services.aqi_api import fetch_aqi_data
except ImportError:
    try:
        from backend.services.weather_api import fetch_weather_data
        from backend.services.aqi_api import fetch_aqi_data
    except ImportError:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from weather_api import fetch_weather_data
        from aqi_api import fetch_aqi_data

async def get_environmental_data(lat: float, lon: float):
    weather_data = await fetch_weather_data(lat, lon)
    aqi_data = await fetch_aqi_data(lat, lon)
    
    main = weather_data.get("main", {})
    temp = main.get("temp", 25)
    
    # Handle list-based AQI response
    pm25 = 30
    if isinstance(aqi_data, dict):
        if "list" in aqi_data and len(aqi_data["list"]) > 0:
            pm25 = aqi_data["list"][0].get("components", {}).get("pm2_5", 30)
        elif "components" in aqi_data:
            pm25 = aqi_data.get("components", {}).get("pm2_5", 30)
        elif "main" in aqi_data: # Fallback for some structures
             pass
    
    now = datetime.now()
    
    return {
        "temperature": temp,
        "humidity": main.get("humidity", 60),
        "pm25": pm25,
        "wind_speed": weather_data.get("wind", {}).get("speed", 0),
        "rainfall": weather_data.get("rain", {}).get("1h", 0),
        "uv_index": weather_data.get("uvi", 5.0),
        "hour_of_day": now.hour,
        "day_of_week": now.weekday(),
        "3_day_temp_avg": round(temp * 0.98, 1),
        "7_day_rain_total": round(weather_data.get("rain", {}).get("1h", 0) * 2.5, 1),
        "raw_weather": weather_data,
        "raw_aqi": aqi_data
    }
