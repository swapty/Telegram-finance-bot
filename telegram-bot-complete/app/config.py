import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot.db")
AI_API_KEY = os.getenv("AI_API_KEY", "")

# Subscription configuration
TRIAL_DURATION_DAYS = 30
SUBSCRIPTION_PRICE_USD = 2

# Notification frequencies
FREQUENCY_INSTANT = "instant"
FREQUENCY_DAILY = "daily"
FREQUENCY_WEEKLY = "weekly"

# Scheduler intervals (minutes)
INSTANT_CHECK_INTERVAL = 15
DAILY_NOTIFICATION_TIME = "09:00"
WEEKLY_NOTIFICATION_DAY = "mon"
WEEKLY_NOTIFICATION_TIME = "09:00"

# RSS sources by market
RSS_SOURCES = {
    "crypto": [
        "https://cointelegraph.com/rss",
        "https://coindesk.com/arc/outboundfeeds/rss/",
    ],
    "stocks": [
        "https://feeds.finance.yahoo.com/rss/2.0/headline",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    ],
    "metals": [
        "https://www.kitco.com/rss/metals.xml",
    ],
}

# Asset keywords for filtering
ASSET_KEYWORDS = {
    "BTC": ["bitcoin", "btc"],
    "ETH": ["ethereum", "eth", "ether"],
    "AAPL": ["apple", "aapl"],
    "TSLA": ["tesla", "tsla"],
    "GOLD": ["gold", "xau"],
    "SILVER": ["silver", "xag"],
}

# Available assets by market
AVAILABLE_ASSETS = {
    "crypto": ["BTC", "ETH"],
    "stocks": ["AAPL", "TSLA"],
    "metals": ["GOLD", "SILVER"],
}

# Validate required environment variables
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")
