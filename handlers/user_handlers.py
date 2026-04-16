from aiogram import Router, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.database import (
    get_user, get_balance, update_balance, get_transactions,
    get_cards_prices, get_card_price, create_pending_charge,
    confirm_charge, cancel_charge, get_pending_charge, update_user_language
)
from app.translations import get_text
from keyboards.inline import (
    main_menu_keyboard, card_amounts_keyboard, confirm_keyboard,
    language_keyboard, back_to_main_keyboard, card_cd, back_cd, confirm_cd
)
from utils.binance import withdraw_usdt

router = Router()

charge_states = {}


class ChargeStates(StatesGroup):
    waiting_card_number = State()


class WithdrawStates(StatesGroup):
    waiting_amount = State()
    waiting_binance_uid = State()


@router.message(commands=["start"])
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    charge_states[user_id] = {"lang": lang}

    name = message.from_user.first_name or "there"
    welcome_text = get_text("welcome", lang, name=name)

    await message.answer(welcome_text, reply_markup=main_menu_keyboard(lang), parse_mode="Markdown")


@router.message(commands=["balance"])
async def cmd_balance(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    balance = await get_balance(user_id)

    from app.database import DATABASE_PATH
    import aiosqlite
    total_deposited = 0
    total_withdrawn = 0

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT total_deposited, total_withdrawn FROM balances WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                total_deposited = row[0]
                total_withdrawn = row[1]

    await message.answer(
        get_text("balance", lang,
                 balance=balance,
                 total_deposited=total_deposited,
                 total_withdrawn=total_withdrawn),
        parse_mode="Markdown",
        reply_markup=back_to_main_keyboard(lang)
    )


@router.callback_query(back_cd.filter(to="main"))
async def back_to_main(call: CallbackQuery, state: FSMContext):
    await state.finish()

    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    name = call.from_user.first_name or "there"
    welcome_text = get_text("welcome", lang, name=name)

    await call.message.edit_text(welcome_text, reply_markup=main_menu_keyboard(lang), parse_mode="Markdown")


@router.callback_query(card_cd.filter())
async def select_card_amount(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    amount = int(callback_data["amount"])
    price = await get_card_price(amount)

    if not price:
        await call.answer(get_text("card_not_found", lang), show_alert=True)
        return

    charge_id = await create_pending_charge(user_id, "", amount, price)

    charge_states[user_id] = {
        "lang": lang,
        "charge_id": charge_id,
        "card_amount": amount,
        "card_price": price
    }

    await call.message.edit_text(
        get_text("enter_card_number", lang, amount=amount),
        reply_markup=back_to_main_keyboard(lang),
        parse_mode="Markdown"
    )
    await ChargeStates.waiting_card_number.set()


@router.message(state=ChargeStates.waiting_card_number)
async def process_card_number(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    card_number = message.text.strip()

    if not card_number.isdigit() or len(card_number) != 14:
        await message.answer(get_text("card_invalid", lang))
        return

    charge_id = charge_states.get(user_id, {}).get("charge_id", 0)

    if charge_id:
        from app.database import DATABASE_PATH
        import aiosqlite
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(
                "UPDATE card_charges SET card_number = ? WHERE id = ?",
                (card_number, charge_id)
            )
            await db.commit()

    await state.finish()

    amount = charge_states.get(user_id, {}).get("card_amount", 0)
    price = charge_states.get(user_id, {}).get("card_price", 0)

    keyboard = confirm_keyboard(charge_id, lang)

    await message.answer(
        get_text("confirm_charge", lang, card_amount=amount, price=price),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


@router.callback_query(confirm_cd.filter(type="charge"))
async def confirm_charge_callback(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()

    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    charge_id = int(callback_data["id"])
    charge = await get_pending_charge(charge_id)

    if not charge or charge["user_id"] != user_id:
        await call.answer("خطأ في العملية", show_alert=True)
        return

    await confirm_charge(charge_id)

    amount = charge["price_usd"]
    await update_balance(user_id, amount, "charge", f"شحن كرت {charge['card_amount']} SAR")

    new_balance = await get_balance(user_id)

    await call.message.edit_text(
        get_text("charge_success", lang, amount=amount, new_balance=new_balance),
        parse_mode="Markdown",
        reply_markup=back_to_main_keyboard(lang)
    )

    if user_id in charge_states:
        del charge_states[user_id]


@router.callback_query(confirm_cd.filter(type="cancel"))
async def cancel_charge_callback(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()

    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    charge_id = int(callback_data["id"])
    await cancel_charge(charge_id)

    if user_id in charge_states:
        del charge_states[user_id]

    await call.message.edit_text(
        get_text("charge_cancelled", lang),
        reply_markup=back_to_main_keyboard(lang)
    )


@router.callback_query(lambda c: c.data == "charge:select_amount:0:0")
async def select_card_amount_menu(call: CallbackQuery):
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    prices = await get_cards_prices()

    if not prices:
        await call.answer("لا توجد كروت متوفرة حالياً", show_alert=True)
        return

    await call.message.edit_text(
        get_text("select_card_amount", lang),
        reply_markup=card_amounts_keyboard(prices, lang)
    )


@router.callback_query(lambda c: c.data == "user:balance")
async def show_balance(call: CallbackQuery):
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    balance = await get_balance(user_id)

    from app.database import DATABASE_PATH
    import aiosqlite
    total_deposited = 0
    total_withdrawn = 0

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT total_deposited, total_withdrawn FROM balances WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                total_deposited = row[0]
                total_withdrawn = row[1]

    await call.message.edit_text(
        get_text("balance", lang,
                 balance=balance,
                 total_deposited=total_deposited,
                 total_withdrawn=total_withdrawn),
        parse_mode="Markdown",
        reply_markup=back_to_main_keyboard(lang)
    )


@router.callback_query(lambda c: c.data == "user:withdraw")
async def start_withdraw(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    balance = await get_balance(user_id)

    if balance < 5:
        await call.answer(get_text("insufficient_balance", lang), show_alert=True)
        return

    charge_states[user_id] = {"lang": lang}

    await call.message.edit_text(
        get_text("withdraw_menu", lang),
        reply_markup=back_to_main_keyboard(lang),
        parse_mode="Markdown"
    )
    await WithdrawStates.waiting_amount.set()


@router.message(state=WithdrawStates.waiting_amount)
async def process_withdraw_amount(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    try:
        amount = float(message.text.strip())
    except ValueError:
        await message.answer("❌ يرجى إدخال مبلغ صحيح")
        return

    balance = await get_balance(user_id)

    if amount < 5:
        await message.answer("❌ الحد الأدنى للسحب 5 USDT")
        return

    if amount > balance:
        await message.answer(get_text("insufficient_balance", lang))
        return

    charge_states[user_id] = charge_states.get(user_id, {})
    charge_states[user_id]["withdraw_amount"] = amount
    charge_states[user_id]["lang"] = lang

    await state.finish()

    await message.answer(
        get_text("enter_binance_uid", lang),
        reply_markup=back_to_main_keyboard(lang),
        parse_mode="Markdown"
    )
    await WithdrawStates.waiting_binance_uid.set()


@router.message(state=WithdrawStates.waiting_binance_uid)
async def process_binance_uid(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    binance_uid = message.text.strip()

    if not binance_uid or len(binance_uid) < 5:
        await message.answer("❌ معرف Binance غير صالح")
        return

    amount = charge_states.get(user_id, {}).get("withdraw_amount", 0)

    await state.finish()

    await message.answer(
        get_text("withdraw_confirm", lang, amount=amount, binance_uid=binance_uid),
        parse_mode="Markdown"
    )

    result = await withdraw_usdt(binance_uid, amount)

    if result.get("success"):
        await update_balance(user_id, amount, "withdraw", f"سحب إلى {binance_uid}")

        await message.answer(
            get_text("withdraw_success", lang,
                     amount=amount,
                     binance_uid=binance_uid,
                     tx_id=result.get("tx_id", "N/A")),
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard(lang)
        )
    else:
        await message.answer(
            get_text("withdraw_failed", lang, error=result.get("error", "Unknown error")),
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard(lang)
        )

    if user_id in charge_states:
        del charge_states[user_id]


@router.callback_query(lambda c: c.data == "user:transactions")
async def show_transactions(call: CallbackQuery):
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    transactions = await get_transactions(user_id)

    if not transactions:
        await call.message.edit_text(
            get_text("no_transactions", lang),
            reply_markup=back_to_main_keyboard(lang)
        )
        return

    text = get_text("transactions_log", lang) + "\n\n"

    for tx in transactions[:10]:
        tx_type = tx["type"]
        amount = tx["amount"]
        desc = tx["description"]
        status = tx["status"]

        type_emoji = "💳" if tx_type == "charge" else "💰" if tx_type == "deposit" else "📤"
        text += f"{type_emoji} {tx_type}: {amount} USDT\n"
        text += f"   📝 {desc}\n"
        text += f"   📌 {status}\n\n"

    await call.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=back_to_main_keyboard(lang)
    )


@router.callback_query(lambda c: c.data == "user:language")
async def change_language(call: CallbackQuery):
    await call.message.edit_text(
        "🌍 اختر اللغة / Choose Language:",
        reply_markup=language_keyboard()
    )


@router.callback_query(lambda c: c.data.startswith("user:set_lang:"))
async def set_language(call: CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    lang = callback_data["value"]

    await update_user_language(user_id, lang)
    charge_states[user_id] = {"lang": lang}

    name = call.from_user.first_name or "there"
    welcome_text = get_text("welcome", lang, name=name)

    await call.message.edit_text(welcome_text, reply_markup=main_menu_keyboard(lang), parse_mode="Markdown")
