from tools.multi_exchange import MultiExchange

print("🌐 TESTING MULTI-EXCHANGE ARBITRAGE\n")

multi = MultiExchange()

# Get prices from all exchanges
print("📊 Fetching BTC/USDT from all exchanges...")
prices = multi.get_all_prices("BTC/USDT")

for exchange, data in prices.items():
    if 'error' in data:
        print(f"   ❌ {exchange}: {data['error']}")
    else:
        print(f"   ✅ {exchange}: ${data['price']:,.2f}")

# Check for arbitrage
print("\n🔍 Checking for arbitrage opportunities...")
arb = multi.find_arbitrage("BTC/USDT")

if arb['opportunity']:
    print(f"\n💰 ARBITRAGE FOUND!")
    print(f"   Buy on {arb['buy_exchange']}: ${arb['buy_price']:,.2f}")
    print(f"   Sell on {arb['sell_exchange']}: ${arb['sell_price']:,.2f}")
    print(f"   Gross spread: {arb['spread_percent']:.2f}%")
    print(f"   Net profit (after fees): {arb['net_profit_percent']:.2f}%")
else:
    print(f"\n⏸️  No arbitrage opportunity")
    print(f"   Reason: {arb.get('reason', 'Spread too small after fees')}")

print("\n✅ Multi-exchange test complete!")
