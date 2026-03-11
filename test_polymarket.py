from tools.polymarket import PolymarketConnector

print("🎲 TESTING POLYMARKET INTEGRATION\n")

poly = PolymarketConnector()

# Get crypto markets
print("📊 Crypto Prediction Markets:")
markets = poly.get_crypto_markets()
for m in markets[:3]:
    print(f"   • {m['question']}")
    print(f"     Probability: {m['yes_price']*100:.0f}% | Volume: ${m['volume']:,}")

# Analyze arbitrage (BTC at $70K)
print("\n🔍 Arbitrage Analysis (BTC @ $70,000):")
arb = poly.analyze_arbitrage(70000)

if arb['opportunities']:
    for opp in arb['opportunities']:
        print(f"\n💰 OPPORTUNITY FOUND!")
        print(f"   {opp['question']}")
        print(f"   Market says: {opp['market_price']*100:.0f}% chance")
        print(f"   BTC needs: {opp['required_gain']:.1f}% gain")
        print(f"   Edge: {opp['edge']*100:.0f}%")
        print(f"   → {opp['recommendation']}")
else:
    print("   No clear arbitrage opportunities")

print(f"\n✅ Analyzed {arb['total_markets']} markets")
