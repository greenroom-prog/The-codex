from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def dashboard():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>ATLAS Protocol</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #fff;
            padding: 20px;
        }
        .header { text-align: center; padding: 30px 0; }
        .header h1 { font-size: 48px; margin-bottom: 10px; }
        .status { 
            background: #00ff88;
            color: #0a0e27;
            padding: 8px 20px;
            border-radius: 20px;
            display: inline-block;
            font-weight: bold;
        }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 20px;
        }
        .card h3 { font-size: 14px; color: #888; margin-bottom: 10px; }
        .card .value { font-size: 32px; font-weight: bold; color: #00ff88; }
        .refresh { 
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #00ff88;
            color: #0a0e27;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 ATLAS PROTOCOL</h1>
        <div class="status">● LIVE</div>
    </div>
    <div class="stats" id="stats"></div>
    <div id="agents"></div>
    <button class="refresh" onclick="load()">🔄 Refresh</button>
    <script>
        async function load() {
            const res = await fetch('/api/data');
            const d = await res.json();
            document.getElementById('stats').innerHTML = `
                <div class="card"><h3>Cycles</h3><div class="value">${d.cycles}</div></div>
                <div class="card"><h3>BTC Price</h3><div class="value">$${d.btc.toLocaleString()}</div></div>
                <div class="card"><h3>Capital</h3><div class="value">$${d.capital}</div></div>
                <div class="card"><h3>Return</h3><div class="value">${d.return}%</div></div>
            `;
        }
        load();
        setInterval(load, 10000);
    </script>
</body>
</html>'''

@app.route('/api/data')
def api():
    db = sqlite3.connect('atlas_trades.db')
    c = db.cursor()
    c.execute('SELECT COUNT(*) FROM cycles')
    cycles = c.fetchone()[0]
    c.execute('SELECT btc_price FROM cycles ORDER BY id DESC LIMIT 1')
    btc = c.fetchone()
    db.close()
    return jsonify({'cycles': cycles, 'btc': btc[0] if btc else 70000, 'capital': 10031, 'return': 0.31})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
