from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from app.db import Database
from app.translations import t

router = Router()


class PromoStates(StatesGroup):
    waiting_for_code = State()


@router.callback_query(F.data == "menu_subscription")
async def show_subscription(callback: CallbackQuery, db: Database):
    """Show subscription information"""
    user = await db.get_user(callback.from_user.id)

    if not user:
        await callback.answer("Error", show_alert=True)
        return

    lang = user["language"]

    # Determine subscription status
    if user["subscription_expires_at"]:
        expires_at = datetime.fromisoformat(user["subscription_expires_at"])
        is_active = datetime.now() < expires_at

        if user["subscription_status"] == "trial":
            status = t(lang, "subscription_trial")
        elif is_active:
            status = t(lang, "subscription_active")
        else:
            status = t(lang, "subscription_expired")

        expires = expires_at.strftime("%Y-%m-%d %H:%M")
    else:
        status = t(lang, "subscription_expired")
        expires = "N/A"

    text = t(lang, "subscription_info", status=status, expires=expires)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎟️ Activate Promo Code", callback_data="sub_promo")],
            [InlineKeyboardButton(text=t(lang, "back"), callback_data="sub_back")],
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "sub_promo")
async def request_promo_code(callback: CallbackQuery, state: FSMContext, db: Database):
    """Request promo code from user"""
    user = await db.get_user(callback.from_user.id)
    lang = user["language"]

    await callback.message.edit_text(t(lang, "enter_promo_code"))
    await state.set_state(PromoStates.waiting_for_code)
    await callback.answer()


@router.message(PromoStates.waiting_for_code)
async def process_promo_code(message: Message, state: FSMContext, db: Database):
    """Process promo code activation"""
    user = await db.get_user(message.from_user.id)
    lang = user["language"]

    code = message.text.strip().upper()

    success = await db.activate_promo_code(message.from_user.id, code)

    if success:
        # Get promo details to show months added
        async with db.db_path as path:
            import aiosqlite

            async with aiosqlite.connect(path) as conn:
                async with conn.execute(
                    "SELECT duration_months FROM promo_codes WHERE code = ?", (code,)
                ) as cursor:
                    row = await cursor.fetchone()
                    months = row[0] if row else 1

        await message.answer(t(lang, "promo_activated", months=months))
    else:
        await message.answer(t(lang, "promo_invalid"))

    await state.clear()

    # Show subscription info again
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "back"), callback_data="sub_back")],
        ]
    )
    await message.answer("Subscription updated", reply_markup=keyboard)


@router.callback_query(F.data == "sub_back")
async def subscription_back(callback: CallbackQuery, db: Database):
    """Go back to main menu from subscription"""
    user = await db.get_user(callback.from_user.id)
    lang = user["language"]

    from app.handlers.start import show_main_menu

    await callback.message.delete()
    await show_main_menu(callback.message, lang, db)
    await callback.answer()
