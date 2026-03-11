from agents.sentinel import Sentinel
from core.financial_protocol import PositionState, ExchangeType
from datetime import datetime

# Test the Sentinel
print("🛡️  TESTING THE SENTINEL (Kill Switch)\n")

# Create sentinel with 5% max drawdown
config = {
    'max_drawdown_percent': 5.0,
    'max_position_size_percent': 10.0,
    'kill_switch_enabled': True,
    'initial_capital': 10000.0
}

sentinel = Sentinel(config)
print(f"Sentinel Status: {sentinel.get_status()}\n")

# Scenario 1: Normal trading (should be fine)
print("📊 Scenario 1: Normal Trading")
positions = [
    PositionState(
        symbol="BTC/USDT",
        exchange=ExchangeType.KUCOIN,
        entry_price=50000,
        current_price=51000,
        quantity=0.1,
        pnl_percent=2.0,
        opened_at=datetime.utcnow()
    )
]
current_capital = 10200  # Made 2% profit

metrics = sentinel.evaluate_risk(positions, current_capital)
triggered, message = sentinel.check_kill_switch(metrics)

print(f"Capital: ${current_capital}")
print(f"Drawdown: {metrics.current_drawdown_percent:.2f}%")
print(f"Status: {message}\n")

# Scenario 2: Dangerous drawdown (should trigger kill switch)
print("⚠️  Scenario 2: Dangerous Drawdown")
current_capital = 9400  # Lost 6% (exceeds 5% limit)

metrics = sentinel.evaluate_risk(positions, current_capital)
triggered, message = sentinel.check_kill_switch(metrics)

print(f"Capital: ${current_capital}")
print(f"Drawdown: {metrics.current_drawdown_percent:.2f}%")
print(f"Kill Switch Triggered: {triggered}")
print(f"Status: {message}\n")

# Scenario 3: Try to trade while frozen (should reject)
print("🔒 Scenario 3: Attempt Trading While Frozen")
print(f"System Frozen: {sentinel.is_frozen}")
print("Attempting to place trade...")
if sentinel.is_frozen:
    print("❌ TRADE REJECTED - System is frozen!\n")

# Scenario 4: Manual override
print("🔓 Scenario 4: Manual Override")
result = sentinel.manual_override("UNFREEZE")
print(f"{result}")
print(f"System Frozen: {sentinel.is_frozen}\n")

print("✅ Sentinel test complete!")
