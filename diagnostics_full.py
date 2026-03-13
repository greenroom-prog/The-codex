import asyncio
import sys
from datetime import datetime

print("\n" + "="*70)
print("🔍 ATLAS AGENT DIAGNOSTICS - FULL SYSTEM ANALYSIS")
print("="*70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Test 1: Import all agents
print("1️⃣ TESTING AGENT IMPORTS...")
print("-" * 70)
try:
    from agents.ghost_agent import GhostAgent
    print("✅ Ghost Agent imported")
except Exception as e:
    print(f"❌ Ghost Agent FAILED: {e}")

try:
    from agents.quant_agent import QuantAgent
    print("✅ Quant Agent imported")
except Exception as e:
    print(f"❌ Quant Agent FAILED: {e}")

try:
    from agents.sentiment_agent import SentimentAgent
    print("✅ Sentiment Agent imported")
except Exception as e:
    print(f"❌ Sentiment Agent FAILED: {e}")

try:
    from agents.prophet_agent import ProphetAgent
    print("✅ Prophet Agent imported")
except Exception as e:
    print(f"❌ Prophet Agent FAILED: {e}")

try:
    from agents.bridge_agent import BridgeAgent
    print("✅ Bridge Agent imported")
except Exception as e:
    print(f"❌ Bridge Agent FAILED: {e}")

try:
    from agents.vault_agent import VaultAgent
    print("✅ Vault Agent imported")
except Exception as e:
    print(f"❌ Vault Agent FAILED: {e}")

try:
    from agents.orchestrator import Orchestrator
    print("✅ Orchestrator imported")
except Exception as e:
    print(f"❌ Orchestrator FAILED: {e}")

# Test 2: Test each agent's methods
print("\n2️⃣ TESTING AGENT METHODS...")
print("-" * 70)

from core.protocol import AgentConfig, AgentRole, ToolType

config = AgentConfig(
    role=AgentRole.CODER,
    model='claude-sonnet-4-20250514',
    temperature=0.3,
    max_iterations=5,
    allowed_tools=[ToolType.CODE_EXEC],
    system_prompt="Test",
    agent_id="test"
)

market_data = {'symbol': 'BTC/USD', 'price': 70000}

async def test_agents():
    # Ghost
    try:
        from agents.ghost_agent import GhostAgent
        ghost = GhostAgent(config)
        signal = await ghost.find_arbitrage(market_data)
        print(f"✅ Ghost: {signal.action} - {signal.reasoning[:50]}...")
    except Exception as e:
        print(f"❌ Ghost execution FAILED: {e}")
    
    # Quant
    try:
        from agents.quant_agent import QuantAgent
        quant = QuantAgent(config)
        signal = await quant.analyze_momentum(market_data)
        print(f"✅ Quant: {signal.action} - {signal.reasoning[:50]}...")
    except Exception as e:
        print(f"❌ Quant execution FAILED: {e}")
    
    # Sentiment
    try:
        from agents.sentiment_agent import SentimentAgent
        sentiment = SentimentAgent(config)
        signal = await sentiment.analyze_with_sentiment(market_data)
        print(f"✅ Sentiment: {signal.action} - {signal.reasoning[:50]}...")
    except Exception as e:
        print(f"❌ Sentiment execution FAILED: {e}")
    
    # Prophet
    try:
        from agents.prophet_agent import ProphetAgent
        prophet = ProphetAgent(config)
        signal = await prophet.analyze_predictions(market_data)
        print(f"✅ Prophet: {signal.action} - {signal.reasoning[:50]}...")
    except Exception as e:
        print(f"❌ Prophet execution FAILED: {e}")
    
    # Bridge
    try:
        from agents.bridge_agent import BridgeAgent
        bridge = BridgeAgent(config)
        signal = await bridge.find_cross_chain_arb(market_data)
        print(f"✅ Bridge: {signal.action} - {signal.reasoning[:50]}...")
    except Exception as e:
        print(f"❌ Bridge execution FAILED: {e}")
    
    # Vault
    try:
        from agents.vault_agent import VaultAgent
        vault = VaultAgent(config)
        signal = await vault.evaluate_risk(market_data)
        print(f"✅ Vault: {signal.action} - {signal.reasoning[:50]}...")
    except Exception as e:
        print(f"❌ Vault execution FAILED: {e}")

asyncio.run(test_agents())

# Test 3: Tool connectivity
print("\n3️⃣ TESTING TOOL CONNECTIVITY...")
print("-" * 70)

try:
    from tools.exchange_connector import ExchangeConnector
    ex = ExchangeConnector('coinbase')
    price = ex.get_price('BTC/USD')
    print(f"✅ Exchange Connector: BTC = ${price:,.2f}")
except Exception as e:
    print(f"❌ Exchange Connector FAILED: {e}")

try:
    from tools.twitter_sentiment import TwitterSentiment
    tw = TwitterSentiment()
    result = tw.analyze_sentiment()
    print(f"✅ Twitter Sentiment: {result['sentiment']} ({result['score']:.2f})")
except Exception as e:
    print(f"❌ Twitter Sentiment FAILED: {e}")

try:
    from tools.whale_tracker import WhaleTracker
    wh = WhaleTracker()
    result = wh.analyze_whale_activity()
    print(f"✅ Whale Tracker: {result['whale_count']} whales, {result['signal']}")
except Exception as e:
    print(f"❌ Whale Tracker FAILED: {e}")

try:
    from tools.order_book import OrderBookAnalyzer
    ob = OrderBookAnalyzer()
    result = ob.get_order_book_depth()
    print(f"✅ Order Book: {result['signal']} (ratio: {result['pressure_ratio']:.2f})")
except Exception as e:
    print(f"❌ Order Book FAILED: {e}")

try:
    from tools.polymarket import PolymarketConnector
    poly = PolymarketConnector()
    markets = poly.get_crypto_markets()
    print(f"✅ Polymarket: {len(markets)} markets found")
except Exception as e:
    print(f"❌ Polymarket FAILED: {e}")

try:
    from tools.cross_chain import CrossChainMonitor
    cc = CrossChainMonitor()
    result = cc.find_cross_chain_arbitrage()
    print(f"✅ Cross-chain: {result.get('has_arbitrage', False)}")
except Exception as e:
    print(f"❌ Cross-chain FAILED: {e}")

# Test 4: Database
print("\n4️⃣ TESTING DATABASE...")
print("-" * 70)

import sqlite3
try:
    conn = sqlite3.connect('atlas_trades.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM cycles")
    cycles = cursor.fetchone()[0]
    print(f"✅ Database: {cycles} cycles logged")
    
    cursor.execute("SELECT COUNT(*) FROM signals")
    signals = cursor.fetchone()[0]
    print(f"✅ Database: {signals} signals logged")
    
    cursor.execute("SELECT COUNT(*) FROM paper_trades")
    trades = cursor.fetchone()[0]
    print(f"✅ Database: {trades} paper trades logged")
    
    conn.close()
except Exception as e:
    print(f"❌ Database FAILED: {e}")

# Test 5: Orchestrator integration
print("\n5️⃣ TESTING ORCHESTRATOR...")
print("-" * 70)

async def test_orchestrator():
    try:
        from agents.orchestrator import Orchestrator
        orch = Orchestrator({'model': 'claude-sonnet-4-20250514'})
        signals = await orch.run_cycle(market_data)
        print(f"✅ Orchestrator: Generated {len(signals)} signals")
        
        buy_votes = sum(1 for s in signals if s.action == "BUY")
        sell_votes = sum(1 for s in signals if s.action == "SELL")
        hold_votes = sum(1 for s in signals if s.action == "HOLD")
        
        print(f"   📊 Votes: {buy_votes} BUY | {sell_votes} SELL | {hold_votes} HOLD")
    except Exception as e:
        print(f"❌ Orchestrator FAILED: {e}")

asyncio.run(test_orchestrator())

print("\n" + "="*70)
print("✅ DIAGNOSTICS COMPLETE")
print("="*70 + "\n")
