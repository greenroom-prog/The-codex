import ccxt
from typing import Dict, List
from datetime import datetime

class MultiExchange:
    """Manage multiple exchanges for arbitrage"""
    
    def __init__(self):
        self.exchanges = {
            'coinbase': ccxt.coinbase({'enableRateLimit': True}),
            'kraken': ccxt.kraken({'enableRateLimit': True})
        }
    
    def get_all_prices(self, symbol: str) -> Dict:
        """Get price from all exchanges"""
        prices = {}
        
        for name, exchange in self.exchanges.items():
            try:
                ticker = exchange.fetch_ticker(symbol)
                prices[name] = {
                    'price': ticker['last'],
                    'bid': ticker.get('bid'),
                    'ask': ticker.get('ask'),
                    'volume': ticker.get('baseVolume', 0)
                }
            except Exception as e:
                prices[name] = {'error': str(e)}
        
        return prices
    
    def find_arbitrage(self, symbol: str) -> Dict:
        """Find arbitrage opportunities between exchanges"""
        prices = self.get_all_prices(symbol)
        
        valid_prices = {
            name: data['price'] 
            for name, data in prices.items() 
            if 'error' not in data and data['price']
        }
        
        if len(valid_prices) < 2:
            return {'opportunity': False, 'reason': 'Not enough exchanges'}
        
        lowest_exchange = min(valid_prices, key=valid_prices.get)
        highest_exchange = max(valid_prices, key=valid_prices.get)
        
        lowest_price = valid_prices[lowest_exchange]
        highest_price = valid_prices[highest_exchange]
        
        spread_percent = ((highest_price - lowest_price) / lowest_price) * 100
        
        # Account for fees (0.6% Coinbase + 0.16% Kraken = 0.76% total)
        net_profit = spread_percent - 0.76
        
        return {
            'opportunity': net_profit > 0.5,
            'buy_exchange': lowest_exchange,
            'sell_exchange': highest_exchange,
            'buy_price': lowest_price,
            'sell_price': highest_price,
            'spread_percent': spread_percent,
            'net_profit_percent': net_profit,
            'timestamp': datetime.utcnow().isoformat()
        }
