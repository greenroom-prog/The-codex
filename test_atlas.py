import asyncio
from dotenv import load_dotenv
from agents.orchestrator import Orchestrator
from tools.exchange_connector import ExchangeConnector

load_dotenv()

async def main():
    print("ATLAS PROTOCOL TEST")
    exchange = ExchangeConnector("coinbase")
    ticker = exchange.get_ticker("BTC/USDT")
    
    market_data = {
        'symbol': ticker['symbol'],
        'price': ticker['price'],
        'volume': ticker.get('volume') or 0
    }
    
    print(f"BTC: ${market_data['price']:,.2f}")
    
    orch = Orchestrator({'capital': 10000.0})
    await orch.run_cycle(market_data)

asyncio.run(main())
