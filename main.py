import asyncio
import logging
import os
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, executor
from aiogram.utils.executor import start_polling
from dotenv import load_dotenv

from config.settings import (
    BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH,
    WEBAPP_HOST, WEBAPP_PORT
)
from app.database import init_db
from handlers.user_handlers import router as user_router
from handlers.admin_handlers import router as admin_router
from middlewares.middleware import setup_middlewares

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

Path("data").mkdir(exist_ok=True)


async def on_startup(dp):
    logger.info("Starting bot...")

    await init_db()
    logger.info("Database initialized")

    dp.include_router(user_router)
    dp.include_router(admin_router)

    setup_middlewares(dp)

    webhook_host = os.getenv("WEBHOOK_HOST", "")

    if webhook_host:
        await dp.bot.set_webhook(f"{webhook_host}{WEBHOOK_PATH}")
        logger.info(f"Webhook set to {webhook_host}{WEBHOOK_PATH}")
    else:
        logger.info("Running in polling mode")

    logger.info("Bot started successfully!")


async def on_shutdown(dp):
    logger.info("Shutting down bot...")
    await dp.storage.close()
    await dp.wait_closed()


def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="Markdown")
    dp = Dispatcher(bot=bot)

    webhook_host = os.getenv("WEBHOOK_HOST", "")

    if webhook_host:
        from aiogram.utils.executor import start_webhook
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        start_polling(
            dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True
        )


if __name__ == "__main__":
    main()
