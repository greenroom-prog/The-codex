from engines.youtube_intelligence import YouTubeIntelligence

class DataEngine:
    """Engine 3: Harvests patterns from YouTube and social media"""
    
    def __init__(self, youtube_key):
        self.youtube = YouTubeIntelligence(youtube_key)
        self.patterns = []
    
    def harvest(self, query="business credit funding"):
        """Harvest patterns from YouTube"""
        videos = self.youtube.search_videos(query, max_results=30)
        patterns = self.youtube.extract_patterns(videos)
        
        self.patterns = patterns
        return patterns
    
    def get_summary(self):
        """Return summary of harvested data"""
        if not self.patterns:
            return "No patterns harvested"
        
        lender_count = len(self.patterns.get('lenders_mentioned', []))
        tactic_count = len(self.patterns.get('tactics_discussed', []))
        
        return f"Found {lender_count} lender mentions, {tactic_count} tactics"
