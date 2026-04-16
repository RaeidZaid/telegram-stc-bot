from aiogram import Router, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.database import (
    is_admin, add_admin, remove_admin, get_stats, get_cards_prices,
    add_card_price, get_all_users, get_all_transactions,
    ban_user, unban_user, get_user
)
from app.translations import get_text
from keyboards.inline import admin_panel_keyboard, back_to_main_keyboard
from config.settings import ADMIN_IDS

router = Router()

admin_cd_data = {}


class AdminStates(StatesGroup):
    waiting_card_amount = State()
    waiting_card_price = State()
    waiting_broadcast = State()
    waiting_user_id = State()
    waiting_admin_id = State()


def is_user_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(commands=["panel"])
async def cmd_admin_panel(message: Message):
    user_id = message.from_user.id

    if not is_user_admin(user_id) and not await is_admin(user_id):
        await message.answer(get_text("not_admin", "ar"))
        return

    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    await message.answer(
        get_text("admin_panel", lang),
        reply_markup=admin_panel_keyboard(lang),
        parse_mode="Markdown"
    )


@router.callback_query(lambda c: c.data.startswith("admin:"))
async def admin_callback(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    if not is_user_admin(user_id) and not await is_admin(user_id):
        await call.answer(get_text("not_admin", "ar"), show_alert=True)
        return

    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    data = call.data.split(":")
    action = data[1]

    if action == "stats":
        stats = await get_stats()

        text = get_text("stats", lang,
                        users_count=stats["users_count"],
                        total_balance=stats["total_balance"],
                        total_sales=stats["total_sales"],
                        total_withdrawals=stats["total_withdrawals"])

        await call.message.edit_text(text, reply_markup=admin_panel_keyboard(lang), parse_mode="Markdown")

    elif action == "add_card":
        admin_cd_data[user_id] = {"action": "add_card"}
        await call.message.edit_text(
            get_text("enter_card_amount", lang),
            reply_markup=back_to_main_keyboard(lang)
        )
        await AdminStates.waiting_card_amount.set()

    elif action == "edit_card":
        prices = await get_cards_prices()

        if not prices:
            await call.answer("لا توجد كروت متوفرة", show_alert=True)
            return

        text = "✏️ اختر كرت لتعديل سعره:\n\n"
        keyboard = InlineKeyboardMarkup()

        for p in prices:
            text += f"💳 كرت {p['card_amount']} SAR - ${p['price_usd']}\n"
            keyboard.add(
                InlineKeyboardButton(
                    f"✏️ {p['card_amount']} SAR - ${p['price_usd']}",
                    callback_data=f"admin_edit:{p['card_amount']}"
                )
            )

        keyboard.add(
            InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")
        )

        await call.message.edit_text(text, reply_markup=keyboard)

    elif action == "broadcast":
        admin_cd_data[user_id] = {"action": "broadcast"}
        await call.message.edit_text(
            get_text("enter_broadcast", lang),
            reply_markup=back_to_main_keyboard(lang)
        )
        await AdminStates.waiting_broadcast.set()

    elif action == "ban_user":
        admin_cd_data[user_id] = {"action": "ban"}
        await call.message.edit_text(
            get_text("enter_user_id", lang),
            reply_markup=back_to_main_keyboard(lang)
        )
        await AdminStates.waiting_user_id.set()

    elif action == "unban_user":
        admin_cd_data[user_id] = {"action": "unban"}
        await call.message.edit_text(
            get_text("enter_user_id", lang),
            reply_markup=back_to_main_keyboard(lang)
        )
        await AdminStates.waiting_user_id.set()

    elif action == "add_admin":
        admin_cd_data[user_id] = {"action": "add_admin"}
        await call.message.edit_text(
            "📝 أدخل User ID للأدمن الجديد:",
            reply_markup=back_to_main_keyboard(lang)
        )
        await AdminStates.waiting_admin_id.set()

    elif action == "remove_admin":
        admin_cd_data[user_id] = {"action": "remove_admin"}
        await call.message.edit_text(
            "📝 أدخل User ID للأدمن المراد إزالته:",
            reply_markup=back_to_main_keyboard(lang)
        )
        await AdminStates.waiting_admin_id.set()

    elif action == "all_transactions":
        transactions = await get_all_transactions(50)

        if not transactions:
            await call.message.edit_text(
                "📭 لا توجد عمليات",
                reply_markup=back_to_main_keyboard(lang)
            )
            return

        text = "📋 *آخر 50 عملية:*\n\n"

        for tx in transactions:
            username = tx.get("username") or "Unknown"
            tx_type = tx["type"]
            amount = tx["amount"]
            desc = tx["description"]

            type_emoji = "💳" if tx_type == "charge" else "💰" if tx_type == "deposit" else "📤"
            text += f"{type_emoji} @{username}: {amount} USDT\n"
            text += f"   📝 {desc}\n\n"

        await call.message.edit_text(text, reply_markup=back_to_main_keyboard(lang), parse_mode="Markdown")


@router.callback_query(lambda c: c.data.startswith("admin_edit:"))
async def edit_card_price(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = call.from_user.id

    if not is_user_admin(user_id) and not await is_admin(user_id):
        await call.answer(get_text("not_admin", "ar"), show_alert=True)
        return

    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    card_amount = int(callback_data["data"].split(":")[1])
    admin_cd_data[user_id] = {"action": "edit_card", "card_amount": card_amount}

    await call.message.edit_text(
        f"✏️ أدخل السعر الجديد لكرت {card_amount} SAR (بالدولار):",
        reply_markup=back_to_main_keyboard(lang)
    )
    await AdminStates.waiting_card_price.set()


@router.callback_query(lambda c: c.data == "back_to_admin")
async def back_to_admin(call: CallbackQuery, state: FSMContext):
    await state.finish()

    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    await call.message.edit_text(
        get_text("admin_panel", lang),
        reply_markup=admin_panel_keyboard(lang),
        parse_mode="Markdown"
    )


@router.message(state=AdminStates.waiting_card_amount)
async def process_card_amount(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    try:
        amount = int(message.text.strip())
    except ValueError:
        await message.answer("❌ يرجى إدخال رقم صحيح")
        return

    admin_cd_data[user_id] = {"action": "add_card", "card_amount": amount}
    await state.finish()

    await message.answer(
        get_text("enter_price", lang),
        reply_markup=back_to_main_keyboard(lang)
    )
    await AdminStates.waiting_card_price.set()


@router.message(state=AdminStates.waiting_card_price)
async def process_card_price(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    try:
        price = float(message.text.strip())
    except ValueError:
        await message.answer("❌ يرجى إدخال سعر صحيح")
        return

    action_data = admin_cd_data.get(user_id, {})

    if action_data.get("action") == "add_card":
        await add_card_price(action_data.get("card_amount", 0), price)
        await message.answer(
            get_text("price_added", lang),
            reply_markup=admin_panel_keyboard(lang)
        )
    elif action_data.get("action") == "edit_card":
        await add_card_price(action_data.get("card_amount", 0), price)
        await message.answer(
            get_text("price_updated", lang),
            reply_markup=admin_panel_keyboard(lang)
        )

    await state.finish()
    if user_id in admin_cd_data:
        del admin_cd_data[user_id]


@router.message(state=AdminStates.waiting_broadcast)
async def process_broadcast(message: Message, state: FSMContext):
    from aiogram import Bot

    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    broadcast_text = message.text.strip()

    if not broadcast_text:
        await message.answer("❌ الرسالة فارغة")
        return

    users = await get_all_users()
    sent_count = 0

    for user_data in users:
        try:
            bot = Bot.get_current()
            await bot.send_message(
                user_data["user_id"],
                f"📢 *إعلان:*\n\n{broadcast_text}",
                parse_mode="Markdown"
            )
            sent_count += 1
        except Exception:
            pass

    await state.finish()

    await message.answer(
        get_text("broadcast_sent", lang, count=sent_count),
        reply_markup=admin_panel_keyboard(lang)
    )


@router.message(state=AdminStates.waiting_user_id)
async def process_user_id(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    try:
        target_user_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ User ID غير صالح")
        return

    action_data = admin_cd_data.get(user_id, {})

    if action_data.get("action") == "ban":
        await ban_user(target_user_id, "حظر من الأدمن")
        await message.answer(
            get_text("user_banned", lang),
            reply_markup=admin_panel_keyboard(lang)
        )
    elif action_data.get("action") == "unban":
        await unban_user(target_user_id)
        await message.answer(
            get_text("user_unbanned", lang),
            reply_markup=admin_panel_keyboard(lang)
        )

    await state.finish()
    if user_id in admin_cd_data:
        del admin_cd_data[user_id]


@router.message(state=AdminStates.waiting_admin_id)
async def process_admin_id(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    try:
        target_admin_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ User ID غير صالح")
        return

    action_data = admin_cd_data.get(user_id, {})

    if action_data.get("action") == "add_admin":
        await add_admin(target_admin_id)
        await message.answer(
            "✅ تم إضافة الأدمن بنجاح",
            reply_markup=admin_panel_keyboard(lang)
        )
    elif action_data.get("action") == "remove_admin":
        await remove_admin(target_admin_id)
        await message.answer(
            "✅ تم إزالة الأدمن بنجاح",
            reply_markup=admin_panel_keyboard(lang)
        )

    await state.finish()
    if user_id in admin_cd_data:
        del admin_cd_data[user_id]
