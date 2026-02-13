from textblob import TextBlob
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

    def get_social_score(self, lat, lon):
        """
        Calculates a social stress score (1-10) based on sentiment analysis
        of recent community feedback.
        """
        # Select 5 random messages for analysis
        recent_messages = random.sample(self.mock_feed, 5)
        polarities = [TextBlob(msg).sentiment.polarity for msg in recent_messages]
        avg_polarity = sum(polarities) / len(polarities)
        
        # Count stress indicators
        stress_count = 0
        all_text = " ".join(recent_messages).lower()
        for word in self.stress_indicators:
            if word in all_text:
                stress_count += 1
        
        # Sentiment score from -1 (bad) to 1 (good)
        # We want a stress score from 1 (low stress) to 10 (high stress)
        # Lower polarity + Higher stress indicators = Higher Stress Score
        base_score = 5 - (avg_polarity * 5) # Scale to 0-10
        stress_bonus = (stress_count / len(self.stress_indicators)) * 5
        
        final_score = min(10, max(1, base_score + stress_bonus))
        return round(final_score, 1)

    def get_recent_pulse(self):
        """
        Returns a list of recent community feedback with sentiment labels.
        """
        pulses = []
        recent_messages = random.sample(self.mock_feed, 4)
        for msg in recent_messages:
            polarity = TextBlob(msg).sentiment.polarity
            label = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
            pulses.append({"text": msg, "sentiment": label})
        return pulses

social_service = SocialService()

