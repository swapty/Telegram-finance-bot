#!/usr/bin/env python3
"""
Admin utility script for managing the bot
"""
import asyncio
import sys
from app.db import Database


async def create_promo_code(code: str, months: int):
    """Create a new promo code"""
    db = Database()
    await db.init_db()

    success = await db.create_promo_code(code.upper(), months)

    if success:
        print(f"✅ Promo code created: {code.upper()} ({months} month{'s' if months > 1 else ''})")
    else:
        print(f"❌ Failed to create promo code (may already exist)")


async def list_promo_codes():
    """List all promo codes"""
    import aiosqlite

    db = Database()
    await db.init_db()

    async with aiosqlite.connect(db.db_path) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute(
            "SELECT code, duration_months, active, created_at FROM promo_codes ORDER BY created_at DESC"
        ) as cursor:
            rows = await cursor.fetchall()

            if not rows:
                print("No promo codes found")
                return

            print("\n📋 Promo Codes:")
            print("-" * 60)
            for row in rows:
                status = "✅ Active" if row["active"] else "❌ Inactive"
                print(
                    f"{row['code']:<20} {row['duration_months']} month(s)    {status}    {row['created_at']}"
                )
            print("-" * 60)


async def deactivate_promo_code(code: str):
    """Deactivate a promo code"""
    import aiosqlite

    db = Database()
    await db.init_db()

    async with aiosqlite.connect(db.db_path) as conn:
        await conn.execute("UPDATE promo_codes SET active = 0 WHERE code = ?", (code.upper(),))
        await conn.commit()

    print(f"✅ Promo code {code.upper()} deactivated")


async def show_stats():
    """Show bot statistics"""
    import aiosqlite

    db = Database()
    await db.init_db()

    async with aiosqlite.connect(db.db_path) as conn:
        # Total users
        async with conn.execute("SELECT COUNT(*) FROM users") as cursor:
            total_users = (await cursor.fetchone())[0]

        # Active subscriptions
        async with conn.execute(
            "SELECT COUNT(*) FROM users WHERE subscription_expires_at > datetime('now')"
        ) as cursor:
            active_subs = (await cursor.fetchone())[0]

        # Trial users
        async with conn.execute(
            "SELECT COUNT(*) FROM users WHERE subscription_status = 'trial' AND subscription_expires_at > datetime('now')"
        ) as cursor:
            trial_users = (await cursor.fetchone())[0]

        # Total news sent
        async with conn.execute("SELECT COUNT(*) FROM sent_news") as cursor:
            news_sent = (await cursor.fetchone())[0]

        print("\n📊 Bot Statistics:")
        print("-" * 40)
        print(f"Total Users:         {total_users}")
        print(f"Active Subscriptions: {active_subs}")
        print(f"Trial Users:         {trial_users}")
        print(f"Total News Sent:     {news_sent}")
        print("-" * 40)


def print_usage():
    """Print usage information"""
    print("""
Admin Utility Script

Usage:
    python admin.py create-promo <CODE> <MONTHS>    Create a promo code
    python admin.py list-promos                     List all promo codes
    python admin.py deactivate-promo <CODE>         Deactivate a promo code
    python admin.py stats                           Show bot statistics

Examples:
    python admin.py create-promo LAUNCH2024 1
    python admin.py create-promo YEAR2024 12
    python admin.py list-promos
    python admin.py deactivate-promo LAUNCH2024
    python admin.py stats
    """)


async def main():
    """Main function"""
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "create-promo":
        if len(sys.argv) != 4:
            print("Usage: python admin.py create-promo <CODE> <MONTHS>")
            return
        code = sys.argv[2]
        months = int(sys.argv[3])
        await create_promo_code(code, months)

    elif command == "list-promos":
        await list_promo_codes()

    elif command == "deactivate-promo":
        if len(sys.argv) != 3:
            print("Usage: python admin.py deactivate-promo <CODE>")
            return
        code = sys.argv[2]
        await deactivate_promo_code(code)

    elif command == "stats":
        await show_stats()

    else:
        print(f"Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    asyncio.run(main())
