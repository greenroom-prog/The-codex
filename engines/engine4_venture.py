class VentureEngine:
    """Engine 4: Evaluates and ranks business ventures"""
    
    def __init__(self):
        self.opportunities = {
            'crypto_trading': {
                'margin': 0.02,  # 2% per trade
                'capital_needed': 10000,
                'risk': 'HIGH',
                'score': 75,
                'status': 'ACTIVE'  # Atlas is doing this
            },
            'credit_consulting': {
                'margin': 0.70,  # 70% profit
                'capital_needed': 5000,
                'risk': 'LOW',
                'score': 85,
                'status': 'FUTURE'
            },
            'digital_products': {
                'margin': 0.90,  # 90% profit
                'capital_needed': 1000,
                'risk': 'MEDIUM',
                'score': 80,
                'status': 'FUTURE'
            },
            'arbitrage_services': {
                'margin': 0.05,  # 5% spreads
                'capital_needed': 50000,
                'risk': 'MEDIUM',
                'score': 70,
                'status': 'FUTURE'
            }
        }
    
    def evaluate(self, venture_type):
        """Evaluate specific venture opportunity"""
        return self.opportunities.get(venture_type, None)
    
    def rank_opportunities(self):
        """Rank all ventures by score"""
        ranked = sorted(
            self.opportunities.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )
        return ranked
    
    def get_summary(self):
        """Return summary of ventures"""
        active = len([v for v in self.opportunities.values() if v['status'] == 'ACTIVE'])
        total = len(self.opportunities)
        return f"{active} active ventures, {total - active} future opportunities"
