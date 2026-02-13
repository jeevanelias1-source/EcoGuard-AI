async def calculate_risk_score(weather, aqi):
    # Heuristic scoring
    score = 0
    temp = weather.get("main", {}).get("temp", 25)
    hum = weather.get("main", {}).get("humidity", 60)
    
    # Handle both real API and mock responses
    aqi_val = aqi.get("main", {}).get("aqi", 2)
    
    if temp > 35: score += 3
    elif temp > 30: score += 2
    
    if hum > 85: score += 2
    
    if aqi_val >= 4: score += 4
    elif aqi_val >= 3: score += 2
    
    score = min(score, 10)
    
    severity = "Low"
    if score >= 8: severity = "Critical"
    elif score >= 6: severity = "High"
    elif score >= 4: severity = "Moderate"
    
    return score, severity
