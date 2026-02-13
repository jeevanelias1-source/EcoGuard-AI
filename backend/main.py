from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sys
import os
# Add current and parent directory to path for flexible imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.services.data_service import get_environmental_data
    from backend.services.risk_engine import environmental_risk_engine
except ImportError:
    from services.data_service import get_environmental_data
from services.risk_engine import environmental_risk_engine
import logging
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Environmental Risk Prediction System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/api/risk")
async def get_simplified_risk(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    try:
        result = await environmental_risk_engine.analyze_risk(lat, lon)
        metrics = result["aggregated_metrics"]
        return {
            "temperature": metrics["temperature"],
            "humidity": metrics["humidity"],
            "pm25": metrics["pm25"],
            "uv_index": metrics.get("uv_index"),
            "rainfall": metrics.get("rainfall"),
            "risk_level": result["score"],
            "severity_label": result["severity_label"],
            "social_stress_score": result["social_overlay"]["score"]
        }
    except Exception as e:
        logger.error(f"Error in /api/risk endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/environmental-data")
async def get_env_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    return await get_environmental_data(lat, lon)

@app.get("/api/risk-data")
async def get_risk_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    try:
        risk_result = await environmental_risk_engine.analyze_risk(lat, lon)
        return {
            "location": {"lat": lat, "lon": lon},
            "weather": risk_result["raw_data"]["raw_weather"],
            "air_quality": risk_result["raw_data"]["raw_aqi"],
            "risk_assessment": {
                "score": risk_result["score"],
                "level": risk_result["severity_label"],
                "factors": risk_result["contributing_factors"],
                "ml_model_prediction": risk_result["ml_prediction"]["label"],
                "ml_raw_output": risk_result["ml_prediction"]["raw_value"],
                "social_stress_score": risk_result["social_overlay"]["score"],
                "social_severity": risk_result["social_overlay"]["severity"],
                "recent_social_sentiment": risk_result["social_overlay"]["sentiment_average"],
                "timestamp": "now"
            },
            "social_data": risk_result["social_overlay"],
            "environmental_data": risk_result["environmental_base"],
            "aggregated_metrics": risk_result["aggregated_metrics"]
        }
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
