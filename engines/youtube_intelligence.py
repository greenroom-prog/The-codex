from googleapiclient.discovery import build
import json
from datetime import datetime

class YouTubeIntelligence:
    """Engine 3: Scrapes YouTube for business intelligence patterns"""
    
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.api_key = api_key
    
    def search_videos(self, query, max_results=50):
        """Search YouTube for videos on a topic"""
        try:
            request = self.youtube.search().list(
                q=query,
                part="snippet",
                maxResults=max_results,
                type="video",
                order="relevance"
            )
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                video = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'published': item['snippet']['publishedAt'],
                    'description': item['snippet']['description']
                }
                videos.append(video)
            
            return videos
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def extract_patterns(self, videos, pattern_type="lenders"):
        """Extract intelligence patterns from video metadata"""
        patterns = {
            'lenders_mentioned': [],
            'tactics_discussed': [],
            'approval_requirements': [],
            'success_stories': []
        }
        
        # Analyze titles and descriptions for patterns
        for video in videos:
            text = (video['title'] + " " + video['description']).lower()
            
            # Find lender mentions
            lenders = ['nav', 'bluevine', 'fundbox', 'brex', 'kabbage', 
                      'american express', 'chase', 'capital one', 'wells fargo']
            for lender in lenders:
                if lender in text:
                    patterns['lenders_mentioned'].append({
                        'lender': lender,
                        'video': video['title'],
                        'channel': video['channel']
                    })
            
            # Find tactics
            tactics = ['no doc', 'no tax returns', 'soft pull', 'stacking', 
                      'shelf corporation', 'tradelines', 'paydex']
            for tactic in tactics:
                if tactic in text:
                    patterns['tactics_discussed'].append({
                        'tactic': tactic,
                        'video': video['title'],
                        'video_id': video['video_id']
                    })
        
        return patterns
    
    def intelligence_report(self, query):
        """Generate full intelligence report"""
        print(f"\n{'='*70}")
        print(f"🎥 YOUTUBE INTELLIGENCE REPORT: {query}")
        print(f"{'='*70}\n")
        
        # Search videos
        videos = self.search_videos(query, max_results=50)
        print(f"📊 Found {len(videos)} videos\n")
        
        # Extract patterns
        patterns = self.extract_patterns(videos)
        
        # Report lenders
        print(f"🏦 LENDERS MENTIONED ({len(patterns['lenders_mentioned'])} times):")
        lender_counts = {}
        for item in patterns['lenders_mentioned']:
            lender = item['lender']
            lender_counts[lender] = lender_counts.get(lender, 0) + 1
        
        for lender, count in sorted(lender_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {lender}: {count} mentions")
        
        # Report tactics
        print(f"\n💡 TACTICS DISCUSSED ({len(patterns['tactics_discussed'])} times):")
        tactic_counts = {}
        for item in patterns['tactics_discussed']:
            tactic = item['tactic']
            tactic_counts[tactic] = tactic_counts.get(tactic, 0) + 1
        
        for tactic, count in sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {tactic}: {count} mentions")
        
        # Save raw data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"intel_{query.replace(' ', '_')}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'query': query,
                'videos': videos,
                'patterns': patterns,
                'timestamp': timestamp
            }, f, indent=2)
        
        print(f"\n💾 Full data saved: {filename}")
        print(f"{'='*70}\n")
        
        return patterns

# Test it
if __name__ == "__main__":
    api_key = "AIzaSyBQ9YGjDy8rF8LERGpooCOECAMyYxa5R8M"
    intel = YouTubeIntelligence(api_key)
    
    # Run intelligence gathering
    intel.intelligence_report("business credit funding 2024")
