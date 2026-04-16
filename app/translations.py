TRANSLATIONS = {
    "ar": {
        "welcome": """
✨ *مرحباً بك في بوت STC للشحن!*

أهلاً {name} 👋

🔹 يمكنك شحن رصيدك بكروت سوا
🔹 نظام رصيد داخلي آمن
🔹 سحب أرباح عبر Binance

اختر من القائمة أدناه:
""",
        "main_menu": "القائمة الرئيسية",
        "charge_card": "💳 شحن كرت سوا",
        "my_balance": "💰 رصيدي",
        "withdraw": "📤 سحب",
        "transactions": "📋 سجل العمليات",
        "settings": "⚙️ الإعدادات",
        "balance": """
💰 *رصيدك الحالي*

الرصيد: `${balance}` USDT

إجمالي الإيداعات: `{total_deposited}` USDT
إجمالي السحوبات: `{total_withdrawn}` USDT
""",
        "select_card_amount": "📦 اختر قيمة الكرت:",
        "enter_card_number": """
📝 *إدخال رقم الكرت*

اخترت كرت بـ `{amount}` USDT

💳 *أرسل رقم الكرت الآن*
(بدون مسافات أو رموز)
""",
        "confirm_charge": """
✅ *تأكيد عملية الشحن*

💳 الكرت: `{card_amount}` SAR
💵 المبلغ: `{price}` USDT

هل تريد تأكيد الشحن؟
""",
        "charge_success": """
✅ *تم شحن رصيدك بنجاح!*

💰 تم إضافة: `{amount}` USDT
💳 رصيدك الجديد: `{new_balance}` USDT

شكراً لاستخدامك خدمتنا!
""",
        "charge_cancelled": "❌ تم إلغاء عملية الشحن",
        "card_invalid": "❌ رقم الكرت غير صالح. تأكد من إدخال 14 رقماً.",
        "card_not_found": "❌ قيمة الكرت غير موجودة. يرجى اختيار من القائمة.",
        "insufficient_balance": "❌ رصيدك غير كافٍ لهذه العملية!",
        "withdraw_menu": """
📤 *سحب الأرباح*

💵 أدخل المبلغ المراد سحبه (USDT)

⚠️ الحد الأدنى للسحب: 5 USDT
⚠️ يتم التحويل عبر TRC20
""",
        "enter_binance_uid": """
💳 *أدخل معرف Binance*

أدخل Binance UID أو البريد الإلكتروني
المرتبط بحسابك

⚠️ تأكد من صحة البيانات قبل الإرسال
""",
        "withdraw_confirm": """
🔔 *تأكيد عملية السحب*

💵 المبلغ: `{amount}` USDT
👤 المستلم: `{binance_uid}`

⏳ جاري التحويل...
""",
        "withdraw_success": """
✅ *تم السحب بنجاح!*

💵 المبلغ: `{amount}` USDT
👤 المستلم: `{binance_uid}`
🧾 رقم العملية: `{tx_id}`

سيصل المبلغ خلال 5-30 دقيقة.
""",
        "withdraw_failed": """
❌ *فشلت عملية السحب*

{error}

💰 تم إعادة المبلغ لرصيدك
""",
        "transactions_log": "📋 *سجل العمليات*",
        "no_transactions": "📭 لا توجد عمليات سابقة",
        "admin_panel": "🧑‍💻 *لوحة التحكم*",
        "add_card_price": "➕ إضافة كرت وسعر",
        "edit_card_price": "✏️ تعديل سعر كرت",
        "view_stats": "📊 الإحصائيات",
        "broadcast": "📢 إذاعة رسالة",
        "manage_users": "👥 إدارة المستخدمين",
        "manage_admins": "👤 إدارة الأدمن",
        "back": "🔙 رجوع",
        "enter_card_amount": "📝 أدخل قيمة الكرت (بالريال)",
        "enter_price": "📝 أدخل السعر (بالدولار)",
        "price_added": "✅ تم إضافة الكرت بنجاح",
        "price_updated": "✅ تم تحديث السعر بنجاح",
        "enter_user_id": "📝 أدخل User ID",
        "user_banned": "✅ تم حظر المستخدم",
        "user_unbanned": "✅ تم إلغاء حظر المستخدم",
        "enter_broadcast": "📝 أدخل الرسالة للإذاعة",
        "broadcast_sent": "✅ تم إرسال الرسالة لـ {count} مستخدم",
        "stats": """
📊 *إحصائيات البوت*

👥 المستخدمين: {users_count}
💰 الرصيد الكلي: {total_balance} USDT
💳 إجمالي المبيعات: {total_sales} USDT
📤 إجمالي السحوبات: {total_withdrawals} USDT
""",
        "not_admin": "❌ ليس لديك صلاحية الوصول للوحة التحكم",
        "card_100": "كرت 100 ريال",
        "card_200": "كرت 200 ريال",
        "custom": "مخصص",
        "confirm": "✅ تأكيد",
        "cancel": "❌ إلغاء",
        "confirm_yes": "✅ نعم",
        "confirm_no": "❌ لا",
        "language": "🌍 اللغة",
        "ar": "🇸🇦 العربية",
        "en": "🇺🇸 English",
    },
    "en": {
        "welcome": """
✨ *Welcome to STC Charging Bot!*

Hello {name} 👋

🔹 Recharge your balance with Sawa cards
🔹 Secure internal balance system
🔹 Withdraw earnings via Binance

Choose from the menu below:
""",
        "main_menu": "Main Menu",
        "charge_card": "💳 Charge Sawa Card",
        "my_balance": "💰 My Balance",
        "withdraw": "📤 Withdraw",
        "transactions": "📋 Transaction History",
        "settings": "⚙️ Settings",
        "balance": """
💰 *Your Current Balance*

Balance: `${balance}` USDT

Total Deposited: `{total_deposited}` USDT
Total Withdrawn: `{total_withdrawn}` USDT
""",
        "select_card_amount": "📦 Select card value:",
        "enter_card_number": """
📝 *Enter Card Number*

Selected: `{amount}` USDT card

💳 *Send the card number now*
(without spaces or symbols)
""",
        "confirm_charge": """
✅ *Confirm Charging*

💳 Card: `{card_amount}` SAR
💵 Amount: `{price}` USDT

Do you want to confirm?
""",
        "charge_success": """
✅ *Balance recharged successfully!*

💰 Added: `{amount}` USDT
💳 New Balance: `{new_balance}` USDT

Thank you for using our service!
""",
        "charge_cancelled": "❌ Charge cancelled",
        "card_invalid": "❌ Invalid card number. Make sure to enter 14 digits.",
        "card_not_found": "❌ Card value not found. Please select from the list.",
        "insufficient_balance": "❌ Insufficient balance!",
        "withdraw_menu": """
📤 *Withdraw Earnings*

💵 Enter amount to withdraw (USDT)

⚠️ Minimum withdrawal: 5 USDT
⚠️ Transfer via TRC20
""",
        "enter_binance_uid": """
💳 *Enter Binance ID*

Enter your Binance UID or email
associated with your account

⚠️ Make sure the data is correct before sending
""",
        "withdraw_confirm": """
🔔 *Confirm Withdrawal*

💵 Amount: `{amount}` USDT
👤 Recipient: `{binance_uid}`

⏳ Processing...
""",
        "withdraw_success": """
✅ *Withdrawal Successful!*

💵 Amount: `{amount}` USDT
👤 Recipient: `{binance_uid}`
🧾 Transaction ID: `{tx_id}`

Amount will arrive in 5-30 minutes.
""",
        "withdraw_failed": """
❌ *Withdrawal Failed*

{error}

💰 Amount has been returned to your balance
""",
        "transactions_log": "📋 *Transaction History*",
        "no_transactions": "📭 No previous transactions",
        "admin_panel": "🧑‍💻 *Admin Panel*",
        "add_card_price": "➕ Add Card Price",
        "edit_card_price": "✏️ Edit Card Price",
        "view_stats": "📊 Statistics",
        "broadcast": "📢 Broadcast Message",
        "manage_users": "👥 Manage Users",
        "manage_admins": "👤 Manage Admins",
        "back": "🔙 Back",
        "enter_card_amount": "📝 Enter card value (SAR)",
        "enter_price": "📝 Enter price (USD)",
        "price_added": "✅ Card added successfully",
        "price_updated": "✅ Price updated successfully",
        "enter_user_id": "📝 Enter User ID",
        "user_banned": "✅ User banned",
        "user_unbanned": "✅ User unbanned",
        "enter_broadcast": "📝 Enter message to broadcast",
        "broadcast_sent": "✅ Message sent to {count} users",
        "stats": """
📊 *Bot Statistics*

👥 Users: {users_count}
💰 Total Balance: {total_balance} USDT
💳 Total Sales: {total_sales} USDT
📤 Total Withdrawals: {total_withdrawals} USDT
""",
        "not_admin": "❌ You don't have access to admin panel",
        "card_100": "100 SAR Card",
        "card_200": "200 SAR Card",
        "custom": "Custom",
        "confirm": "✅ Confirm",
        "cancel": "❌ Cancel",
        "confirm_yes": "✅ Yes",
        "confirm_no": "❌ No",
        "language": "🌍 Language",
        "ar": "🇸🇦 Arabic",
        "en": "🇺🇸 English",
    }
}


def get_text(key: str, lang: str = "ar", **kwargs) -> str:
    text = TRANSLATIONS.get(lang, TRANSLATIONS["ar"]).get(key, key)
    try:
        return text.format(**kwargs)
    except (KeyError, ValueError):
        return text
