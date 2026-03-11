import ccxt
from typing import Dict

class OrderBookAnalyzer:
    """Analyze order book depth for price prediction"""
    
    def __init__(self):
        self.exchanges = {
            'coinbase': ccxt.coinbase({'enableRateLimit': True}),
            'kraken': ccxt.kraken({'enableRateLimit': True})
        }
    
    def get_order_book_depth(self, symbol: str = 'BTC/USDT', exchange: str = 'coinbase') -> Dict:
        """Get order book and calculate buy/sell pressure"""
        try:
            exchange_obj = self.exchanges.get(exchange)
            if not exchange_obj:
                return self._mock_order_book()
            
            book = exchange_obj.fetch_order_book(symbol, limit=20)
            
            # Calculate depth
            bid_volume = sum(bid[1] for bid in book['bids'][:10])  # Top 10 bids
            ask_volume = sum(ask[1] for ask in book['asks'][:10])  # Top 10 asks
            
            bid_value = sum(bid[0] * bid[1] for bid in book['bids'][:10])
            ask_value = sum(ask[0] * ask[1] for ask in book['asks'][:10])
            
            # Buy/sell pressure ratio
            pressure_ratio = bid_value / ask_value if ask_value > 0 else 1.0
            
            return {
                'bid_volume': bid_volume,
                'ask_volume': ask_volume,
                'bid_value_usd': bid_value,
                'ask_value_usd': ask_value,
                'pressure_ratio': pressure_ratio,
                'signal': 'BUY_PRESSURE' if pressure_ratio > 1.2 else 'SELL_PRESSURE' if pressure_ratio < 0.8 else 'BALANCED',
                'top_bid': book['bids'][0][0] if book['bids'] else 0,
                'top_ask': book['asks'][0][0] if book['asks'] else 0,
                'spread': (book['asks'][0][0] - book['bids'][0][0]) if book['asks'] and book['bids'] else 0
            }
        except:
            return self._mock_order_book()
    
    def _mock_order_book(self) -> Dict:
        """Mock order book data"""
        return {
            'bid_volume': 45.2,
            'ask_volume': 38.7,
            'bid_value_usd': 3164000,
            'ask_value_usd': 2709000,
            'pressure_ratio': 1.17,
            'signal': 'BUY_PRESSURE',
            'top_bid': 70250,
            'top_ask': 70255,
            'spread': 5
        }
