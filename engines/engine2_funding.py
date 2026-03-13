import json
from datetime import datetime

class FundingEngine:
    """Engine 2: Maps lenders and capital opportunities"""
    
    def __init__(self):
        self.lenders = self._load_lender_db()
    
    def _load_lender_db(self):
        """Load or create lender database"""
        try:
            with open('lenders.json', 'r') as f:
                return json.load(f)
        except:
            # Default lender database
            return {
                'nav': {
                    'limit': 250000,
                    'requirements': 'no-doc, 1yr business',
                    'approval_rate': 85,
                    'notes': 'Best for established businesses'
                },
                'bluevine': {
                    'limit': 100000,
                    'requirements': 'soft-pull, revenue verification',
                    'approval_rate': 90,
                    'notes': 'Fast approval, good for startups'
                },
                'fundbox': {
                    'limit': 150000,
                    'requirements': 'revenue only',
                    'approval_rate': 75,
                    'notes': 'Medium difficulty'
                },
                'brex': {
                    'limit': 500000,
                    'requirements': '1yr business, high revenue',
                    'approval_rate': 70,
                    'notes': 'High limits but strict'
                }
            }
    
    def find_opportunities(self, target_amount=100000):
        """Find best lenders for target amount"""
        opportunities = []
        
        for name, data in self.lenders.items():
            if data['limit'] >= target_amount:
                opportunities.append({
                    'lender': name,
                    'max_amount': data['limit'],
                    'requirements': data['requirements'],
                    'approval_rate': data['approval_rate']
                })
        
        return sorted(opportunities, key=lambda x: x['approval_rate'], reverse=True)
