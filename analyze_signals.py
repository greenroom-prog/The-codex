import sqlite3

conn = sqlite3.connect('atlas_trades.db')
cursor = conn.cursor()

# Analyze which agents are most accurate
cursor.execute('''
    SELECT agent_id, action, COUNT(*) as count
    FROM signals
    GROUP BY agent_id, action
    ORDER BY agent_id, count DESC
''')

print("\n📊 AGENT VOTING PATTERNS:\n" + "="*50)
for agent, action, count in cursor.fetchall():
    print(f"{agent:12} → {action:4} ({count:3} times)")

# Find Prophet's buy signals
cursor.execute('''
    SELECT reasoning, COUNT(*) 
    FROM signals 
    WHERE agent_id='prophet' AND action='BUY'
    GROUP BY reasoning
''')

print("\n🔮 PROPHET'S BUY SIGNALS:\n" + "="*50)
for reason, count in cursor.fetchall():
    print(f"  {reason[:60]}... ({count}x)")

conn.close()
