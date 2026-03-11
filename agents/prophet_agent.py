from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
from tools.polymarket import PolymarketConnector

class ProphetAgent(FinancialAgent):
    """The Prophet - Polymarket prediction market trader"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.poly = PolymarketConnector()
    
    async def analyze_predictions(self, market_data: dict) -> TradeSignal:
        btc_price = market_data['price']
        arb = self.poly.analyze_arbitrage(btc_price)
        
        if arb['opportunities']:
            opp = arb['opportunities'][0]  # Best opportunity
            reasoning = f"POLYMARKET: {opp['question'][:40]}... Edge: {opp['edge']*100:.0f}%"
            action = opp['recommendation']
            confidence = min(0.95, opp['edge'] * 2)
        else:
            reasoning = "No Polymarket arbitrage found"
            action = "HOLD"
            confidence = 0.3
        
        return TradeSignal(
            agent_id="prophet",
            exchange=ExchangeType.COINBASE,
            symbol=market_data['symbol'],
            action=action,
            quantity=0.01,
            confidence=confidence,
            reasoning=reasoning
        )
