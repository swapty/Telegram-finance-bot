# Financial News Telegram Bot

A Telegram bot that delivers filtered financial news (crypto, stocks, metals) with customizable frequency and subscription management.

## Features

✅ **Multi-language Support**: English and Russian  
✅ **Asset Tracking**: Crypto (BTC, ETH), Stocks (AAPL, TSLA), Metals (Gold, Silver)  
✅ **Flexible Notifications**: Instant (15 min), Daily (9 AM), Weekly (Monday 9 AM)  
✅ **Subscription System**: 1-month free trial, $2/month paid subscription  
✅ **Promo Codes**: Support for 1, 2, or 12-month promo codes  
✅ **Referral Program**: +1 month for each friend invited  
✅ **RSS News Ingestion**: Automated news fetching from multiple sources  
✅ **Smart Filtering**: Keyword-based filtering matched to user assets  
✅ **Duplicate Prevention**: Never send the same news twice  

## Architecture

```
app/
├── main.py                 # Bot entry point
├── config.py              # Configuration and environment variables
├── db.py                  # Database operations
├── translations.py        # Multi-language support
├── scheduler.py           # News delivery scheduler
├── handlers/              # Command and callback handlers
│   ├── start.py          # /start and language selection
│   ├── settings.py       # Asset and frequency settings
│   ├── subscription.py   # Subscription management
│   └── referral.py       # Referral system
└── services/
    └── news_service.py   # RSS fetching and filtering
```

## Database Schema

### users
- `id` - Primary key
- `telegram_id` - Unique Telegram user ID
- `language` - User language (en/ru)
- `subscription_status` - trial/paid/expired
- `subscription_expires_at` - Expiration timestamp
- `referral_code` - Unique referral code
- `referred_by` - ID of user who referred this user
- `created_at` - Registration timestamp

### user_settings
- `user_id` - Foreign key to users.telegram_id
- `assets` - JSON array of selected assets
- `frequency` - instant/daily/weekly

### sent_news
- `user_id` - Foreign key to users.telegram_id
- `news_hash` - MD5 hash of news item
- `sent_at` - Timestamp when sent
- Unique constraint on (user_id, news_hash)

### promo_codes
- `code` - Promo code string
- `duration_months` - Number of months to add
- `active` - Boolean flag

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_ID=your_telegram_id
DATABASE_PATH=bot.db
AI_API_KEY=optional_for_future_ai_features
```

### 3. Run the Bot

```bash
python app/main.py
```

## Usage

### User Flow

1. **Start**: User sends `/start` → selects language (EN/RU)
2. **Trial Activated**: 1-month free trial begins automatically
3. **Settings**: User selects assets and notification frequency
4. **Receive News**: Bot delivers filtered news based on settings

### Admin Operations

Create promo codes directly in the database:

```python
import asyncio
from app.db import Database

async def create_promo():
    db = Database()
    await db.init_db()
    await db.create_promo_code("LAUNCH2024", duration_months=1)

asyncio.run(create_promo())
```

## Testing Checklist

- [ ] `/start` command works
- [ ] Language selection persists
- [ ] Asset selection saves correctly
- [ ] Frequency selection works
- [ ] Trial subscription activates on registration
- [ ] Promo code activation extends subscription
- [ ] Referral link generation works
- [ ] Referrer gets +1 month when friend joins
- [ ] News sends according to schedule
- [ ] Duplicate news is blocked
- [ ] Expired subscriptions stop receiving news

## News Sources

### Crypto
- CoinTelegraph RSS
- CoinDesk RSS

### Stocks
- Yahoo Finance RSS
- CNBC RSS

### Metals
- Kitco Metals RSS

## Deployment

### Free Cloud Options

1. **Heroku** (with scheduler add-on)
2. **Railway.app**
3. **Fly.io**
4. **Render.com**

### Requirements
- Python 3.11+
- SQLite database (file-based, included)
- 256MB RAM minimum
- Scheduled jobs support

## Future Improvements

- [ ] Payment integration (Stripe/Telegram Payments)
- [ ] AI-powered importance scoring
- [ ] More asset types (forex, commodities)
- [ ] Custom keyword alerts
- [ ] News sentiment analysis
- [ ] User analytics dashboard
- [ ] Admin panel via bot commands
- [ ] Export news history
- [ ] Multi-timezone support

## License

MIT License

## Support

For issues or questions, contact the admin via Telegram.
