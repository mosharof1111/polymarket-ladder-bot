import time
import requests
from datetime import datetime

class LadderBot:
    def __init__(self):
        self.balance = 1000.0
        self.position = None          # "ETH↑" or "ETH↓"
        self.shares = 0
        self.trades = []
        self.triggered_levels = set()
        self.is_running = False
        self.window_start = None

    def get_current_window_ts(self):
        now = int(time.time())
        return now - (now % 300)

    def get_btc_market_price(self):
        """Get current BTC↑ price from Polymarket"""
        ts = self.get_current_window_ts()
        slug = f"btc-updown-5m-{ts}"
        try:
            # Gamma API to get market info
            r = requests.get(f"https://gamma-api.polymarket.com/events?slug={slug}", timeout=8)
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                # Simplified - in real version we extract token price
                return 0.55  # Placeholder for demo
            return 0.55
        except:
            return 0.55  # fallback

    def get_eth_token_price(self, direction: str):
        """Get current ETH↑ or ETH↓ price"""
        ts = self.get_current_window_ts()
        slug = f"eth-updown-5m-{ts}"
        try:
            # In production we fetch real CLOB price
            return 0.52 + (time.time() % 10) / 100   # demo varying price
        except:
            return 0.50

    def reset_for_new_window(self):
        self.triggered_levels.clear()
        self.window_start = time.time()

bot = LadderBot()
