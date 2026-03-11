from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
import ccxt
import time

class GhostAgent(FinancialAgent):
    def __init__(self, config):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.exchanges = {
            "coinbase": ccxt.coinbase({"enableRateLimit": True}),
            "kraken": ccxt.kraken({"enableRateLimit": True})
        }
    
    async def find_arbitrage(self, market_data):
        try:
            cb = self.exchanges["coinbase"].fetch_ticker("BTC/USD")["last"]
            kr = self.exchanges["kraken"].fetch_ticker("BTC/USD")["last"]
            spread = (abs(cb - kr) / cb) * 100
            
            if spread > 0.5:
                return TradeSignal(agent_id="ghost", exchange=ExchangeType.COINBASE, symbol="BTC/USD", action="BUY" if cb < kr else "SELL", quantity=0.01, confidence=0.75, reasoning=f"ARB: {spread:.2f}%")
        except:
            pass
        
        return TradeSignal(agent_id="ghost", exchange=ExchangeType.COINBASE, symbol="BTC/USD", action="HOLD", quantity=0, confidence=0.5, reasoning="No arb")
