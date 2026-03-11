from py_clob_client.client import ClobClient
from typing import Dict, List
import json

class PolymarketConnector:
    """Connect to Polymarket prediction markets"""
    
    def __init__(self):
        # Polymarket uses Polygon blockchain
        self.host = "https://clob.polymarket.com"
        self.client = ClobClient(self.host, key=None)  # Read-only for now
    
    def get_crypto_markets(self) -> List[Dict]:
        """Get all crypto-related prediction markets"""
        try:
            # Search for BTC/crypto markets
            markets = self.client.get_markets()
            
            crypto_markets = []
            keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto']
            
            for market in markets:
                question = market.get('question', '').lower()
                if any(k in question for k in keywords):
                    crypto_markets.append({
                        'question': market.get('question'),
                        'end_date': market.get('end_date_iso'),
                        'yes_price': market.get('outcome_prices', [0.5, 0.5])[1],
                        'volume': market.get('volume', 0),
                        'market_id': market.get('condition_id')
                    })
            
            return crypto_markets[:10]  # Top 10
        except Exception as e:
            # Fallback to mock data for testing
            return self._get_mock_markets()
    
    def _get_mock_markets(self) -> List[Dict]:
        """Mock data for testing"""
        return [
            {
                'question': 'Will Bitcoin hit $80,000 by March 31, 2026?',
                'end_date': '2026-03-31',
                'yes_price': 0.45,  # 45% chance according to market
                'volume': 125000,
                'market_id': 'btc_80k_mar'
            },
            {
                'question': 'Will Bitcoin exceed $75,000 in March 2026?',
                'end_date': '2026-03-31',
                'yes_price': 0.62,  # 62% chance
                'volume': 89000,
                'market_id': 'btc_75k_mar'
            },
            {
                'question': 'Will the Fed cut rates in March 2026?',
                'end_date': '2026-03-31',
                'yes_price': 0.38,  # 38% chance
                'volume': 250000,
                'market_id': 'fed_cut_mar'
            }
        ]
    
    def analyze_arbitrage(self, current_btc_price: float) -> Dict:
        """Find arbitrage between Polymarket and actual BTC price"""
        markets = self.get_crypto_markets()
        
        opportunities = []
        
        for market in markets:
            question = market['question']
            
            # Parse target price from question
            if '$80,000' in question or '$80k' in question:
                target = 80000
            elif '$75,000' in question or '$75k' in question:
                target = 75000
            else:
                continue
            
            # Calculate required BTC gain
            required_gain = ((target - current_btc_price) / current_btc_price) * 100
            
            # Market probability vs required gain
            market_prob = market['yes_price']
            
            # Simple edge calculation
            # If BTC only needs 5% gain but market says 45% → underpriced!
            edge = market_prob - (required_gain / 20)  # Rough heuristic
            
            if edge > 0.1:  # 10% edge threshold
                opportunities.append({
                    'question': question,
                    'market_price': market_prob,
                    'required_gain': required_gain,
                    'edge': edge,
                    'recommendation': 'BUY' if edge > 0.15 else 'HOLD'
                })
        
        return {
            'opportunities': opportunities,
            'total_markets': len(markets)
        }
