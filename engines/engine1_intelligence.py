import feedparser
from datetime import datetime

class IntelligenceEngine:
    """Engine 1: Scans policy makers and market movers for signals"""
    
    def __init__(self):
        self.sources = {
            'cftc': 'https://www.cftc.gov/PressRoom/RSS/rss_pressreleases',
            'sec': 'https://www.sec.gov/news/pressreleases.rss',
            'treasury': 'https://home.treasury.gov/news/press-releases/rss',
            'fed': 'https://www.federalreserve.gov/feeds/press_all.xml'
        }
        self.signals = []
    
    def scan(self):
        """Scan all policy sources for crypto signals"""
        crypto_keywords = ['crypto', 'bitcoin', 'digital asset', 'blockchain', 
                          'virtual currency', 'stablecoin']
        
        for source, url in self.sources.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:
                    text = (entry.title + " " + entry.get('summary', '')).lower()
                    if any(k in text for k in crypto_keywords):
                        sentiment = self._classify(entry.title)
                        self.signals.append({
                            'source': source,
                            'title': entry.title,
                            'type': 'policy',
                            'sentiment': sentiment,
                            'timestamp': datetime.now().isoformat()
                        })
            except Exception as e:
                pass
        
        return self.signals
    
    def _classify(self, text):
        """Classify sentiment of announcement"""
        text = text.lower()
        if any(w in text for w in ['approve', 'clarity', 'framework', 'legal']):
            return 'BULLISH'
        elif any(w in text for w in ['ban', 'restrict', 'fraud', 'crackdown']):
            return 'BEARISH'
        return 'NEUTRAL'
    
    def get_summary(self):
        """Return summary of signals"""
        if not self.signals:
            return "No policy signals"
        
        bullish = len([s for s in self.signals if s['sentiment'] == 'BULLISH'])
        bearish = len([s for s in self.signals if s['sentiment'] == 'BEARISH'])
        
        if bullish > bearish:
            return f"BULLISH ({bullish} pos, {bearish} neg)"
        elif bearish > bullish:
            return f"BEARISH ({bullish} pos, {bearish} neg)"
        return f"NEUTRAL ({bullish} pos, {bearish} neg)"
