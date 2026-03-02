import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from app.db import Database
from app.services.news_service import NewsService
from app.translations import t
from app.config import (
    INSTANT_CHECK_INTERVAL,
    DAILY_NOTIFICATION_TIME,
    WEEKLY_NOTIFICATION_DAY,
    WEEKLY_NOTIFICATION_TIME,
    FREQUENCY_INSTANT,
    FREQUENCY_DAILY,
    FREQUENCY_WEEKLY,
)

logger = logging.getLogger(__name__)


class NewsScheduler:
    def __init__(self, bot: Bot, db: Database):
        self.bot = bot
        self.db = db
        self.news_service = NewsService(db)
        self.scheduler = AsyncIOScheduler()

    def start(self):
        """Start the scheduler"""
        # Instant notifications - every X minutes
        self.scheduler.add_job(
            self.send_instant_news,
            trigger=IntervalTrigger(minutes=INSTANT_CHECK_INTERVAL),
            id="instant_news",
            replace_existing=True,
        )

        # Daily notifications - at specific time
        hour, minute = DAILY_NOTIFICATION_TIME.split(":")
        self.scheduler.add_job(
            self.send_daily_news,
            trigger=CronTrigger(hour=int(hour), minute=int(minute)),
            id="daily_news",
            replace_existing=True,
        )

        # Weekly notifications - specific day and time
        hour, minute = WEEKLY_NOTIFICATION_TIME.split(":")
        self.scheduler.add_job(
            self.send_weekly_news,
            trigger=CronTrigger(
                day_of_week=WEEKLY_NOTIFICATION_DAY, hour=int(hour), minute=int(minute)
            ),
            id="weekly_news",
            replace_existing=True,
        )

        self.scheduler.start()
        logger.info("News scheduler started")

    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("News scheduler stopped")

    async def send_instant_news(self):
        """Send news to users with instant frequency"""
        await self._send_news_by_frequency(FREQUENCY_INSTANT)

    async def send_daily_news(self):
        """Send news to users with daily frequency"""
        await self._send_news_by_frequency(FREQUENCY_DAILY)

    async def send_weekly_news(self):
        """Send news to users with weekly frequency"""
        await self._send_news_by_frequency(FREQUENCY_WEEKLY)

    async def _send_news_by_frequency(self, frequency: str):
        """Send news to all users with specified frequency"""
        try:
            # Fetch latest news
            all_news = await self.news_service.fetch_rss_feeds()

            if not all_news:
                logger.info(f"No news fetched for {frequency} update")
                return

            # Get users with this frequency
            users = await self.db.get_users_by_frequency(frequency)

            logger.info(f"Sending {frequency} news to {len(users)} users")

            for user in users:
                try:
                    await self._send_news_to_user(user, all_news)
                except Exception as e:
                    logger.error(f"Error sending news to user {user['telegram_id']}: {e}")

        except Exception as e:
            logger.error(f"Error in {frequency} news job: {e}")

    async def _send_news_to_user(self, user: dict, all_news: list):
        """Send filtered news to a single user"""
        telegram_id = user["telegram_id"]
        lang = user["language"]
        assets = user["assets"]

        # Check if user has active subscription
        if not await self.db.has_active_subscription(telegram_id):
            # Send subscription expired message once
            try:
                await self.bot.send_message(telegram_id, t(lang, "subscription_expired_msg"))
            except Exception:
                pass
            return

        # Filter news for user's assets
        filtered_news = self.news_service.filter_news_for_user(all_news, assets)

        if not filtered_news:
            return

        # Send each news item (check for duplicates)
        news_sent = 0
        for news in filtered_news[:5]:  # Limit to 5 items per batch
            news_hash = news["hash"]

            # Check if already sent
            if await self.db.is_news_sent(telegram_id, news_hash):
                continue

            # Format and send news
            text = t(
                lang,
                "news_title",
                title=news["title"],
                summary=news["summary"] or "No summary available",
                link=news["link"],
            )

            try:
                await self.bot.send_message(telegram_id, text, disable_web_page_preview=False)
                await self.db.mark_news_sent(telegram_id, news_hash)
                news_sent += 1

                # Small delay to avoid rate limits
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"Error sending message to {telegram_id}: {e}")

        logger.info(f"Sent {news_sent} news items to user {telegram_id}")
