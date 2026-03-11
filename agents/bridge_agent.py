from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
from tools.cross_chain import CrossChainMonitor

class BridgeAgent(FinancialAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.cross_chain = CrossChainMonitor()
    
    async def find_cross_chain_arb(self, market_data: dict) -> TradeSignal:
        arb = self.cross_chain.find_cross_chain_arbitrage()
        
        if arb['opportunity']:
            reasoning = f"CROSS-CHAIN: {arb['buy_chain']}->{arb['sell_chain']} {arb['net_profit_bps']:.1f}bps"
            action = "BUY"
            confidence = 0.8
        else:
            reasoning = f"No arb: {arb['spread_bps']:.1f}bps"
            action = "HOLD"
            confidence = 0.3
        
        return TradeSignal(
            agent_id="bridge",
            exchange=ExchangeType.COINBASE,
            symbol=market_data['symbol'],
            action=action,
            quantity=0.01,
            confidence=confidence,
            reasoning=reasoning
        )
