import asyncio
from datetime import datetime
from typing import List, Dict
from core.financial_protocol import FinancialAgentRole, PositionState, RiskMetrics

class Sentinel:
    """The kill switch - monitors all agents and enforces risk limits"""
    
    def __init__(self, config: dict):
        self.max_drawdown_percent = config.get('max_drawdown_percent', 5.0)
        self.max_position_size_percent = config.get('max_position_size_percent', 10.0)
        self.kill_switch_enabled = config.get('kill_switch_enabled', True)
        self.is_frozen = False
        self.initial_capital = config.get('initial_capital', 10000.0)
        
    def evaluate_risk(self, positions: List[PositionState], current_capital: float) -> RiskMetrics:
        """Calculate current risk metrics"""
        
        total_value = sum(p.quantity * p.current_price for p in positions)
        deployed_capital = total_value
        
        # Calculate drawdown
        current_drawdown = ((self.initial_capital - current_capital) / self.initial_capital) * 100
        
        # Find largest position
        largest_position = 0
        if positions and current_capital > 0:
            largest_position = max(
                (p.quantity * p.current_price / current_capital) * 100 
                for p in positions
            )
        
        metrics = RiskMetrics(
            total_capital=current_capital,
            deployed_capital=deployed_capital,
            max_drawdown_percent=self.max_drawdown_percent,
            current_drawdown_percent=current_drawdown,
            position_count=len(positions),
            largest_position_percent=largest_position,
            kill_switch_triggered=self.is_frozen
        )
        
        return metrics
    
    def check_kill_switch(self, metrics: RiskMetrics) -> tuple[bool, str]:
        """Check if kill switch should trigger"""
        
        if not self.kill_switch_enabled:
            return False, "Kill switch disabled"
        
        if self.is_frozen:
            return True, "System already frozen"
        
        # Check drawdown limit
        if metrics.current_drawdown_percent >= self.max_drawdown_percent:
            self.is_frozen = True
            return True, f"🚨 KILL SWITCH TRIGGERED: Drawdown {metrics.current_drawdown_percent:.2f}% exceeds limit {self.max_drawdown_percent}%"
        
        # Check position size
        if metrics.largest_position_percent > self.max_position_size_percent:
            self.is_frozen = True
            return True, f"🚨 KILL SWITCH TRIGGERED: Position size {metrics.largest_position_percent:.2f}% exceeds limit {self.max_position_size_percent}%"
        
        return False, "All systems operational"
    
    def manual_override(self, action: str) -> str:
        """Allow manual control"""
        if action == "FREEZE":
            self.is_frozen = True
            return "✅ System manually frozen"
        elif action == "UNFREEZE":
            self.is_frozen = False
            return "✅ System unfrozen - trading resumed"
        else:
            return "❌ Invalid action. Use FREEZE or UNFREEZE"
    
    def get_status(self) -> dict:
        """Get current sentinel status"""
        return {
            "kill_switch_enabled": self.kill_switch_enabled,
            "is_frozen": self.is_frozen,
            "max_drawdown_percent": self.max_drawdown_percent,
            "max_position_size_percent": self.max_position_size_percent,
            "initial_capital": self.initial_capital
        }
