import asyncio
from datetime import datetime
from typing import Optional, List
from core.protocol import AgentConfig, AgentState, Message
from core.financial_protocol import (
    FinancialAgentRole, TradeSignal, PositionState, 
    RiskMetrics, ExchangeType
)
from core.llm_engine import LLMEngine
import json

class FinancialAgent:
    """Specialized financial trading agent"""
    
    def __init__(self, role: FinancialAgentRole, config: AgentConfig):
        self.role = role
        self.config = config
        self.llm = LLMEngine(config)
        self.state = AgentState(config=config)
        self.positions: List[PositionState] = []
        
    async def analyze_market(self, market_data: dict) -> TradeSignal:
        """Analyze market and generate trading signal"""
        
        prompt = self._build_analysis_prompt(market_data)
        
        # Ask Claude to analyze
        analysis = await self.llm.generate(
            messages=[Message(role="user", content=prompt)],
            response_model=None
        )
        
        # Parse the response into a signal
        signal = self._parse_signal(analysis, market_data)
        return signal
    
    def _build_analysis_prompt(self, market_data: dict) -> str:
        """Build role-specific analysis prompt"""
        
        base_data = f"""
Market Data:
- Symbol: {market_data.get('symbol', 'Unknown')}
- Current Price: ${market_data.get('price', 0)}
- 24h Volume: ${market_data.get('volume', 0)}
- 24h Change: {market_data.get('change_24h', 0)}%
"""
        
        if self.role == FinancialAgentRole.GHOST:
            return f"""{base_data}

You are THE GHOST - an arbitrage hunter.
Your job: Find price discrepancies between exchanges.

Analyze this data and respond with:
1. ACTION: BUY, SELL, or HOLD
2. CONFIDENCE: 0.0 to 1.0
3. REASONING: One sentence explaining why

Focus on: Speed and risk-free opportunities only."""

        elif self.role == FinancialAgentRole.QUANT:
            return f"""{base_data}

You are THE QUANT - a momentum trader.
Your job: Execute high-frequency trend-following strategies.

Analyze this data and respond with:
1. ACTION: BUY, SELL, or HOLD
2. CONFIDENCE: 0.0 to 1.0
3. REASONING: One sentence explaining the trend

Focus on: Order flow patterns and explosive momentum."""

        elif self.role == FinancialAgentRole.VAULT:
            return f"""{base_data}

You are THE VAULT - the risk-off defender.
Your job: Preserve capital during volatility.

Analyze this data and respond with:
1. ACTION: BUY, SELL, or HOLD
2. CONFIDENCE: 0.0 to 1.0
3. REASONING: One sentence about risk

Focus on: Moving to safety (BTC, stablecoins) when markets are unstable."""

        else:
            return base_data
    
    def _parse_signal(self, analysis: str, market_data: dict) -> TradeSignal:
        """Parse Claude's analysis into a TradeSignal"""
        
        # Simple parsing - look for keywords
        action = "HOLD"
        confidence = 0.5
        
        if "BUY" in analysis.upper():
            action = "BUY"
            confidence = 0.7
        elif "SELL" in analysis.upper():
            action = "SELL"
            confidence = 0.7
            
        return TradeSignal(
            agent_id=self.config.agent_id,
            exchange=ExchangeType.KUCOIN,
            symbol=market_data.get('symbol', 'BTC/USDT'),
            action=action,
            quantity=0.01,  # Start small
            confidence=confidence,
            reasoning=analysis[:200]  # First 200 chars
        )
