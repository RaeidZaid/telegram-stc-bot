from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

from app.database import is_banned, get_user, create_user


class BanMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        user_id = message.from_user.id

        if await is_banned(user_id):
            await message.answer("🚫 عذراً، حسابك محظور.")
            raise CancelHandler()

    async def on_pre_process_callback_query(self, call: CallbackQuery, data: dict):
        user_id = call.from_user.id

        if await is_banned(user_id):
            await call.answer("🚫 حسابك محظور.", show_alert=True)
            raise CancelHandler()


class UserMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        user_id = message.from_user.id
        username = message.from_user.username or ""
        first_name = message.from_user.first_name or "User"

        user = await get_user(user_id)
        if not user:
            await create_user(user_id, username, first_name)

    async def on_pre_process_callback_query(self, call: CallbackQuery, data: dict):
        user_id = call.from_user.id
        username = call.from_user.username or ""
        first_name = call.from_user.first_name or "User"

        user = await get_user(user_id)
        if not user:
            await create_user(user_id, username, first_name)


def setup_middlewares(dp: Dispatcher):
    dp.middleware.setup(UserMiddleware())
    dp.middleware.setup(BanMiddleware())
