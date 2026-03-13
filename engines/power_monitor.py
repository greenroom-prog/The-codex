import time
from power_intelligence import PowerIntelligence
from datetime import datetime

class PowerMonitor:
    """Continuously monitors policy makers for crypto signals"""
    
    def __init__(self, check_interval=1800):  # 30 minutes
        self.intel = PowerIntelligence()
        self.check_interval = check_interval
        self.last_items = []
    
    def monitor_forever(self):
        """Run continuous monitoring"""
        print(f"\n🔄 Power Monitor Started")
        print(f"   Checking every {self.check_interval/60:.0f} minutes")
        print(f"   Watching: CFTC, SEC, Treasury, White House, Fed\n")
        
        cycle = 0
        while True:
            cycle += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n[{timestamp}] Cycle {cycle}: Scanning...")
            
            items = self.intel.scan_all_sources()
            
            # Check for NEW items (not seen before)
            new_items = [item for item in items if item not in self.last_items]
            
            if new_items:
                print(f"\n🚨 NEW ANNOUNCEMENTS DETECTED! ({len(new_items)})")
                for item in new_items:
                    print(f"\n📰 {item['source'].upper()}")
                    print(f"   {item['title']}")
                    print(f"   🔗 {item['link']}")
                
                # TODO: Send to Atlas for auto-trading
                # TODO: Send alert to your phone
                
            else:
                print("✅ No new announcements")
            
            self.last_items = items
            
            print(f"\n⏳ Sleeping {self.check_interval/60:.0f} minutes...")
            time.sleep(self.check_interval)

if __name__ == "__main__":
    monitor = PowerMonitor(check_interval=1800)  # 30 min
    monitor.monitor_forever()
