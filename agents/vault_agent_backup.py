from agents.financial_agent import FinancialAgent
from core.financial_protocol import FinancialAgentRole, TradeSignal, ExchangeType
from core.protocol import AgentConfig
import sqlite3

class VaultAgent(FinancialAgent):
    """Risk + AUTO PROFIT-TAKING"""
    
    def __init__(self, config):
        super().__init__(FinancialAgentRole.GHOST, config)
    
    async def evaluate_risk(self, market_data):
        btc_price = market_data["price"]
        
        # CHECK IF WE HAVE A POSITION
        try:
            conn = sqlite3.connect("atlas_trades.db")
            cursor = conn.cursor()
            cursor.execute("SELECT btc_position FROM paper_trades ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            position = result[0] if result else 0
            
            # If holding BTC, check for profit
            if position > 0:
                cursor.execute("SELECT AVG(btc_price) FROM paper_trades WHERE action='BUY' AND btc_position > 0")
                avg_entry = cursor.fetchone()[0]
                profit_pct = ((btc_price - avg_entry) / avg_entry) * 100
                
                # AUTO-SELL at 0.5% profit (LOWERED from 0.8%)
                if profit_pct > 0.5:
                    conn.close()
                    return TradeSignal(
                        agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                        action="SELL", quantity=position, confidence=0.95,
                        reasoning=f"PROFIT-TAKE: {profit_pct:.2f}% gain"
                    )
                
                # STOP-LOSS at -1.5%
                if profit_pct < -1.5:
                    conn.close()
                    return TradeSignal(
                        agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                        action="SELL", quantity=position, confidence=0.90,
                        reasoning=f"STOP-LOSS: {profit_pct:.2f}% loss"
                    )
            
            conn.close()
        except:
            pass
        
        # Default risk management
        if btc_price > 71000:
            return TradeSignal(
                agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="SELL", quantity=0.015, confidence=0.78,
                reasoning="PROFIT TAKE: BTC >$71K"
            )
        elif btc_price < 68000:
            return TradeSignal(
                agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
                action="BUY", quantity=0.025, confidence=0.82,
                reasoning="BUY DIP: BTC <$68K"
            )
        
        return TradeSignal(
            agent_id="vault", exchange=ExchangeType.COINBASE, symbol="BTC/USD",
            action="HOLD", quantity=0, confidence=0.58, reasoning="Neutral"
        )
