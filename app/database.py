import aiosqlite
from datetime import datetime
from typing import Optional, List, Dict, Any

DATABASE_PATH = "data/database.db"


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language TEXT DEFAULT 'ar',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS balances (
                user_id INTEGER PRIMARY KEY,
                balance REAL DEFAULT 0.0,
                total_deposited REAL DEFAULT 0.0,
                total_withdrawn REAL DEFAULT 0.0,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS cards_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_amount INTEGER UNIQUE,
                price_usd REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,
                amount REAL,
                description TEXT,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS banned_users (
                user_id INTEGER PRIMARY KEY,
                banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reason TEXT
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS card_charges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                card_number TEXT,
                card_amount INTEGER,
                price_usd REAL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)

        await db.commit()


async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def create_user(user_id: int, username: str, first_name: str, language: str = "ar"):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name, language) VALUES (?, ?, ?, ?)",
            (user_id, username, first_name, language)
        )
        await db.execute(
            "INSERT OR IGNORE INTO balances (user_id) VALUES (?)",
            (user_id,)
        )
        await db.commit()


async def get_balance(user_id: int) -> float:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT balance FROM balances WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0.0


async def update_balance(user_id: int, amount: float, transaction_type: str, description: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        if transaction_type in ["deposit", "charge", "refund"]:
            await db.execute(
                "UPDATE balances SET balance = balance + ?, total_deposited = total_deposited + ? WHERE user_id = ?",
                (amount, amount, user_id)
            )
        elif transaction_type == "withdraw":
            await db.execute(
                "UPDATE balances SET balance = balance - ?, total_withdrawn = total_withdrawn + ? WHERE user_id = ?",
                (amount, amount, user_id)
            )

        await db.execute(
            "INSERT INTO transactions (user_id, type, amount, description) VALUES (?, ?, ?, ?)",
            (user_id, transaction_type, amount, description)
        )
        await db.commit()


async def get_transactions(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_all_transactions(limit: int = 100) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT t.*, u.username, u.first_name FROM transactions t JOIN users u ON t.user_id = u.user_id ORDER BY t.created_at DESC LIMIT ?",
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_cards_prices() -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM cards_prices ORDER BY card_amount") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def add_card_price(card_amount: int, price_usd: float):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO cards_prices (card_amount, price_usd) VALUES (?, ?)",
            (card_amount, price_usd)
        )
        await db.commit()


async def delete_card_price(card_amount: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM cards_prices WHERE card_amount = ?", (card_amount,))
        await db.commit()


async def get_card_price(card_amount: int) -> Optional[float]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT price_usd FROM cards_prices WHERE card_amount = ?", (card_amount,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def create_pending_charge(user_id: int, card_number: str, card_amount: int, price_usd: float) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO card_charges (user_id, card_number, card_amount, price_usd, status) VALUES (?, ?, ?, ?, 'pending')",
            (user_id, card_number, card_amount, price_usd)
        )
        await db.commit()
        return cursor.lastrowid


async def confirm_charge(charge_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE card_charges SET status = 'completed' WHERE id = ?", (charge_id,)
        )
        await db.commit()


async def cancel_charge(charge_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE card_charges SET status = 'cancelled' WHERE id = ?", (charge_id,)
        )
        await db.commit()


async def get_pending_charge(charge_id: int) -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM card_charges WHERE id = ? AND status = 'pending'", (charge_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_all_users() -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_stats() -> Dict[str, Any]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT COUNT(*) as count FROM users") as cursor:
            users_count = (await cursor.fetchone())[0]

        async with db.execute("SELECT SUM(balance) as total FROM balances") as cursor:
            total_balance = (await cursor.fetchone())[0] or 0

        async with db.execute("SELECT SUM(amount) as total FROM transactions WHERE type = 'charge'") as cursor:
            total_sales = (await cursor.fetchone())[0] or 0

        async with db.execute("SELECT SUM(amount) as total FROM transactions WHERE type = 'withdraw'") as cursor:
            total_withdrawals = (await cursor.fetchone())[0] or 0

        return {
            "users_count": users_count,
            "total_balance": total_balance,
            "total_sales": total_sales,
            "total_withdrawals": total_withdrawals
        }


async def is_admin(user_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM admins WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchone() is not None


async def add_admin(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (user_id,))
        await db.commit()


async def remove_admin(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
        await db.commit()


async def is_banned(user_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM banned_users WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchone() is not None


async def ban_user(user_id: int, reason: str = ""):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO banned_users (user_id, reason) VALUES (?, ?)",
            (user_id, reason)
        )
        await db.commit()


async def unban_user(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
        await db.commit()


async def update_user_language(user_id: int, language: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?", (language, user_id)
        )
        await db.commit()
