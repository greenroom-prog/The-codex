from tools.cross_chain import CrossChainMonitor

print("🌉 TESTING CROSS-CHAIN ARBITRAGE\n")

monitor = CrossChainMonitor()

# Get USDC prices across chains
print("📊 USDC prices across chains:")
prices = monitor.get_stablecoin_prices()
for chain, price in prices.items():
    print(f"   {chain.upper()}: ${price:.6f}")

# Check for arbitrage
print("\n🔍 Checking for cross-chain arbitrage...")
arb = monitor.find_cross_chain_arbitrage()

if arb['opportunity']:
    print(f"\n💰 CROSS-CHAIN ARBITRAGE FOUND!")
    print(f"   Buy on {arb['buy_chain']}: ${arb['buy_price']:.6f}")
    print(f"   Sell on {arb['sell_chain']}: ${arb['sell_price']:.6f}")
    print(f"   Gross spread: {arb['spread_bps']:.1f} basis points")
    print(f"   Net profit (after bridge): {arb['net_profit_bps']:.1f} bps")
else:
    print(f"\n⏸️  No arbitrage opportunity")
    print(f"   Spread: {arb['spread_bps']:.1f} bps (need >15 bps after fees)")

print("\n✅ Cross-chain test complete!")
