import sqlite3
from datetime import datetime

class AtlasBacktest:
    """Analyze Atlas historical performance"""
    
    def __init__(self, db_path='atlas_trades.db'):
        self.db = db_path
        self.initial_capital = 10000
    
    def analyze_performance(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        # Get all cycles with signals
        cursor.execute('''
            SELECT c.timestamp, c.btc_price, c.consensus,
                   GROUP_CONCAT(s.agent_id || ':' || s.action || ':' || s.confidence) as signals
            FROM cycles c
            LEFT JOIN signals s ON DATE(c.timestamp) = DATE(s.timestamp)
            GROUP BY c.id
            ORDER BY c.timestamp
        ''')
        
        cycles = cursor.fetchall()
        
        # Simulate trading
        capital = self.initial_capital
        position = 0  # BTC holdings
        trades = []
        
        for timestamp, btc_price, consensus, signals in cycles:
            if not signals:
                continue
            
            # Count votes
            buy_votes = signals.count(':BUY:')
            sell_votes = signals.count(':SELL:')
            
            # Execute on 3+ consensus (simplified)
            if buy_votes >= 3 and position == 0:
                # Buy 0.1 BTC
                btc_bought = min(0.1, capital / btc_price)
                cost = btc_bought * btc_price
                if cost <= capital:
                    capital -= cost
                    position += btc_bought
                    trades.append(('BUY', timestamp, btc_price, btc_bought))
            
            elif sell_votes >= 3 and position > 0:
                # Sell all
                proceeds = position * btc_price
                capital += proceeds
                trades.append(('SELL', timestamp, btc_price, position))
                position = 0
        
        # Close any open position at current price
        if position > 0:
            cursor.execute('SELECT btc_price FROM cycles ORDER BY timestamp DESC LIMIT 1')
            current_price = cursor.fetchone()[0]
            capital += position * current_price
            trades.append(('CLOSE', 'now', current_price, position))
            position = 0
        
        conn.close()
        
        # Calculate metrics
        total_return = capital - self.initial_capital
        return_pct = (total_return / self.initial_capital) * 100
        
        return {
            'initial_capital': self.initial_capital,
            'final_capital': capital,
            'total_return': total_return,
            'return_pct': return_pct,
            'total_cycles': len(cycles),
            'total_trades': len(trades),
            'trades': trades
        }

# Run backtest
backtest = AtlasBacktest()
results = backtest.analyze_performance()

print("\n" + "="*60)
print("📈 ATLAS BACKTEST RESULTS")
print("="*60)
print(f"Initial Capital:    ${results['initial_capital']:,.2f}")
print(f"Final Capital:      ${results['final_capital']:,.2f}")
print(f"Total Return:       ${results['total_return']:,.2f}")
print(f"Return %:           {results['return_pct']:.2f}%")
print(f"Total Cycles:       {results['total_cycles']}")
print(f"Total Trades:       {results['total_trades']}")

if results['trades']:
    print(f"\n📊 TRADE HISTORY:")
    for action, timestamp, price, amount in results['trades'][-5:]:
        print(f"   {action}: {amount:.4f} BTC @ ${price:,.2f}")

print("\n⚠️  Note: This is simplified simulation, not financial advice!")
print("="*60 + "\n")
