from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
import ccxt
import time

class GhostAgent(FinancialAgent):
    """Multi-strategy: CEX arb + Latency + Speed (AGGRESSIVE)"""
    
    def __init__(self, config):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.exchanges = {
            "coinbase": ccxt.coinbase({"enableRateLimit": True}),
            "kraken": ccxt.kraken({"enableRateLimit": True})
        }
    
    async def find_arbitrage(self, market_data):
        signals = []
        
        # STRATEGY 1: CEX Arbitrage (LOWERED: 0.3% from 0.5%)
        try:
            cb = self.exchanges["coinbase"].fetch_ticker("BTC/USD")["last"]
            kr = self.exchanges["kraken"].fetch_ticker("BTC/USD")["last"]
            spread_pct = (abs(cb - kr) / cb) * 100
            
            if spread_pct > 0.3:  # LOWERED threshold
                signals.append(TradeSignal(
                    agent_id="ghost", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                    action="BUY" if cb < kr else "SELL", quantity=0.015,
                    confidence=0.80, reasoning=f"CEX ARB: {spread_pct:.2f}% spread"
                ))
        except: pass
        
        # STRATEGY 2: Latency Arbitrage (AGGRESSIVE: 50ms threshold)
        prices, times = {}, {}
        for name, ex in self.exchanges.items():
            start = time.time()
            try:
                prices[name] = ex.fetch_ticker("BTC/USD")["last"]
                times[name] = (time.time() - start) * 1000
            except: pass
        
        if len(prices) >= 2:
            fastest = min(times, key=times.get)
            slowest = max(times, key=times.get)
            gap = times[slowest] - times[fastest]
            edge = (abs(prices[fastest] - prices[slowest]) / prices[fastest]) * 100
            
            if gap > 50 and edge > 0.02:  # LOWERED: 50ms and 0.02%
                signals.append(TradeSignal(
                    agent_id="ghost", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                    action="BUY", quantity=0.02, confidence=0.88,
                    reasoning=f"SPEED: {gap:.0f}ms edge, {edge:.3f}%"
                ))
        
        # Return best or HOLD
        if signals:
            return max(signals, key=lambda s: s.confidence)
        
        return TradeSignal(
            agent_id="ghost", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
            action="HOLD", quantity=0, confidence=0.5, reasoning="No arb found"
        )
