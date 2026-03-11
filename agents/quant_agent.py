from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
from tools.order_book import OrderBookAnalyzer

class QuantAgent(FinancialAgent):
    """Momentum + Order Flow (AGGRESSIVE)"""
    
    def __init__(self, config):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.order_book = OrderBookAnalyzer()
    
    async def analyze_momentum(self, market_data):
        btc_price = market_data["price"]
        book = self.order_book.get_order_book_depth()
        ratio = book["pressure_ratio"]
        
        # AGGRESSIVE: 0.8x and 1.1x thresholds (was 0.8x and 1.2x)
        if btc_price > 69500 and ratio > 1.1:  # LOWERED
            return TradeSignal(
                agent_id="quant", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="BUY", quantity=0.018, confidence=0.85,
                reasoning=f"MOMENTUM: ${btc_price:,.0f} + BUY pressure {ratio:.2f}x"
            )
        elif btc_price < 68500 or ratio < 0.85:  # RAISED (more sensitive)
            return TradeSignal(
                agent_id="quant", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="SELL", quantity=0.012, confidence=0.80,
                reasoning=f"WEAKNESS: ${btc_price:,.0f} + pressure {ratio:.2f}x"
            )
        
        return TradeSignal(
            agent_id="quant", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
            action="HOLD", quantity=0, confidence=0.55, reasoning="Neutral"
        )
