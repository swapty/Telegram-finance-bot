import feedparser
import asyncio
from typing import List, Dict
from datetime import datetime
import logging
from app.config import RSS_SOURCES, ASSET_KEYWORDS
from app.db import Database

logger = logging.getLogger(__name__)


class NewsService:
    def __init__(self, db: Database):
        self.db = db

    async def fetch_rss_feeds(self) -> List[Dict]:
        """Fetch and parse all RSS feeds"""
        all_news = []

        for market, sources in RSS_SOURCES.items():
            for source_url in sources:
                try:
                    news_items = await self._fetch_feed(source_url, market)
                    all_news.extend(news_items)
                except Exception as e:
                    logger.error(f"Error fetching {source_url}: {e}")

        return all_news

    async def _fetch_feed(self, url: str, market: str) -> List[Dict]:
        """Fetch and parse single RSS feed"""
        loop = asyncio.get_event_loop()
        feed = await loop.run_in_executor(None, feedparser.parse, url)

        news_items = []
        for entry in feed.entries[:10]:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")

            if not title or not link:
                continue

            # Remove HTML tags from summary
            summary = self._clean_html(summary)

            news_item = {
                "title": title,
                "link": link,
                "summary": summary[:200] if summary else "",
                "market": market,
                "published": entry.get("published", ""),
                "hash": Database.hash_news(title, link),
            }

            news_items.append(news_item)

        return news_items

    def filter_news_for_user(self, news_items: List[Dict], user_assets: List[str]) -> List[Dict]:
        """Filter news items based on user's selected assets"""
        if not user_assets:
            return []

        filtered = []
        for news in news_items:
            if self._matches_assets(news, user_assets):
                filtered.append(news)

        return filtered

    def _matches_assets(self, news: Dict, user_assets: List[str]) -> bool:
        """Check if news item matches any of user's assets"""
        content = f"{news['title']} {news['summary']}".lower()

        for asset in user_assets:
            if asset in ASSET_KEYWORDS:
                keywords = ASSET_KEYWORDS[asset]
                if any(keyword.lower() in content for keyword in keywords):
                    return True

        return False

    @staticmethod
    def _clean_html(text: str) -> str:
        """Remove HTML tags from text"""
        import re
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text).strip()
