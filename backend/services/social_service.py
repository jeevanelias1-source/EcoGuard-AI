import random

class SocialService:
    def __init__(self):
        self.mock_feed = [
            "The air feels heavy today, hard to breathe.",
            "Beautiful sunny day! Perfect for a walk.",
            "Is it just me or is the pollution getting worse in downtown?",
            "Love the new environmental monitoring app, so helpful.",
            "Stuck in traffic, the smog is unbearable.",
            "Water quality in the local park seems much better now.",
            "Warning: High UV levels today, stay hydrated!",
            "Feeling stressed about the recent heatwaves.",
            "Great community effort on the recycling drive.",
            "The city needs more green spaces."
        ]
        self.stress_indicators = ["unbearable", "worse", "heavy", "hard", "pollution", "smog", "stressed"]

    async def get_social_stress(self, location_name: str):
        # Simulated stress score calculation
        recent_messages = random.sample(self.mock_feed, 4)
        stress_count = 0
        all_text = " ".join(recent_messages).lower()
        for word in self.stress_indicators:
            if word in all_text:
                stress_count += 1
        
        score = min(10.0, 2.0 + (stress_count * 2.0) + random.uniform(-1, 1))
        severity = "Low"
        if score >= 8: severity = "Critical"
        elif score >= 6: severity = "High"
        elif score >= 4: severity = "Moderate"
        
        return {
            "score": round(score, 1),
            "severity": severity,
            "sentiment_average": round(random.uniform(-0.5, 0.8), 2),
            "recent_shouts": recent_messages
        }

social_service = SocialService()
