import streamlit as st
import time
from bot import bot

st.set_page_config(page_title="Polymarket Ladder Bot", layout="wide", page_icon="🚀")
st.title("🚀 Polymarket 5m ETH Ladder Bot")

st.sidebar.header("Controls")
if st.sidebar.button("▶️ Start Bot" if not bot.is_running else "⏹️ Stop Bot", type="primary", use_container_width=True):
    if not bot.is_running:
        bot.is_running = True
        bot.reset_for_new_window()
        st.success("✅ Bot Started")
    else:
        bot.is_running = False
        st.warning("⛔ Bot Stopped")

col1, col2, col3 = st.columns(3)
col1.metric("Balance", f"${bot.balance:,.2f}")
col2.metric("Position", bot.position or "No Position")
col3.metric("Shares", bot.shares)

if bot.window_start:
    elapsed = int(time.time() - bot.window_start)
    st.progress(elapsed / 300)
    st.caption(f"Elapsed: {elapsed}s | Cutoff at 270s (4:30)")

st.subheader("Market Signals")
btc_up_price = bot.get_btc_market_price()
signal = "🟢 BULLISH" if btc_up_price >= 0.70 else "🔴 BEARISH"
st.metric("BTC Market Signal", signal, f"BTC↑ Price: {btc_up_price:.3f}")

# Ladder
st.subheader("ETH Ladder Status")
cols = st.columns(4)
thresholds = [0.70, 0.80, 0.90, 0.97]
for i in range(4):
    status = "✅ Triggered" if (i+1) in bot.triggered_levels else "⏳ Waiting"
    cols[i].metric(f"L{i+1} (>= {thresholds[i]})", status)

# Live Log
st.subheader("Live Log")
log_placeholder = st.empty()

if bot.is_running:
    while True:
        btc_up = bot.get_btc_market_price()
        eth_price = bot.get_eth_token_price("↑" if btc_up >= 0.70 else "↓")
        
        # Simple demo ladder trigger
        elapsed = int(time.time() - bot.window_start) if bot.window_start else 301
        if elapsed < 270:
            for lvl in range(1, 5):
                if lvl not in bot.triggered_levels and btc_up >= [0.70,0.80,0.90,0.97][lvl-1]:
                    cost = eth_price * 50
                    if bot.balance >= cost:
                        bot.balance -= cost
                        bot.shares += 50
                        bot.position = f"ETH{'↑' if btc_up >= 0.70 else '↓'}"
                        bot.trades.append(f"L{lvl} BUY 50 @ {eth_price:.3f} | BTC↑={btc_up:.3f}")
                        bot.triggered_levels.add(lvl)
                    break

        log_text = "\n".join(bot.trades[-10:]) or "Waiting for signals..."
        log_placeholder.text_area("Activity", log_text, height=300)

        time.sleep(3)
        st.rerun()
else:
    st.info("Start the bot from the sidebar to begin demo")
