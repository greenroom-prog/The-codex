import asyncio
import os

os.environ["ANTHROPIC_API_KEY"] = "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"

from agents.orchestrator import Orchestrator
from tools.exchange_connector import ExchangeConnector
from tools.trade_logger import TradeLogger

async def main():
    config = {"model": "claude-sonnet-4-20250514"}
    orchestrator = Orchestrator(config)
    exchange = ExchangeConnector("coinbase")
    logger = TradeLogger()
    
    print("ATLAS CONQUISTADOR LAUNCHED")
    cycle = 0
    
    while True:
        try:
            cycle += 1
            print(f"\nCYCLE {cycle}")
            
            btc_price = exchange.get_price("BTC/USD")
            market_data = {"symbol": "BTC/USD", "price": btc_price}
            
            signals = await orchestrator.run_cycle(market_data)
            
            # Determine consensus
            buy_votes = sum(1 for s in signals if s.action == "BUY")
            sell_votes = sum(1 for s in signals if s.action == "SELL")
            
            if buy_votes >= 2:
                consensus = "BUY"
            elif sell_votes >= 2:
                consensus = "SELL"
            else:
                consensus = "HOLD"
            
            # Log everything
            logger.log_cycle(btc_price, 10000, consensus)
            logger.log_signals(signals, btc_price, consensus)
            
            print(f"Waiting 900 seconds...")
            await asyncio.sleep(900)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(900)

if __name__ == "__main__":
    asyncio.run(main())
