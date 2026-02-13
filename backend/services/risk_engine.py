from services.data_service import get_environmental_data
from services.risk_model import calculate_risk_score
from services.social_service import social_service
from utils.risk_ml import risk_engine

class RiskEngine:
    async def analyze_risk(self, lat: float, lon: float):
        # 1. Get real-world data (async)
        data = await get_environmental_data(lat, lon)
        
        # 2. Heuristic base assessment (now async)
        score, label = await calculate_risk_score(data["raw_weather"], data["raw_aqi"])
        
        # 3. Social overlay (async)
        location_name = data["raw_weather"].get("name", "Current Region")
        social_data = await social_service.get_social_stress(location_name)
        
        # 4. ML Enhancement (sync)
        ml_label_idx = risk_engine.predict_risk(
            data["raw_weather"].get("main", {}).get("temp", 25),
            data["raw_weather"].get("main", {}).get("humidity", 60),
            data["raw_aqi"].get("list", [{}])[0].get("components", {}).get("pm2_5", 30)
        )
        ml_labels = ["Low Risk", "High Risk"]
        
        # Aggregate metrics
        metrics = {
            "temperature": data["raw_weather"].get("main", {}).get("temp"),
            "humidity": data["raw_weather"].get("main", {}).get("humidity"),
            "pm25": data["raw_aqi"].get("list", [{}])[0].get("components", {}).get("pm2_5", 30)
        }
        
        return {
            "score": score,
            "severity_label": label,
            "contributing_factors": ["Heat" if metrics["temperature"] > 30 else "Normal"],
            "aggregated_metrics": metrics,
            "social_overlay": social_data,
            "raw_data": data,
            "ml_prediction": {"label": ml_labels[ml_label_idx], "raw_value": ml_label_idx},
            "environmental_base": {"score": score, "level": label}
        }

environmental_risk_engine = RiskEngine()
