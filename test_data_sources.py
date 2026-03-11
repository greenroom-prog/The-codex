from tools.twitter_sentiment import TwitterSentiment
from tools.whale_tracker import WhaleTracker
from tools.order_book import OrderBookAnalyzer

print("🔍 TESTING ALL 3 DATA SOURCES\n")
print("="*60)

# 1. Twitter Sentiment
print("\n📱 TWITTER SENTIMENT:")
twitter = TwitterSentiment()
sentiment = twitter.analyze_sentiment()
print(f"   Overall: {sentiment['sentiment']}")
print(f"   Score: {sentiment['score']:.3f}")
print(f"   Bullish: {sentiment['bullish_pct']:.0f}%")
print(f"   Bearish: {sentiment['bearish_pct']:.0f}%")
print(f"   Real Data: {sentiment['using_real_data']}")

# 2. Whale Tracker
print("\n🐋 WHALE TRACKER:")
whales = WhaleTracker()
activity = whales.analyze_whale_activity()
print(f"   Active Whales: {activity['whale_count']}")
print(f"   BTC Moved: {activity['total_btc_moved']:.1f} BTC")
print(f"   USD Value: ${activity['total_usd_value']:,.0f}")
print(f"   Signal: {activity['signal']}")

# 3. Order Book
print("\n📊 ORDER BOOK DEPTH (Coinbase):")
book = OrderBookAnalyzer()
depth = book.get_order_book_depth()
print(f"   Buy Pressure: ${depth['bid_value_usd']:,.0f}")
print(f"   Sell Pressure: ${depth['ask_value_usd']:,.0f}")
print(f"   Ratio: {depth['pressure_ratio']:.2f}")
print(f"   Signal: {depth['signal']}")
print(f"   Spread: ${depth['spread']:.2f}")

print("\n" + "="*60)
print("✅ ALL 3 DATA SOURCES OPERATIONAL!")
