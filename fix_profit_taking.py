import sqlite3

conn = sqlite3.connect('atlas_trades.db')
cursor = conn.cursor()

# Check current position
cursor.execute("SELECT btc_position, capital_after FROM paper_trades ORDER BY id DESC LIMIT 1")
position, capital = cursor.fetchone()

print(f"Current position: {position} BTC")
print(f"Capital: ${capital:,.2f}")

# Get average entry price
cursor.execute("SELECT AVG(btc_price) FROM paper_trades WHERE action='BUY' AND btc_position > 0")
avg_entry = cursor.fetchone()[0]

print(f"Average entry: ${avg_entry:,.2f}")

# Current BTC price
from tools.exchange_connector import ExchangeConnector
ex = ExchangeConnector('coinbase')
current = ex.get_price('BTC/USD')

profit_pct = ((current - avg_entry) / avg_entry) * 100

print(f"Current price: ${current:,.2f}")
print(f"Profit: {profit_pct:+.2f}%")

if profit_pct > 0.5:
    print(f"\n✅ SHOULD SELL! {profit_pct:.2f}% profit available")
else:
    print(f"\n⏳ HOLD: Only {profit_pct:.2f}% profit")

conn.close()
