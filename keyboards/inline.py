from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

charge_cd = CallbackData("charge", "action", "amount", "charge_id")
admin_cd = CallbackData("admin", "action", "value")
user_cd = CallbackData("user", "action", "user_id")
card_cd = CallbackData("card", "amount")
back_cd = CallbackData("back", "to")
confirm_cd = CallbackData("confirm", "type", "id")


def main_menu_keyboard(lang: str = "ar") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    if lang == "ar":
        keyboard.row(
            InlineKeyboardButton("💳 شحن كرت سوا", callback_data="charge:select_amount:0:0"),
        )
        keyboard.row(
            InlineKeyboardButton("💰 رصيدي", callback_data="user:balance"),
        )
        keyboard.row(
            InlineKeyboardButton("📤 سحب", callback_data="user:withdraw"),
            InlineKeyboardButton("📋 سجل العمليات", callback_data="user:transactions"),
        )
        keyboard.row(
            InlineKeyboardButton("🌍 اللغة", callback_data="user:language"),
        )
    else:
        keyboard.row(
            InlineKeyboardButton("💳 Charge Sawa Card", callback_data="charge:select_amount:0:0"),
        )
        keyboard.row(
            InlineKeyboardButton("💰 My Balance", callback_data="user:balance"),
        )
        keyboard.row(
            InlineKeyboardButton("📤 Withdraw", callback_data="user:withdraw"),
            InlineKeyboardButton("📋 Transactions", callback_data="user:transactions"),
        )
        keyboard.row(
            InlineKeyboardButton("🌍 Language", callback_data="user:language"),
        )
    return keyboard


def card_amounts_keyboard(prices: list, lang: str = "ar") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    for price in prices:
        amount = price["card_amount"]
        usd = price["price_usd"]
        if lang == "ar":
            btn_text = f"💳 كرت {amount} SAR - ${usd}"
        else:
            btn_text = f"💳 {amount} SAR Card - ${usd}"
        keyboard.add(
            InlineKeyboardButton(btn_text, callback_data=card_cd.new(amount=amount))
        )

    keyboard.row(
        InlineKeyboardButton("🔙 رجوع" if lang == "ar" else "🔙 Back", callback_data=back_cd.new(to="main"))
    )
    return keyboard


def confirm_keyboard(charge_id: int, lang: str = "ar") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    if lang == "ar":
        keyboard.row(
            InlineKeyboardButton("✅ تأكيد", callback_data=confirm_cd.new(type="charge", id=charge_id)),
            InlineKeyboardButton("❌ إلغاء", callback_data=confirm_cd.new(type="cancel", id=charge_id)),
        )
    else:
        keyboard.row(
            InlineKeyboardButton("✅ Confirm", callback_data=confirm_cd.new(type="charge", id=charge_id)),
            InlineKeyboardButton("❌ Cancel", callback_data=confirm_cd.new(type="cancel", id=charge_id)),
        )
    return keyboard


def language_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        InlineKeyboardButton("🇸🇦 العربية", callback_data="user:set_lang:ar"),
        InlineKeyboardButton("🇺🇸 English", callback_data="user:set_lang:en"),
    )
    return keyboard


def back_to_main_keyboard(lang: str = "ar") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔙 القائمة الرئيسية" if lang == "ar" else "🔙 Main Menu", callback_data=back_cd.new(to="main"))
    )
    return keyboard


def admin_panel_keyboard(lang: str = "ar") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    if lang == "ar":
        keyboard.row(
            InlineKeyboardButton("➕ إضافة كرت", callback_data=admin_cd.new(action="add_card", value="")),
            InlineKeyboardButton("✏️ تعديل كرت", callback_data=admin_cd.new(action="edit_card", value="")),
        )
        keyboard.row(
            InlineKeyboardButton("📊 الإحصائيات", callback_data=admin_cd.new(action="stats", value="")),
            InlineKeyboardButton("📢 إذاعة", callback_data=admin_cd.new(action="broadcast", value="")),
        )
        keyboard.row(
            InlineKeyboardButton("🚫 حظر مستخدم", callback_data=admin_cd.new(action="ban_user", value="")),
            InlineKeyboardButton("✅ إلغاء الحظر", callback_data=admin_cd.new(action="unban_user", value="")),
        )
        keyboard.row(
            InlineKeyboardButton("👤 إضافة أدمن", callback_data=admin_cd.new(action="add_admin", value="")),
            InlineKeyboardButton("❌ إزالة أدمن", callback_data=admin_cd.new(action="remove_admin", value="")),
        )
        keyboard.row(
            InlineKeyboardButton("📋 سجل العمليات", callback_data=admin_cd.new(action="all_transactions", value="")),
        )
    else:
        keyboard.row(
            InlineKeyboardButton("➕ Add Card", callback_data=admin_cd.new(action="add_card", value="")),
            InlineKeyboardButton("✏️ Edit Card", callback_data=admin_cd.new(action="edit_card", value="")),
        )
        keyboard.row(
            InlineKeyboardButton("📊 Statistics", callback_data=admin_cd.new(action="stats", value="")),
            InlineKeyboardButton("📢 Broadcast", callback_data=admin_cd.new(action="broadcast", value="")),
        )
        keyboard.row(
            InlineKeyboardButton("🚫 Ban User", callback_data=admin_cd.new(action="ban_user", value="")),
            InlineKeyboardButton("✅ Unban User", callback_data=admin_cd.new(action="unban_user", value="")),
        )
        keyboard.row(
            InlineKeyboardButton("👤 Add Admin", callback_data=admin_cd.new(action="add_admin", value="")),
            InlineKeyboardButton("❌ Remove Admin", callback_data=admin_cd.new(action="remove_admin", value="")),
        )
        keyboard.row(
            InlineKeyboardButton("📋 All Transactions", callback_data=admin_cd.new(action="all_transactions", value="")),
        )
    keyboard.row(
        InlineKeyboardButton("🔙 رجوع" if lang == "ar" else "🔙 Back", callback_data=back_cd.new(to="main"))
    )
    return keyboard


def cancel_keyboard(lang: str = "ar") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("❌ إلغاء", callback_data=back_cd.new(to="main"))
    )
    return keyboard
