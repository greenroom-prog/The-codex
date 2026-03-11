from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
from tools.twitter_sentiment import TwitterSentiment
from tools.whale_tracker import WhaleTracker

class SentimentAgent(FinancialAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.twitter = TwitterSentiment()
        self.whales = WhaleTracker()
    
    async def analyze_with_sentiment(self, market_data: dict) -> TradeSignal:
        twitter_data = self.twitter.analyze_sentiment()
        whale_data = self.whales.analyze_whale_activity()
        twitter_score = twitter_data['score']
        whale_signal = whale_data['signal']
        
        # LOWERED thresholds from 0.2 to 0.05
        if twitter_score > 0.05 and whale_signal == 'WHALE_ACCUMULATION':
            action = "BUY"
            confidence = 0.65
            reasoning = f"BULLISH: Twitter {twitter_data['bullish_pct']:.0f}% + Whales {whale_data['total_btc_moved']:.0f} BTC"
        elif twitter_score < -0.05 and whale_signal == 'HIGH_VOLATILITY':
            action = "SELL"
            confidence = 0.60
            reasoning = f"BEARISH: Twitter {twitter_data['bearish_pct']:.0f}% + {whale_data['whale_count']} whales"
        else:
            action = "HOLD"
            confidence = 0.5
            reasoning = f"NEUTRAL: Twitter {twitter_data['sentiment']}, Whales {whale_signal}"
        
        return TradeSignal(agent_id="sentiment", exchange=ExchangeType.COINBASE, symbol=market_data['symbol'], action=action, quantity=0.01, confidence=confidence, reasoning=reasoning)
