# STC Charging Bot - بوت شحن سوا

بوت تيليجرام احترافي لشحن كروت سوا مع نظام رصيد داخلي وإدارة أدمن متكاملة.

## المميزات

- 💳 شحن كروت سوا (STC)
- 💰 نظام رصيد داخلي
- 📤 سحب أرباح عبر Binance API
- 🧑‍💻 لوحة تحكم أدمن متكاملة
- 🌐 دعم اللغتين العربية والإنجليزية
- 🚀 جاهز للنشر على Railway

## المتطلبات

- Python 3.13.1+
- pip

## التثبيت المحلي

```bash
# 1. تأكد من تثبيت Python 3.13
python --version  # يجب أن يعرض Python 3.13.x

# 2. استنسخ المشروع
git clone <repo-url>
cd telegram-stc-bot

# 3. أنشئ بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 4. ثبّت المكتبات
pip install -r requirements.txt

# 4. أنشئ ملف .env
cp .env.example .env

# 5. عدّل الملف وأضف بياناتك
# BOT_TOKEN=توكن البوت من BotFather
# ADMIN_IDS=أيدي الحسابات الإدارية
# BINANCE_API_KEY=مفتاح Binance API
# BINANCE_API_SECRET=سر Binance API

# 6. شغّل البوت
python main.py
```

## النشر على Railway

### الخطوة 1: إنشاء بوت تيليجرام

1. افتح @BotFather على تيليجرام
2. أرسل `/newbot`
3. اختر اسم للبوت
4. احفظ التوكن

### الخطوة 2: إعداد Railway

1. اذهب إلى [railway.app](https://railway.app)
2. سجّل الدخول بحساب GitHub
3. انقر "New Project" > "Deploy from GitHub"
4. اختر المستودع

### الخطوة 3: إضافة المتغيرات

في لوحة Railway، أضف المتغيرات التالية:

```
BOT_TOKEN = your_bot_token_from_botfather
ADMIN_IDS = 123456789,987654321
BINANCE_API_KEY = your_binance_api_key
BINANCE_API_SECRET = your_binance_api_secret
WEBHOOK_HOST = https://your-app-name.up.railway.app
WEBHOOK_PATH = /webhook
```

### الخطوة 4: إعداد Binance API

#### إنشاء API Key:
1. سجّل الدخول على [Binance](https://www.binance.com)
2. اذهب إلى Dashboard > API Management
3. أنشئ API Key جديد
4. فعّل "Enable Spot & Margin Trading"
5. **مهم**: فعّل "Enable Withdrawals"

#### الصلاحيات المطلوبة:
- Spot Trading (للقراءة)
- Wallet (للتحويلات)

#### الأمان:
- لا تشارك API Secret مع أحد
- استخدم IP restriction
- فعّل 2FA

### الخطوة 5: إضافة الأدمن

#### الطريقة 1 - من الكود:
عدّل ملف `.env`:
```
ADMIN_IDS=123456789,987654321,111222333
```
الأرقام هي User ID من تيليجرام.

#### الطريقة 2 - من البوت نفسه:
1. شغّل البوت
2. المستخدم الأدمن يرسل `/panel`
3. اختيار "إدارة الأدمن"
4. إدخال User ID

## أوامر البوت

### للمستخدم:
| الأمر | الوصف |
|-------|-------|
| `/start` | بدء البوت |
| `/balance` | عرض الرصيد |

### للأدمن:
| الأمر | الوصف |
|-------|-------|
| `/panel` | لوحة التحكم |

## هيكل المشروع

```
telegram-stc-bot/
├── app/
│   ├── database.py      # إدارة قاعدة البيانات
│   └── translations.py  # النصوص والترجمة
├── config/
│   └── settings.py      # الإعدادات
├── handlers/
│   ├── admin_handlers.py
│   └── user_handlers.py
├── keyboards/
│   └── inline.py        # الأزرار
├── middlewares/
│   └── middleware.py    # التحقق من الحظر
├── utils/
│   └── binance.py       # تكامل Binance
├── data/                # قاعدة البيانات
├── main.py              # الملف الرئيسي
├── requirements.txt     # المكتبات
├── runtime.txt          # إصدار Python
├── pyproject.toml       # إعدادات المشروع
├── Procfile
├── .env.example
└── README.md
```

**ملاحظة:** ملف `runtime.txt` يحدد Python 3.13.1 لـ Railway.

## قاعدة البيانات

البوت يستخدم SQLite افتراضياً. الجداول:

- `users` - بيانات المستخدمين
- `balances` - أرصدة المستخدمين
- `cards_prices` - أسعار الكروت
- `transactions` - سجل العمليات
- `admins` - قائمة الأدمن
- `banned_users` - المحظورين
- `card_charges` - عمليات الشحن

## إعداد كروت سوا

بعد تشغيل البوت، الأدمن يرسل `/panel` ثم:
1. اختيار "➕ إضافة كرت"
2. إدخال قيمة الكرت (مثلاً: 100)
3. إدخال السعر بالدولار (مثلاً: 2.5)

## حل المشاكل

### بوت لا يستجيب:
- تأكد من صحة BOT_TOKEN
- تأكد من المتغيرات في Railway

### السحب يفشل:
- تأكد من صحة API Key و Secret
- تأكد من تفعيل الصلاحيات
- راجع رصيد المحفظة

### قاعدة البيانات:
- تأكد من وجود مجلد `data/`
- تأكد من صلاحيات الكتابة

## المساعدة

للمساعدة أو الإبلاغ عن مشكلة:
- GitHub Issues

## الترخيص

MIT License
