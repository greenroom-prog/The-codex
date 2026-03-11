from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
from datetime import datetime

class SentimentAnalyzer:
    """Analyze social media sentiment for crypto"""
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        # Crypto-specific keywords
        self.keywords = {
            'bullish': ['moon', 'bullish', 'pump', 'buy', 'long', 'ATH', 'breakout'],
            'bearish': ['dump', 'bearish', 'sell', 'short', 'crash', 'drop', 'rekt']
        }
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze sentiment of a single text"""
        scores = self.analyzer.polarity_scores(text)
        
        # Check for crypto keywords
        text_lower = text.lower()
        bullish_count = sum(1 for word in self.keywords['bullish'] if word in text_lower)
        bearish_count = sum(1 for word in self.keywords['bearish'] if word in text_lower)
        
        # Combine VADER score with keyword analysis
        sentiment_score = scores['compound']
        if bullish_count > bearish_count:
            sentiment_score += 0.2
        elif bearish_count > bullish_count:
            sentiment_score -= 0.2
        
        # Classify sentiment
        if sentiment_score >= 0.05:
            sentiment = "BULLISH"
        elif sentiment_score <= -0.05:
            sentiment = "BEARISH"
        else:
            sentiment = "NEUTRAL"
        
        return {
            'sentiment': sentiment,
            'score': sentiment_score,
            'confidence': abs(sentiment_score),
            'bullish_keywords': bullish_count,
            'bearish_keywords': bearish_count,
            'raw_scores': scores
        }
    
    def analyze_batch(self, texts: List[str]) -> Dict:
        """Analyze sentiment across multiple texts"""
        if not texts:
            return {
                'overall_sentiment': 'NEUTRAL',
                'sentiment_score': 0.0,
                'sample_size': 0
            }
        
        results = [self.analyze_text(text) for text in texts]
        
        # Calculate aggregates
        avg_score = sum(r['score'] for r in results) / len(results)
        bullish_count = sum(1 for r in results if r['sentiment'] == 'BULLISH')
        bearish_count = sum(1 for r in results if r['sentiment'] == 'BEARISH')
        
        # Overall sentiment
        if avg_score >= 0.1:
            overall = "BULLISH"
        elif avg_score <= -0.1:
            overall = "BEARISH"
        else:
            overall = "NEUTRAL"
        
        return {
            'overall_sentiment': overall,
            'sentiment_score': avg_score,
            'bullish_percent': (bullish_count / len(results)) * 100,
            'bearish_percent': (bearish_count / len(results)) * 100,
            'sample_size': len(results),
            'timestamp': datetime.utcnow()
        }
    
    def get_mock_social_data(self, symbol: str) -> List[str]:
        """Mock social media posts for testing (replace with real API later)"""
        # Simulated posts about BTC
        mock_posts = [
            f"{symbol} breaking through resistance! Moon mission activated 🚀",
            f"Just bought more {symbol}, feeling bullish on this dip",
            f"{symbol} looking weak, might sell soon",
            f"Technical analysis shows {symbol} forming bull flag pattern",
            f"{symbol} holders getting rekt, crash incoming?",
            f"Major institutions accumulating {symbol}, very bullish signal",
            f"{symbol} consolidating nicely, breakout soon",
            f"Fear index high, perfect time to buy {symbol}",
            f"{symbol} price action looking terrible, bear market confirmed",
            f"Diamond hands on {symbol}, not selling"
        ]
        return mock_posts

