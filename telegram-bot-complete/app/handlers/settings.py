from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.db import Database
from app.translations import t
from app.config import AVAILABLE_ASSETS, FREQUENCY_INSTANT, FREQUENCY_DAILY, FREQUENCY_WEEKLY

router = Router()


@router.callback_query(F.data == "menu_settings")
async def show_settings(callback: CallbackQuery, db: Database):
    """Show settings menu"""
    user = await db.get_user(callback.from_user.id)
    settings = await db.get_user_settings(callback.from_user.id)

    if not user or not settings:
        await callback.answer("Error loading settings", show_alert=True)
        return

    lang = user["language"]

    # Show current settings and options
    current_assets = settings["assets"]
    current_freq = settings["frequency"]

    assets_text = ", ".join(current_assets) if current_assets else t(lang, "no_assets")
    freq_text = {
        FREQUENCY_INSTANT: t(lang, "instant"),
        FREQUENCY_DAILY: t(lang, "daily"),
        FREQUENCY_WEEKLY: t(lang, "weekly"),
    }.get(current_freq, current_freq)

    text = t(lang, "current_settings", assets=assets_text, frequency=freq_text)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "select_assets"), callback_data="settings_assets")],
            [
                InlineKeyboardButton(
                    text=t(lang, "select_frequency"), callback_data="settings_frequency"
                )
            ],
            [InlineKeyboardButton(text=t(lang, "back"), callback_data="settings_back")],
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "settings_assets")
async def show_asset_selection(callback: CallbackQuery, db: Database):
    """Show asset selection menu"""
    user = await db.get_user(callback.from_user.id)
    settings = await db.get_user_settings(callback.from_user.id)

    if not user or not settings:
        await callback.answer("Error", show_alert=True)
        return

    lang = user["language"]
    current_assets = settings["assets"]

    # Create buttons for all available assets
    buttons = []

    # Group by market
    for market, assets in AVAILABLE_ASSETS.items():
        market_label = t(lang, f"assets_{market}")
        buttons.append([InlineKeyboardButton(text=market_label, callback_data="noop")])

        for asset in assets:
            is_selected = asset in current_assets
            label = f"{'✅' if is_selected else '☐'} {asset}"
            buttons.append(
                [InlineKeyboardButton(text=label, callback_data=f"toggle_asset_{asset}")]
            )

    buttons.append([InlineKeyboardButton(text=t(lang, "back"), callback_data="menu_settings")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(t(lang, "select_assets"), reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("toggle_asset_"))
async def toggle_asset(callback: CallbackQuery, db: Database):
    """Toggle asset selection"""
    asset = callback.data.split("_", 2)[2]

    settings = await db.get_user_settings(callback.from_user.id)
    if not settings:
        await callback.answer("Error", show_alert=True)
        return

    current_assets = settings["assets"]

    if asset in current_assets:
        current_assets.remove(asset)
    else:
        current_assets.append(asset)

    await db.update_user_settings(callback.from_user.id, assets=current_assets)

    # Refresh the menu
    await show_asset_selection(callback, db)


@router.callback_query(F.data == "settings_frequency")
async def show_frequency_selection(callback: CallbackQuery, db: Database):
    """Show frequency selection menu"""
    user = await db.get_user(callback.from_user.id)
    settings = await db.get_user_settings(callback.from_user.id)

    if not user or not settings:
        await callback.answer("Error", show_alert=True)
        return

    lang = user["language"]
    current_freq = settings["frequency"]

    buttons = []
    for freq in [FREQUENCY_INSTANT, FREQUENCY_DAILY, FREQUENCY_WEEKLY]:
        is_selected = freq == current_freq
        label = f"{'✅' if is_selected else '☐'} {t(lang, freq)}"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"set_freq_{freq}")])

    buttons.append([InlineKeyboardButton(text=t(lang, "back"), callback_data="menu_settings")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(t(lang, "select_frequency"), reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("set_freq_"))
async def set_frequency(callback: CallbackQuery, db: Database):
    """Set notification frequency"""
    frequency = callback.data.split("_", 2)[2]

    await db.update_user_settings(callback.from_user.id, frequency=frequency)

    user = await db.get_user(callback.from_user.id)
    lang = user["language"]

    await callback.answer(t(lang, "settings_updated"), show_alert=True)

    # Go back to settings menu
    await show_settings(callback, db)


@router.callback_query(F.data == "settings_back")
async def settings_back(callback: CallbackQuery, db: Database):
    """Go back to main menu from settings"""
    user = await db.get_user(callback.from_user.id)
    lang = user["language"]

    from app.handlers.start import show_main_menu

    await callback.message.delete()
    await show_main_menu(callback.message, lang, db)
    await callback.answer()


@router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):
    """No-op callback for category headers"""
    await callback.answer()
