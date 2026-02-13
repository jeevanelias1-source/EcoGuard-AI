try:
    from services.data_service import get_environmental_data
    from services.risk_model import calculate_risk_score
    from services.social_service import social_service
except ImportError:
    try:
        from backend.services.data_service import get_environmental_data
        from backend.services.risk_model import calculate_risk_score
        from backend.services.social_service import social_service
    except ImportError:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from data_service import get_environmental_data
        from risk_model import calculate_risk_score
        from social_service import social_service

from utils.risk_ml import risk_engine

class RiskEngine:
    async def analyze_risk(self, lat: float, lon: float):
        # 1. Get real-world data (async)
        data = await get_environmental_data(lat, lon)
        
        # 2. Heuristic base assessment (now async)
        # Use .get() and fallbacks
        raw_weather = data.get("raw_weather", {})
        if not raw_weather:
            raw_weather = {"main": {"temp": data.get("temperature", 25), "humidity": data.get("humidity", 60)}, "name": "Local Area"}
            
        raw_aqi = data.get("raw_aqi", {})
        if not raw_aqi:
            raw_aqi = {"list": [{"components": {"pm2_5": data.get("pm25", 30)}}], "main": {"aqi": 2}}
            
        score, label = await calculate_risk_score(raw_weather, raw_aqi)
        
        # 3. Social overlay (async)
        location_name = raw_weather.get("name", "Current Region")
        social_data = await social_service.get_social_stress(location_name)
        
        # 4. ML Enhancement (sync)
        ml_label_idx = risk_engine.predict_risk(
            raw_weather.get("main", {}).get("temp", 25),
            raw_weather.get("main", {}).get("humidity", 60),
            raw_aqi.get("list", [{}])[0].get("components", {}).get("pm2_5", 30) if isinstance(raw_aqi, dict) and "list" in raw_aqi else 30
        )
        ml_labels = ["Low Risk", "High Risk"]
        
        # Aggregate metrics
        metrics = {
            "temperature": raw_weather.get("main", {}).get("temp"),
            "humidity": raw_weather.get("main", {}).get("humidity"),
            "pm25": raw_aqi.get("list", [{}])[0].get("components", {}).get("pm2_5", 30) if isinstance(raw_aqi, dict) and "list" in raw_aqi else 30
        }
        
        return {
            "score": score,
            "severity_label": label,
            "contributing_factors": ["Heat" if (metrics["temperature"] or 0) > 30 else "Normal"],
            "aggregated_metrics": metrics,
            "social_overlay": social_data,
            "raw_data": data,
            "ml_prediction": {"label": ml_labels[ml_label_idx], "raw_value": ml_label_idx},
            "environmental_base": {"score": score, "level": label}
        }

environmental_risk_engine = RiskEngine()
