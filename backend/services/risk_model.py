async def calculate_risk_score(environmental_data, social_score):
    """
    Calculates a hybrid risk score (1-10) by combining environmental data
    and social stress sentiment.
    
    Weights:
    - Environmental Risks: 70%
    - Social Stress: 30%
    """
    try:
        # Environmental risk component (simplified for this model)
        # In a real scenario, this would involve complex logic based on multiple factors
        temp = environmental_data.get("temperature", 25)
        aqi = environmental_data.get("aqi", 1)
        humidity = environmental_data.get("humidity", 50)
        
        # Normalize environmental factors to 1-10 scale
        # e.g., Temp > 35 is high risk, AQI > 4 is high risk
        env_score = (min(temp / 40 * 10, 10) + (aqi * 2) + (humidity / 100 * 5)) / 3
        env_score = min(10, max(1, env_score))
        
        # Hybrid calculation
        final_score = (env_score * 0.7) + (social_score * 0.3)
        
        return round(final_score, 1)
    except Exception as e:
        return 5.0 # Neutral fallback

