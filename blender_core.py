from engines.engine1_intelligence import IntelligenceEngine
from engines.engine2_funding import FundingEngine
from engines.engine3_data import DataEngine
from engines.engine4_venture import VentureEngine
from engines.engine5_atlas import AtlasEngine
from datetime import datetime
import json

class ProjectBlender:
    """
    PROJECT BLENDER - The Complete System
    Integrates all 5 engines to form autonomous business intelligence
    """
    
    def __init__(self):
        print("\n" + "="*70)
        print("🔥 PROJECT BLENDER - INITIALIZING")
        print("="*70 + "\n")
        
        # Initialize all 5 engines
        self.engine1 = IntelligenceEngine()
        self.engine2 = FundingEngine()
        self.engine3 = DataEngine("AIzaSyBQ9YGjDy8rF8LERGpooCOECAMyYxa5R8M")
        self.engine4 = VentureEngine()
        self.engine5 = AtlasEngine()
        
        print("✅ Engine 1: Intelligence (Policy Scanner)")
        print("✅ Engine 2: Funding (Capital Mapper)")
        print("✅ Engine 3: Data Harvesting (Pattern Discovery)")
        print("✅ Engine 4: Venture (Opportunity Evaluator)")
        print("✅ Engine 5: Atlas Protocol (Autonomous Agents)")
        print()
    
    def full_system_scan(self):
        """Run complete intelligence scan across all engines"""
        
        print("\n" + "="*70)
        print("🧠 FULL SYSTEM SCAN - PROJECT BLENDER")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'engines': {}
        }
        
        # ENGINE 1: Intelligence
        print("🏛️  ENGINE 1: INTELLIGENCE")
        print("-" * 70)
        intel_signals = self.engine1.scan()
        intel_summary = self.engine1.get_summary()
        print(f"   {intel_summary}")
        if intel_signals:
            for sig in intel_signals[:3]:  # Show top 3
                print(f"   • {sig['source'].upper()}: {sig['title'][:60]}...")
        report['engines']['intelligence'] = {
            'summary': intel_summary,
            'signals': len(intel_signals)
        }
        print()
        
        # ENGINE 2: Funding
        print("💰 ENGINE 2: FUNDING")
        print("-" * 70)
        opportunities = self.engine2.find_opportunities(target_amount=100000)
        print(f"   Found {len(opportunities)} funding opportunities:")
        for opp in opportunities[:3]:  # Top 3
            print(f"   • {opp['lender'].upper()}: ${opp['max_amount']:,} " +
                  f"({opp['approval_rate']}% approval)")
        report['engines']['funding'] = {
            'opportunities': len(opportunities)
        }
        print()
        
        # ENGINE 3: Data Harvesting
        print("📺 ENGINE 3: DATA HARVESTING")
        print("-" * 70)
        print("   Scanning YouTube for business credit patterns...")
        patterns = self.engine3.harvest("business credit 2026")
        summary = self.engine3.get_summary()
        print(f"   {summary}")
        report['engines']['data'] = {
            'summary': summary
        }
        print()
        
        # ENGINE 4: Venture
        print("🚀 ENGINE 4: VENTURE")
        print("-" * 70)
        ventures = self.engine4.rank_opportunities()
        summary = self.engine4.get_summary()
        print(f"   {summary}")
        for name, data in ventures[:3]:  # Top 3
            print(f"   • {name}: {data['score']}/100 score " +
                  f"({data['margin']*100:.0f}% margin, {data['status']})")
        report['engines']['venture'] = {
            'summary': summary,
            'top_venture': ventures[0][0]
        }
        print()
        
        # ENGINE 5: Atlas
        print("⚔️  ENGINE 5: ATLAS PROTOCOL")
        print("-" * 70)
        atlas_status = self.engine5.get_status()
        summary = self.engine5.get_summary()
        print(f"   {summary}")
        if 'error' not in atlas_status:
            print(f"   Capital: ${atlas_status['current_capital']:,.2f}")
            print(f"   P&L: ${atlas_status['total_pnl']:+.2f}")
        report['engines']['atlas'] = atlas_status
        print()
        
        # CORRELATE SIGNALS
        print("🔗 CROSS-ENGINE ANALYSIS")
        print("-" * 70)
        self._correlate_signals(report)
        print()
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blender_report_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Full report saved: {filename}")
        print("="*70 + "\n")
        
        return report
    
    def _correlate_signals(self, report):
        """Find correlations across engines"""
        
        # Check if all systems bullish
        intel = report['engines']['intelligence']['summary']
        atlas_pnl = report['engines']['atlas'].get('total_pnl', 0)
        
        if 'BULLISH' in intel and atlas_pnl > 0:
            print("   🚨 STRONG SIGNAL: Policy bullish + Atlas profitable")
            print("   → Recommendation: Increase Atlas position size")
        elif 'BEARISH' in intel and atlas_pnl < 0:
            print("   ⚠️  WARNING: Policy bearish + Atlas losing")
            print("   → Recommendation: Reduce exposure, wait for clarity")
        elif 'BULLISH' in intel and atlas_pnl < 0:
            print("   🤔 DIVERGENCE: Policy bullish but Atlas struggling")
            print("   → Recommendation: Optimize Atlas strategies")
        else:
            print("   ✅ Systems running normally, no major signals")
    
    def quick_status(self):
        """Quick status check of all engines"""
        print("\n📊 QUICK STATUS - PROJECT BLENDER\n")
        print(f"Engine 1: {self.engine1.get_summary()}")
        print(f"Engine 2: {len(self.engine2.find_opportunities())} funding opportunities")
        print(f"Engine 3: {self.engine3.get_summary()}")
        print(f"Engine 4: {self.engine4.get_summary()}")
        print(f"Engine 5: {self.engine5.get_summary()}")
        print()

if __name__ == "__main__":
    # Initialize Project Blender
    blender = ProjectBlender()
    
    # Run full system scan
    blender.full_system_scan()
