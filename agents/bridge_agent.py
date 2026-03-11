from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
from tools.cross_chain import CrossChainMonitor

class BridgeAgent(FinancialAgent):
    """Cross-chain arb (AGGRESSIVE: 5bps threshold)"""
    
    def __init__(self, config):
        super().__init__(FinancialAgentRole.GHOST, config)
        self.cross = CrossChainMonitor()
    
    async def find_cross_chain_arb(self, market_data):
        try:
            result = self.cross.find_cross_chain_arbitrage()
            
            # LOWERED: 5bps from 10bps
            if result.get("has_arbitrage") and result.get("spread_bps", 0) > 5:
                return TradeSignal(
                    agent_id="bridge", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                    action="BUY", quantity=0.022, confidence=0.84,
                    reasoning=f"CROSS-CHAIN: {result.get('spread_bps', 0):.1f}bps"
                )
        except: pass
        
        return TradeSignal(
            agent_id="bridge", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
            action="HOLD", quantity=0, confidence=0.5, reasoning="No arb"
        )
