from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig

class VaultAgent(FinancialAgent):
    def __init__(self, config):
        super().__init__(FinancialAgentRole.GHOST, config)
    
    async def evaluate_risk(self, market_data):
        btc_price = market_data["price"]
        
        if btc_price > 72000:
            return TradeSignal(agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD", action="SELL", quantity=0.01, confidence=0.75, reasoning="PROFIT TAKE: BTC >2K")
        elif btc_price < 67000:
            return TradeSignal(agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD", action="BUY", quantity=0.02, confidence=0.80, reasoning="BUY DIP: BTC <7K")
        
        return TradeSignal(agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD", action="HOLD", quantity=0, confidence=0.6, reasoning="Risk neutral")
