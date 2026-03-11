from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
from tools.order_book import OrderBookAnalyzer

class QuantAgent(FinancialAgent):
    """Enhanced with Order Book depth analysis"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.order_book = OrderBookAnalyzer()
    
    async def analyze_momentum(self, market_data: dict) -> TradeSignal:
        btc_price = market_data['price']
        
        # Get order book pressure
        book_data = self.order_book.get_order_book_depth()
        
        # Analyze momentum + order flow
        pressure_ratio = book_data['pressure_ratio']
        book_signal = book_data['signal']
        
        if btc_price > 70000 and pressure_ratio > 1.2:
            action = "BUY"
            confidence = 0.80
            reasoning = f"MOMENTUM: BTC ${btc_price:,.0f} + {book_signal} (ratio: {pressure_ratio:.2f})"
        elif btc_price < 68000 or pressure_ratio < 0.8:
            action = "SELL"
            confidence = 0.75
            reasoning = f"WEAKNESS: BTC ${btc_price:,.0f} + {book_signal} (ratio: {pressure_ratio:.2f})"
        else:
            action = "HOLD"
            confidence = 0.60
            reasoning = f"RANGE: BTC ${btc_price:,.0f} + {book_signal}"
        
        return TradeSignal(
            agent_id="quant",
            exchange=ExchangeType.COINBASE,
            symbol=market_data['symbol'],
            action=action,
            quantity=0.01,
            confidence=confidence,
            reasoning=reasoning
        )
