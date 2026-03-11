import sqlite3
from datetime import datetime

class PaperTrader:
    """Simulates trades without executing them"""
    
    def __init__(self, initial_capital=10000):
        self.capital = initial_capital
        self.btc_position = 0
        self.trades = []
        self.db = sqlite3.connect('atlas_trades.db')
        self._init_db()
    
    def _init_db(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS paper_trades (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                action TEXT,
                btc_price REAL,
                quantity REAL,
                value REAL,
                capital_after REAL,
                btc_position REAL,
                pnl REAL
            )
        ''')
        self.db.commit()
    
    def execute_trade(self, action, btc_price, quantity=0.01):
        """Simulate a trade"""
        pnl = 0
        
        if action == "BUY" and self.btc_position == 0:
            cost = quantity * btc_price
            if cost <= self.capital:
                self.capital -= cost
                self.btc_position += quantity
                value = cost
        
        elif action == "SELL" and self.btc_position > 0:
            proceeds = self.btc_position * btc_price
            self.capital += proceeds
            # Calculate P&L
            if self.trades:
                last_buy = [t for t in self.trades if t['action'] == 'BUY'][-1]
                buy_price = last_buy['btc_price']
                pnl = (btc_price - buy_price) * self.btc_position
            value = proceeds
            self.btc_position = 0
        
        else:
            value = 0
        
        # Log the trade
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO paper_trades 
            (timestamp, action, btc_price, quantity, value, capital_after, btc_position, pnl)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            action,
            btc_price,
            quantity,
            value,
            self.capital,
            self.btc_position,
            pnl
        ))
        self.db.commit()
        
        self.trades.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'btc_price': btc_price,
            'quantity': quantity,
            'value': value,
            'pnl': pnl
        })
        
        return {
            'executed': True,
            'action': action,
            'price': btc_price,
            'capital': self.capital,
            'btc_position': self.btc_position,
            'pnl': pnl
        }
    
    def get_performance(self):
        """Get paper trading performance stats"""
        cursor = self.db.cursor()
        cursor.execute('SELECT COUNT(*), SUM(pnl) FROM paper_trades WHERE action="SELL"')
        trades, total_pnl = cursor.fetchone()
        
        total_value = self.capital + (self.btc_position * self.trades[-1]['btc_price'] if self.trades else 0)
        return_pct = ((total_value - 10000) / 10000) * 100
        
        return {
            'total_trades': trades or 0,
            'total_pnl': total_pnl or 0,
            'current_capital': self.capital,
            'btc_position': self.btc_position,
            'total_value': total_value,
            'return_pct': return_pct
        }
