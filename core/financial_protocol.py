from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class FinancialAgentRole(str, Enum):
    """Financial agent specializations"""
    GHOST = "ghost"          # Arbitrage hunter
    QUANT = "quant"          # Momentum trader
    VAULT = "vault"          # Risk-off defender
    FARMER = "farmer"        # Yield generator
    SENTINEL = "sentinel"    # Risk monitor
    SCRIBE = "scribe"        # Tax/compliance

class ExchangeType(str, Enum):
    """Supported exchanges"""
    KUCOIN = "kucoin"
    BINANCE = "binance"
    COINBASE = "coinbase"

class TradeSignal(BaseModel):
    """Trading signal from agent"""
    agent_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    exchange: ExchangeType
    symbol: str  # e.g., "BTC/USDT"
    action: str  # "BUY", "SELL", "HOLD"
    quantity: float
    price: Optional[float] = None
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str

class PositionState(BaseModel):
    """Current position tracking"""
    symbol: str
    exchange: ExchangeType
    entry_price: float
    current_price: float
    quantity: float
    pnl_percent: float
    opened_at: datetime

class RiskMetrics(BaseModel):
    """Portfolio risk metrics"""
    total_capital: float
    deployed_capital: float
    max_drawdown_percent: float
    current_drawdown_percent: float
    position_count: int
    largest_position_percent: float
    kill_switch_triggered: bool = False
