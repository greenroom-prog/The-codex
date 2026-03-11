from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig

class VaultAgent(FinancialAgent):
    """Risk + Profit-taking (DYNAMIC)"""
    
    def __init__(self, config):
        super().__init__(FinancialAgentRole.GHOST, config)
    
    async def evaluate_risk(self, market_data):
        btc_price = market_data["price"]
        
        # DYNAMIC: Support trends instead of fighting them
        if btc_price > 71000:
            return TradeSignal(
                agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="SELL", quantity=0.015, confidence=0.78,
                reasoning="PROFIT TAKE: BTC >$71K"
            )
        elif btc_price > 69800:  # NEW: Momentum support
            return TradeSignal(
                agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="BUY", quantity=0.015, confidence=0.72,
                reasoning="MOMENTUM: Strong uptrend"
            )
        elif btc_price < 68000:
            return TradeSignal(
                agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="BUY", quantity=0.025, confidence=0.82,
                reasoning="BUY DIP: BTC <$68K"
            )
        
        return TradeSignal(
            agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
            action="HOLD", quantity=0, confidence=0.58, reasoning="Neutral range"
        )
