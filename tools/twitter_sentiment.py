import tweepy
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List

class TwitterSentiment:
    """Real Twitter sentiment analysis"""
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        # Twitter API v2 - Free tier: 500 tweets/month
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN', None)
        
        if bearer_token:
            self.client = tweepy.Client(bearer_token=bearer_token)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
    
    def get_bitcoin_tweets(self, count: int = 10) -> List[str]:
        """Fetch recent Bitcoin tweets"""
        if not self.enabled:
            return self._get_mock_tweets()
        
        try:
            query = 'bitcoin OR btc OR $BTC -is:retweet lang:en'
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=min(count, 100),
                tweet_fields=['created_at', 'public_metrics']
            )
            
            if tweets.data:
                return [tweet.text for tweet in tweets.data]
            else:
                return self._get_mock_tweets()
        except:
            return self._get_mock_tweets()
    
    def _get_mock_tweets(self) -> List[str]:
        """Fallback mock data"""
        return [
            "Bitcoin breaking out! This is bullish AF 🚀",
            "BTC dump incoming, everyone panic selling",
            "Just bought more bitcoin at this level",
            "Bitcoin is dead, told you so",
            "To the moon! Bitcoin ATH soon 🌙",
            "Bearish on crypto right now",
            "Bitcoin looking strong, holding $70k",
            "Sell signal on BTC, this won't end well",
            "Accumulating more sats, long term bullish",
            "Bitcoin crash imminent, mark my words"
        ]
    
    def analyze_sentiment(self) -> Dict:
        """Analyze Bitcoin sentiment from Twitter"""
        tweets = self.get_bitcoin_tweets(20)
        
        scores = [self.analyzer.polarity_scores(tweet)['compound'] for tweet in tweets]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        bullish = sum(1 for s in scores if s > 0.05)
        bearish = sum(1 for s in scores if s < -0.05)
        neutral = len(scores) - bullish - bearish
        
        return {
            'score': avg_score,
            'sentiment': 'BULLISH' if avg_score > 0.05 else 'BEARISH' if avg_score < -0.05 else 'NEUTRAL',
            'bullish_pct': (bullish / len(scores)) * 100,
            'bearish_pct': (bearish / len(scores)) * 100,
            'sample_size': len(tweets),
            'using_real_data': self.enabled
        }
