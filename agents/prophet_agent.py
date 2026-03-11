from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
from tools.polymarket import PolymarketConnector

class ProphetAgent(FinancialAgent):
    """Polymarket edges (AGGRESSIVE: 8% threshold)"""
    
    def __init__(self, config):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.poly = PolymarketConnector()
    
    async def analyze_predictions(self, market_data):
        try:
            btc_price = market_data["price"]
            result = self.poly.analyze_arbitrage(btc_price)
            
            # LOWERED: 8% from 15%
            if result.get("has_arbitrage") and result.get("edge_pct", 0) > 8:
                return TradeSignal(
                    agent_id="prophet", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                    action="BUY", quantity=0.03, confidence=0.92,
                    reasoning=f"POLYMARKET: {result.get('edge_pct', 0):.0f}% edge"
                )
        except: pass
        
        return TradeSignal(
            agent_id="prophet", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
            action="HOLD", quantity=0, confidence=0.5, reasoning="No edge"
        )
