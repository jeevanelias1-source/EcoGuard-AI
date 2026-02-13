import numpy as np
import pandas as pd
# Mocking scikit-learn behavior for demonstration if model file is not found
# In a real scenario, this would load a joblib model

class RiskEngine:
    def __init__(self):
        self.model_loaded = False
        try:
            # Fallback for demonstration: A simple heuristic model
            self.weights = {
                "temperature": 0.4,
                "humidity": 0.2,
                "pm2_5": 0.4
            }
            self.model_loaded = True
        except Exception:
            pass

    def predict_risk(self, features):
        """
        Predicts an environmental risk level based on input features.
        Features expected: temperature, humidity, PM2.5, etc.
        Returns a risk score 1-10.
        """
        try:
            temp = features.get("temperature", 25)
            hum = features.get("humidity", 50)
            pm25 = features.get("PM2.5", 10)
            
            # Simple weighted prediction logic
            score = (temp / 40 * 4) + (hum / 100 * 2) + (pm25 / 100 * 4)
            final_score = min(10, max(1, score * 2)) # Scale and bound
            
            return round(final_score, 1)
        except Exception:
            return 5.0

risk_engine = RiskEngine()

