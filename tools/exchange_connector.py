import ccxt

class ExchangeConnector:
    def __init__(self, exchange_name='coinbase'):
        self.exchange_name = exchange_name
        if exchange_name == 'coinbase':
            self.exchange = ccxt.coinbase({'enableRateLimit': True})
        elif exchange_name == 'kraken':
            self.exchange = ccxt.kraken({'enableRateLimit': True})
        else:
            self.exchange = ccxt.coinbase({'enableRateLimit': True})
    
    def get_price(self, symbol='BTC/USDT'):
        """Get current price for a symbol"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except:
            # Fallback to BTC/USD if USDT fails
            ticker = self.exchange.fetch_ticker('BTC/USD')
            return ticker['last']
    
    def get_ticker(self, symbol='BTC/USDT'):
        """Get full ticker data"""
        return self.exchange.fetch_ticker(symbol)
    
    def get_balance(self):
        """Get account balance"""
        return self.exchange.fetch_balance()
