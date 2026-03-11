import ccxt

exchange = ccxt.coinbase({
    'apiKey': 'organizations/7746d813-52e1-4a67-898e-8df4662673ed/apiKeys/6ef9bc8b-0d45-4174-bc2c-c9fa5de5e72a',
    'secret': '-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEILnNBHNJQ/HXu5RH9Ai24tj6NFaeY37Sh3BRbMGN/t9+oAoGCCqGSM49\nAwEHoUQDQgAE2ERa1sStm5CjwFmug3C9THN+/Nj1I33XoCnQCPyzqJ9xYNlwO8Xa\n2gspkkIueko0m4OFzw+iFs6cQiG6rONQHg==\n-----END EC PRIVATE KEY-----',
    'enableRateLimit': True
})

print('\n🔌 Testing Coinbase API...\n')

balance = exchange.fetch_balance()
ticker = exchange.fetch_ticker('BTC/USD')

print(f"💰 USD: ${balance['total'].get('USD', 0):,.2f}")
print(f"💰 BTC: {balance['total'].get('BTC', 0):.8f}")
print(f"📊 BTC: ${ticker['last']:,.2f}")
print('\n✅ CONNECTED!\n')
