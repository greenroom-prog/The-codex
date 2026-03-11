import asyncio
from datetime import datetime
from agents.ghost_agent import GhostAgent
from agents.quant_agent import QuantAgent
from agents.vault_agent import VaultAgent
from agents.sentiment_agent import SentimentAgent
from agents.bridge_agent import BridgeAgent
from agents.prophet_agent import ProphetAgent
from agents.sentinel import Sentinel
from core.protocol import AgentConfig, AgentRole, ToolType
from tools.paper_trader import PaperTrader

class Orchestrator:
    def __init__(self, config: dict):
        cfg = AgentConfig(role=AgentRole.CODER, model='claude-sonnet-4-20250514', temperature=0.3, max_iterations=5, allowed_tools=[ToolType.CODE_EXEC], system_prompt="Agent", agent_id="orch")
        self.ghost = GhostAgent(cfg)
        self.quant = QuantAgent(cfg)
        self.vault = VaultAgent(cfg)
        self.sentiment = SentimentAgent(cfg)
        self.bridge = BridgeAgent(cfg)
        self.prophet = ProphetAgent(cfg)
        self.sentinel = Sentinel({'max_drawdown_percent': 10.0, 'max_position_size_percent': 25.0, 'kill_switch_enabled': True, 'initial_capital': 10000.0})
        self.paper_trader = PaperTrader(initial_capital=10000)
        self.capital = 10000.0
        self.positions = []
    
    async def run_cycle(self, market_data: dict):
        print(f"\n{'='*60}\n⚔️  ATLAS CONQUISTADOR MODE - TAKE EVERYTHING\n{'='*60}")
        
        # Run all agents
        g = await self.ghost.find_arbitrage(market_data)
        q = await self.quant.analyze_momentum(market_data)
        v = await self.vault.evaluate_risk(market_data)
        s = await self.sentiment.analyze_with_sentiment(market_data)
        b = await self.bridge.find_cross_chain_arb(market_data)
        p = await self.prophet.analyze_predictions(market_data)
        
        signals = [g, q, v, s, b, p]
        
        # AGGRESSIVE LOGIC: Just 2 votes needed (down from 3)
        buy_votes = sum(1 for sig in signals if sig.action == "BUY")
        sell_votes = sum(1 for sig in signals if sig.action == "SELL")
        
        # Individual agent overrides (high conviction = instant action)
        prophet_override = p.action == "BUY" and p.confidence > 0.7
        quant_override = q.action == "BUY" and q.confidence > 0.8
        
        print(f"\n🗳️  VOTES: {buy_votes} BUY | {sell_votes} SELL")
        
        # EXECUTE AGGRESSIVELY
        if prophet_override:
            print(f"\n💎 PROPHET OVERRIDE: {p.reasoning[:60]}...")
            result = self.paper_trader.execute_trade("BUY", market_data['price'], quantity=0.02)
            print(f"   📝 BOUGHT 0.02 BTC @ ${market_data['price']:,.2f}")
        
        elif buy_votes >= 2:  # LOWERED from 3 to 2
            result = self.paper_trader.execute_trade("BUY", market_data['price'], quantity=0.015)
            print(f"\n📝 CONSENSUS BUY: 0.015 BTC @ ${market_data['price']:,.2f}")
            print(f"   💰 ${result['capital']:,.2f} remaining")
        
        elif sell_votes >= 2 and self.paper_trader.btc_position > 0:  # LOWERED from 3 to 2
            result = self.paper_trader.execute_trade("SELL", market_data['price'])
            print(f"\n📝 CONSENSUS SELL: {result['btc_position']:.4f} BTC @ ${market_data['price']:,.2f}")
            print(f"   💵 P&L: ${result['pnl']:+,.2f}")
            print(f"   💰 ${result['capital']:,.2f} total")
        
        # Quick profit taking: If up 1%+ on position, SELL
        if self.paper_trader.btc_position > 0 and self.paper_trader.trades:
            last_buy = [t for t in self.paper_trader.trades if t['action'] == 'BUY'][-1]
            gain_pct = ((market_data['price'] - last_buy['btc_price']) / last_buy['btc_price']) * 100
            
            if gain_pct > 1.0:  # 1% profit = TAKE IT
                result = self.paper_trader.execute_trade("SELL", market_data['price'])
                print(f"\n💰 PROFIT TAKING: +{gain_pct:.1f}% gain = ${result['pnl']:,.2f}")
        
        # Performance
        perf = self.paper_trader.get_performance()
        print(f"\n⚔️  CONQUISTADOR STATS:")
        print(f"   Raids: {perf['total_trades']}")
        print(f"   Plunder: ${perf['total_pnl']:+,.2f}")
        print(f"   Treasury: ${perf['total_value']:,.2f}")
        print(f"   Conquest: {perf['return_pct']:+.2f}%")
        
        return signals
