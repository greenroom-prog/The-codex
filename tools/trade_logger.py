import sqlite3
from datetime import datetime
from typing import List
from core.financial_protocol import TradeSignal

class TradeLogger:
    def __init__(self, db_path: str = "atlas_trades.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                agent_id TEXT,
                symbol TEXT,
                action TEXT,
                price REAL,
                confidence REAL,
                reasoning TEXT,
                consensus TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cycles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                btc_price REAL,
                capital REAL,
                consensus TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_signals(self, signals: List[TradeSignal], btc_price: float, consensus: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.utcnow().isoformat()
        
        for signal in signals:
            cursor.execute(
                'INSERT INTO signals VALUES (NULL,?,?,?,?,?,?,?,?)',
                (timestamp, signal.agent_id, signal.symbol, signal.action, 
                 btc_price, signal.confidence, signal.reasoning, consensus)
            )
        
        conn.commit()
        conn.close()
    
    def log_cycle(self, btc_price: float, capital: float, consensus: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO cycles VALUES (NULL,?,?,?,?)',
            (datetime.utcnow().isoformat(), btc_price, capital, consensus)
        )
        conn.commit()
        conn.close()
    
    def get_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM cycles')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM signals WHERE action="BUY"')
        buys = cursor.fetchone()[0]
        
        conn.close()
        return {'total_cycles': total, 'buy_signals': buys}
