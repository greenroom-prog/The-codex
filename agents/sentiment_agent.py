from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
from tools.twitter_sentiment import TwitterSentiment
from tools.whale_tracker import WhaleTracker

class SentimentAgent(FinancialAgent):
    """Twitter + Whales (AGGRESSIVE)"""
    
    def __init__(self, config):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.twitter = TwitterSentiment()
        self.whales = WhaleTracker()
    
    async def analyze_with_sentiment(self, market_data):
        tw = self.twitter.analyze_sentiment()
        wh = self.whales.analyze_whale_activity()
        
        # CRITICAL: If whales accumulating, OVERRIDE bearish Twitter
        if wh["signal"] == "WHALE_ACCUMULATION":
            return TradeSignal(
                agent_id="sentiment", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="BUY", quantity=0.025, confidence=0.90,
                reasoning=f"WHALES: {wh['total_btc_moved']:.0f} BTC accumulating (override Twitter)"
            )
        
        # LOWERED: 0.05 from 0.1
        if tw["score"] > 0.05:
            return TradeSignal(
                agent_id="sentiment", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="BUY", quantity=0.02, confidence=0.78,
                reasoning=f"BULLISH: Twitter {tw['bullish_pct']:.0f}%"
            )
        elif tw["score"] < -0.05:
            return TradeSignal(
                agent_id="sentiment", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="SELL", quantity=0.015, confidence=0.72,
                reasoning=f"BEARISH: Twitter {tw['bearish_pct']:.0f}%"
            )
        
        return TradeSignal(
            agent_id="sentiment", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
            action="HOLD", quantity=0, confidence=0.5, reasoning="Neutral"
        )
