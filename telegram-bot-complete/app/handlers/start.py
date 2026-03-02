from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.db import Database
from app.translations import t

router = Router()


class RegistrationStates(StatesGroup):
    waiting_for_language = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, db: Database):
    """Handle /start command"""
    user = await db.get_user(message.from_user.id)

    # Check for referral code
    args = message.text.split()
    referral_code = None
    if len(args) > 1:
        referral_code = args[1]

    if user:
        # User already exists, show main menu
        await show_main_menu(message, user["language"], db)
    else:
        # New user, show language selection
        referred_by = None
        if referral_code:
            referred_by = await db.get_user_by_referral_code(referral_code)

        await state.update_data(referred_by=referred_by)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
                [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            ]
        )
        await message.answer("🌍 Select language / Выберите язык:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("lang_"))
async def process_language_selection(callback: CallbackQuery, state: FSMContext, db: Database):
    """Process language selection"""
    language = callback.data.split("_")[1]

    # Get referral data from state
    data = await state.get_data()
    referred_by = data.get("referred_by")

    # Create user
    success = await db.create_user(
        telegram_id=callback.from_user.id, language=language, referred_by=referred_by
    )

    if success:
        await callback.message.edit_text(t(language, "language_selected"))
        await state.clear()

        # Show main menu
        await show_main_menu(callback.message, language, db)

        # Notify referrer if exists
        if referred_by:
            referrer = await db.get_user(referred_by)
            if referrer:
                msg = t(
                    referrer["language"],
                    "referral_info",
                    link="",
                    count="✅ +1 friend joined!",
                )
                try:
                    await callback.bot.send_message(referred_by, f"🎉 {msg}")
                except Exception:
                    pass
    else:
        await callback.answer("Error creating account", show_alert=True)


async def show_main_menu(message: Message, language: str, db: Database):
    """Show main menu to user"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(language, "settings"), callback_data="menu_settings")],
            [
                InlineKeyboardButton(
                    text=t(language, "subscription"), callback_data="menu_subscription"
                )
            ],
            [
                InlineKeyboardButton(
                    text=t(language, "invite_friend"), callback_data="menu_invite"
                )
            ],
        ]
    )
    await message.answer(t(language, "main_menu"), reply_markup=keyboard)
