import requests
import feedparser
from datetime import datetime
import json

class PowerIntelligence:
    """Track policy makers & market movers"""
    
    def __init__(self):
        self.sources = {
            'cftc': 'https://www.cftc.gov/PressRoom/RSS/rss_pressreleases',
            'sec': 'https://www.sec.gov/news/pressreleases.rss',
            'treasury': 'https://home.treasury.gov/news/press-releases/rss',
            'white_house': 'https://www.whitehouse.gov/feed/',
            'fed': 'https://www.federalreserve.gov/feeds/press_all.xml'
        }
    
    def scan_all_sources(self):
        """Scan all government sources for crypto mentions"""
        print("\n" + "="*70)
        print("🏛️  POWER INTELLIGENCE SCAN")
        print("="*70 + "\n")
        
        all_items = []
        crypto_keywords = ['crypto', 'bitcoin', 'digital asset', 'blockchain', 
                          'virtual currency', 'stablecoin', 'defi']
        
        for source_name, url in self.sources.items():
            try:
                print(f"📡 Scanning {source_name.upper()}...")
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:10]:  # Latest 10
                    title = entry.title.lower()
                    summary = entry.get('summary', '').lower()
                    
                    # Check if crypto-related
                    if any(keyword in title + summary for keyword in crypto_keywords):
                        all_items.append({
                            'source': source_name,
                            'title': entry.title,
                            'date': entry.get('published', 'Unknown'),
                            'link': entry.link
                        })
                        print(f"   🚨 FOUND: {entry.title[:60]}...")
                
            except Exception as e:
                print(f"   ❌ Error scanning {source_name}: {e}")
        
        # Save results
        if all_items:
            print(f"\n✅ Found {len(all_items)} crypto-related announcements\n")
            
            for item in all_items:
                print(f"📰 {item['source'].upper()}: {item['title']}")
                print(f"   🔗 {item['link']}\n")
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"power_intel_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(all_items, f, indent=2)
            
            print(f"💾 Saved to: {filename}")
        else:
            print("📭 No crypto announcements found in recent feeds")
        
        print("\n" + "="*70 + "\n")
        return all_items

if __name__ == "__main__":
    intel = PowerIntelligence()
    intel.scan_all_sources()
