from backend.services.data_service import get_environmental_data
from backend.utils.risk_ml import risk_engine
from backend.services.risk_model import calculate_risk_score
from backend.services.social_service import social_service
import logging

logger = logging.getLogger(__name__)

class RiskEngine:
    async def analyze_risk(self, lat: float, lon: float):
        data = await get_environmental_data(lat, lon)
        if "error" in data:
            raise Exception(data["error"])
        try:
            ml_risk_val = risk_engine.predict_risk(data["temperature"], data["humidity"], data["pm25"])
            ml_label = "High Risk" if ml_risk_val == 1 else "Low Risk"
        except:
            ml_risk_val = 0
            ml_label = "Unavailable"
        location_name = data.get("raw_weather", {}).get("name", "Local Area")
        social_data = await social_service.get_social_stress(location_name)
        base_assessment = calculate_risk_score(data["raw_weather"], data["raw_aqi"])
        env_score = base_assessment["score"]
        social_score = social_data["score"]
        combined_score = round((env_score * 0.7) + (social_score * 0.3), 1)
        final_severity = "Low"
        if combined_score >= 8: final_severity = "Critical"
        elif combined_score >= 6: final_severity = "High"
        elif combined_score >= 4: final_severity = "Moderate"
        return {
            "score": combined_score,
            "severity_label": final_severity,
            "environmental_base": {"score": env_score, "label": base_assessment["level"]},
            "social_overlay": social_data,
            "ml_prediction": {"label": ml_label, "raw_value": ml_risk_val},
            "contributing_factors": base_assessment["factors"],
            "aggregated_metrics": data,
            "raw_data": data
        }
environmental_risk_engine = RiskEngine()
