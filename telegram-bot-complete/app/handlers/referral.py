from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.db import Database
from app.translations import t

router = Router()


@router.callback_query(F.data == "menu_invite")
async def show_invite(callback: CallbackQuery, db: Database):
    """Show referral information"""
    user = await db.get_user(callback.from_user.id)

    if not user:
        await callback.answer("Error", show_alert=True)
        return

    lang = user["language"]
    referral_code = await db.get_referral_code(callback.from_user.id)

    if not referral_code:
        await callback.answer("Error generating referral code", show_alert=True)
        return

    # Generate referral link
    bot_username = (await callback.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={referral_code}"

    # Count referred users (simplified - could be tracked in DB)
    import aiosqlite

    async with aiosqlite.connect(db.db_path) as conn:
        async with conn.execute(
            "SELECT COUNT(*) FROM users WHERE referred_by = ?", (callback.from_user.id,)
        ) as cursor:
            row = await cursor.fetchone()
            count = row[0] if row else 0

    text = t(lang, "referral_info", link=referral_link, count=count)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "back"), callback_data="invite_back")],
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "invite_back")
async def invite_back(callback: CallbackQuery, db: Database):
    """Go back to main menu from invite"""
    user = await db.get_user(callback.from_user.id)
    lang = user["language"]

    from app.handlers.start import show_main_menu

    await callback.message.delete()
    await show_main_menu(callback.message, lang, db)
    await callback.answer()
