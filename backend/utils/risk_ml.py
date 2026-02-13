class RiskEngine:
    def predict_risk(self, temp, humidity, pm25):
        # Pure Python implementation of the risk model logic
        # High temp (>30), High humidity (>80), High PM2.5 (>50) increase risk
        score = 0
        if temp > 30: score += 1
        if temp > 35: score += 1
        if humidity > 80: score += 1
        if pm25 > 50: score += 2
        if pm25 > 100: score += 3
        
        label = 1 if score >= 3 else 0
        return label

risk_engine = RiskEngine()
