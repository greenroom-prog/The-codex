import sqlite3
from datetime import datetime

class AtlasEngine:
    """Engine 5: Autonomous trading agents (already running)"""
    
    def __init__(self, db_path='atlas_trades.db'):
        self.db_path = db_path
    
    def get_status(self):
        """Get current Atlas performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Get latest stats
            c.execute("SELECT COUNT(*) FROM paper_trades")
            total_trades = c.fetchone()[0]
            
            c.execute("SELECT SUM(pnl) FROM paper_trades")
            total_pnl = c.fetchone()[0] or 0
            
            c.execute("SELECT capital_after FROM paper_trades ORDER BY id DESC LIMIT 1")
            result = c.fetchone()
            current_capital = result[0] if result else 10000
            
            conn.close()
            
            return {
                'status': 'ACTIVE',
                'total_trades': total_trades,
                'total_pnl': round(total_pnl, 2),
                'current_capital': round(current_capital, 2),
                'agents': 6
            }
        except Exception as e:
            return {
                'status': 'UNKNOWN',
                'error': str(e)
            }
    
    def get_summary(self):
        """Return Atlas summary"""
        status = self.get_status()
        if 'error' in status:
            return f"Atlas: {status['status']}"
        
        pnl = status['total_pnl']
        trades = status['total_trades']
        return f"Atlas: {trades} trades, ${pnl} P&L"
