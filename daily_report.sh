#!/bin/bash
echo "═══════════════════════════════════════════════════════════"
echo "📊 ATLAS DAILY REPORT - $(date '+%Y-%m-%d %H:%M')"
echo "═══════════════════════════════════════════════════════════"

echo -e "\n💰 TRADING STATS:"
sqlite3 atlas_trades.db "SELECT COUNT(*) FROM paper_trades;" | xargs echo "   Total trades:"
sqlite3 atlas_trades.db "SELECT COUNT(*) FROM paper_trades WHERE action='BUY';" | xargs echo "   Buys:"
sqlite3 atlas_trades.db "SELECT COUNT(*) FROM paper_trades WHERE action='SELL';" | xargs echo "   Sells:"

echo -e "\n📈 CURRENT POSITION:"
sqlite3 atlas_trades.db "SELECT btc_position, capital_after FROM paper_trades ORDER BY id DESC LIMIT 1;" | awk -F'|' '{printf "   BTC: %.4f\n   Cash: $%.2f\n", $1, $2}'

echo -e "\n💵 PERFORMANCE:"
sqlite3 atlas_trades.db "SELECT SUM(pnl) FROM paper_trades WHERE pnl IS NOT NULL;" | xargs printf "   Total P&L: $%.2f\n"

echo -e "\n📝 RECENT TRADES:"
sqlite3 atlas_trades.db "SELECT substr(timestamp,12,8), action, btc_price FROM paper_trades ORDER BY id DESC LIMIT 5;" | awk -F'|' '{printf "   %s | %s @ $%.2f\n", $1, $2, $3}'

echo "═══════════════════════════════════════════════════════════"
