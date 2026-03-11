from tools.exchange_connector import ExchangeConnector

print("🔌 Testing Coinbase Connection\n")

exchange = ExchangeConnector("coinbase")

print("📊 Fetching BTC/USDT price...")
ticker = exchange.get_ticker("BTC/USDT")

if 'error' in ticker:
    print(f"❌ Error: {ticker['error']}")
else:
    print(f"✅ BTC Price: ${ticker['price']:,.2f}")
    change = ticker['change_24h'] or 0.0
    volume = ticker['volume'] or 0.0
    print(f"   24h Change: {change:.2f}%")
    print(f"   Volume: {volume:,.0f} BTC")

print("\n✅ Exchange connector working!")
