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
WEEKLY_NOTIFICATION_DAY = "mon"  # mon, tue, wed, thu, fri, sat, sun
WEEKLY_NOTIFICATION_TIME = "09:00"

# RSS sources by language and market
RSS_SOURCES = {
    "en": {
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
    },
    "ru": {
        "crypto": [
            "https://ru.cointelegraph.com/rss",
            "https://bits.media/news/rss/",
            "https://www.rbc.ru/v10/rss/project/rbcnews/cryptocurrency.rss",
        ],
        "stocks": [
            "https://www.rbc.ru/v10/rss/project/rbcnews/finance.rss",
            "https://www.kommersant.ru/RSS/section-finance.xml",
        ],
        "metals": [
            "https://www.rbc.ru/v10/rss/project/rbcnews/business.rss",
        ],
    },
}

# Asset keywords for filtering (multilingual)
ASSET_KEYWORDS = {
    "BTC": {
        "en": ["bitcoin", "btc"],
        "ru": ["биткоин", "биткойн", "btc", "биткоина", "биткойна"],
    },
    "ETH": {
        "en": ["ethereum", "eth", "ether"],
        "ru": ["эфириум", "eth", "эфир", "эфириума", "ethereum"],
    },
    "AAPL": {
        "en": ["apple", "aapl"],
        "ru": ["apple", "aapl", "эппл"],
    },
    "TSLA": {
        "en": ["tesla", "tsla"],
        "ru": ["tesla", "тесла", "tsla"],
    },
    "GOLD": {
        "en": ["gold", "xau"],
        "ru": ["золото", "золот", "xau", "золота"],
    },
    "SILVER": {
        "en": ["silver", "xag"],
        "ru": ["серебро", "серебр", "xag", "серебра"],
    },
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
