import aiosqlite
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from app.config import DATABASE_PATH, TRIAL_DURATION_DAYS


class Database:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path

    async def init_db(self):
        """Initialize database schema"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    language TEXT DEFAULT 'en',
                    subscription_status TEXT DEFAULT 'trial',
                    subscription_expires_at TIMESTAMP,
                    referral_code TEXT UNIQUE,
                    referred_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (referred_by) REFERENCES users(telegram_id)
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    assets TEXT DEFAULT '[]',
                    frequency TEXT DEFAULT 'instant',
                    FOREIGN KEY (user_id) REFERENCES users(telegram_id)
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS sent_news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    news_hash TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(telegram_id),
                    UNIQUE(user_id, news_hash)
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS promo_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    duration_months INTEGER NOT NULL,
                    active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id)
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_sent_news_user_hash ON sent_news(user_id, news_hash)
            """)

            await db.commit()

    async def create_user(
        self, telegram_id: int, language: str = "en", referred_by: Optional[int] = None
    ) -> bool:
        """Create new user with trial subscription"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                referral_code = self._generate_referral_code()
                expires_at = datetime.now() + timedelta(days=TRIAL_DURATION_DAYS)

                await db.execute(
                    """
                    INSERT INTO users (telegram_id, language, subscription_status, 
                                     subscription_expires_at, referral_code, referred_by)
                    VALUES (?, ?, 'trial', ?, ?, ?)
                    """,
                    (telegram_id, language, expires_at, referral_code, referred_by),
                )

                await db.execute(
                    """
                    INSERT INTO user_settings (user_id, assets, frequency)
                    VALUES (?, '[]', 'instant')
                    """,
                    (telegram_id,),
                )

                await db.commit()

                # Reward referrer if exists
                if referred_by:
                    await self._reward_referrer(referred_by)

                return True
        except aiosqlite.IntegrityError:
            return False

    async def get_user(self, telegram_id: int) -> Optional[Dict]:
        """Get user by telegram_id"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def update_language(self, telegram_id: int, language: str):
        """Update user language"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET language = ? WHERE telegram_id = ?",
                (language, telegram_id),
            )
            await db.commit()

    async def get_user_settings(self, telegram_id: int) -> Optional[Dict]:
        """Get user settings"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM user_settings WHERE user_id = ?", (telegram_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    result = dict(row)
                    result["assets"] = json.loads(result["assets"])
                    return result
                return None

    async def update_user_settings(
        self, telegram_id: int, assets: Optional[List[str]] = None, frequency: Optional[str] = None
    ):
        """Update user settings"""
        async with aiosqlite.connect(self.db_path) as db:
            if assets is not None:
                await db.execute(
                    "UPDATE user_settings SET assets = ? WHERE user_id = ?",
                    (json.dumps(assets), telegram_id),
                )

            if frequency is not None:
                await db.execute(
                    "UPDATE user_settings SET frequency = ? WHERE user_id = ?",
                    (frequency, telegram_id),
                )

            await db.commit()

    async def is_news_sent(self, telegram_id: int, news_hash: str) -> bool:
        """Check if news was already sent to user"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT 1 FROM sent_news WHERE user_id = ? AND news_hash = ?",
                (telegram_id, news_hash),
            ) as cursor:
                return await cursor.fetchone() is not None

    async def mark_news_sent(self, telegram_id: int, news_hash: str):
        """Mark news as sent to user"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO sent_news (user_id, news_hash) VALUES (?, ?)",
                (telegram_id, news_hash),
            )
            await db.commit()

    async def has_active_subscription(self, telegram_id: int) -> bool:
        """Check if user has active subscription"""
        user = await self.get_user(telegram_id)
        if not user:
            return False

        if user["subscription_expires_at"]:
            expires_at = datetime.fromisoformat(user["subscription_expires_at"])
            return datetime.now() < expires_at

        return False

    async def activate_promo_code(self, telegram_id: int, code: str) -> bool:
        """Activate promo code for user"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM promo_codes WHERE code = ? AND active = 1", (code,)
            ) as cursor:
                promo = await cursor.fetchone()

            if not promo:
                return False

            user = await self.get_user(telegram_id)
            if not user:
                return False

            current_expires = user["subscription_expires_at"]
            if current_expires:
                current_expires = datetime.fromisoformat(current_expires)
                if current_expires < datetime.now():
                    current_expires = datetime.now()
            else:
                current_expires = datetime.now()

            new_expires = current_expires + timedelta(days=30 * promo["duration_months"])

            await db.execute(
                """
                UPDATE users 
                SET subscription_status = 'paid', subscription_expires_at = ?
                WHERE telegram_id = ?
                """,
                (new_expires, telegram_id),
            )

            await db.commit()
            return True

    async def get_users_by_frequency(self, frequency: str) -> List[Dict]:
        """Get all users with specific notification frequency and active subscription"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT u.telegram_id, u.language, s.assets, s.frequency
                FROM users u
                JOIN user_settings s ON u.telegram_id = s.user_id
                WHERE s.frequency = ? AND u.subscription_expires_at > datetime('now')
                """,
                (frequency,),
            ) as cursor:
                rows = await cursor.fetchall()
                results = []
                for row in rows:
                    result = dict(row)
                    result["assets"] = json.loads(result["assets"])
                    results.append(result)
                return results

    async def create_promo_code(self, code: str, duration_months: int) -> bool:
        """Create new promo code"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO promo_codes (code, duration_months) VALUES (?, ?)",
                    (code, duration_months),
                )
                await db.commit()
                return True
        except aiosqlite.IntegrityError:
            return False

    async def get_referral_code(self, telegram_id: int) -> Optional[str]:
        """Get user's referral code"""
        user = await self.get_user(telegram_id)
        return user["referral_code"] if user else None

    async def get_user_by_referral_code(self, referral_code: str) -> Optional[int]:
        """Get telegram_id by referral code"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT telegram_id FROM users WHERE referral_code = ?", (referral_code,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None

    def _generate_referral_code(self) -> str:
        """Generate unique referral code"""
        return secrets.token_urlsafe(8)

    async def _reward_referrer(self, referrer_id: int):
        """Add 1 month to referrer's subscription"""
        user = await self.get_user(referrer_id)
        if not user:
            return

        current_expires = user["subscription_expires_at"]
        if current_expires:
            current_expires = datetime.fromisoformat(current_expires)
            if current_expires < datetime.now():
                current_expires = datetime.now()
        else:
            current_expires = datetime.now()

        new_expires = current_expires + timedelta(days=30)

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET subscription_expires_at = ? WHERE telegram_id = ?",
                (new_expires, referrer_id),
            )
            await db.commit()

    @staticmethod
    def hash_news(title: str, link: str) -> str:
        """Generate hash for news item"""
        content = f"{title}|{link}"
        return hashlib.md5(content.encode()).hexdigest()
