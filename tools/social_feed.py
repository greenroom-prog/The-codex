from typing import List
import random

class MockSocialFeed:
    """Simulates social media feed for testing"""
    
    def __init__(self):
        self.fear_posts = [
            "BTC crashing hard! Time to panic sell everything!",
            "This market is done. Total dump incoming. Get out now!",
            "Another exchange rugpull. Crypto is a scam. Selling all my bags.",
            "Fear index at all time high. Markets bleeding red.",
            "Whales dumping. Small holders getting destroyed. This is bad."
        ]
        
        self.greed_posts = [
            "BTC to the moon! 🚀 Bull run just starting!",
            "Just bought more! This rally is going to ATH!",
            "Breakout confirmed! Time to go all in! Bullish!",
            "Whales accumulating. We're going parabolic soon!",
            "Best entry point ever. Loading up bags! HODL!"
        ]
        
        self.neutral_posts = [
            "BTC holding support at $70k. Waiting for direction.",
            "Market consolidating. Could go either way from here.",
            "Trading sideways. No clear trend yet.",
            "Volume is low. Just watching for now.",
            "Interesting price action. Let's see what happens."
        ]
    
    def get_recent_posts(self, sentiment_bias: str = 'neutral', count: int = 20) -> List[str]:
        """Get simulated social media posts
        
        sentiment_bias: 'fear', 'greed', or 'neutral'
        """
        posts = []
        
        if sentiment_bias == 'fear':
            # 70% fear posts
            posts.extend(random.sample(self.fear_posts * 3, min(count * 7 // 10, len(self.fear_posts) * 3)))
            posts.extend(random.sample(self.neutral_posts, min(count * 3 // 10, len(self.neutral_posts))))
        elif sentiment_bias == 'greed':
            # 70% greed posts
            posts.extend(random.sample(self.greed_posts * 3, min(count * 7 // 10, len(self.greed_posts) * 3)))
            posts.extend(random.sample(self.neutral_posts, min(count * 3 // 10, len(self.neutral_posts))))
        else:
            # Mix of everything
            posts.extend(random.sample(self.fear_posts, min(count // 3, len(self.fear_posts))))
            posts.extend(random.sample(self.greed_posts, min(count // 3, len(self.greed_posts))))
            posts.extend(random.sample(self.neutral_posts, min(count // 3, len(self.neutral_posts))))
        
        random.shuffle(posts)
        return posts[:count]
