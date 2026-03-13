from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig, Message
from tools.multi_exchange import MultiExchange

class GhostAgent(FinancialAgent):
    """The Ghost - Real Arbitrage Hunter across multiple exchanges"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.multi_exchange = MultiExchange()
    
    async def find_arbitrage(self, ticker_data: dict) -> TradeSignal:
        # Get real arbitrage opportunity
        arb = self.multi_exchange.find_arbitrage("BTC/USDT")
        
        if arb['opportunity']:
            reasoning = f"ARBITRAGE: Buy {arb['buy_exchange']} ${arb['buy_price']:,.0f}, Sell {arb['sell_exchange']} ${arb['sell_price']:,.0f}, Net: {arb['net_profit_percent']:.2f}%"
            action = "BUY"
            confidence = min(0.95, arb['net_profit_percent'] / 2)  # Higher profit = higher confidence
        else:
            reasoning = f"No arbitrage: Spread {arb.get('spread_percent', 0):.2f}% < 0.76% fees"
            action = "HOLD"
            confidence = 0.5
        
        return TradeSignal(
            agent_id=self.config.agent_id,
            exchange=ExchangeType.COINBASE,
            symbol=ticker_data['symbol'],
            action=action,
            quantity=0.01,
            confidence=confidence,
            reasoning=reasoning
        )
