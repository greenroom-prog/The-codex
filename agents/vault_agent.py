from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig, Message

class VaultAgent(FinancialAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(FinancialAgentRole.VAULT, config)
    
    async def evaluate_risk(self, market_data: dict) -> TradeSignal:
        prompt = f"VAULT: {market_data['symbol']} ${market_data['price']}. Risk? SELL/HOLD + why."
        analysis = await self.llm.generate(messages=[Message(role="user", content=prompt)], response_model=None)
        action = "SELL" if "SELL" in analysis.upper() else "HOLD"
        return TradeSignal(agent_id=self.config.agent_id, exchange=ExchangeType.COINBASE, symbol=market_data['symbol'], action=action, quantity=0.01, confidence=0.9, reasoning=analysis[:200])
