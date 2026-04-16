import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.webhook import WebhookRunner, WebhookRequestHandler
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

from config.settings import (
    BOT_TOKEN, ADMIN_IDS, WEBHOOK_HOST, WEBHOOK_PATH,
    WEBAPP_HOST, WEBAPP_PORT, DATABASE_URL
)
from app.database import init_db
from handlers.user_handlers import dp as user_dp, router as user_router
from handlers.admin_handlers import router as admin_router
from middlewares.middleware import setup_middlewares

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")
dp = Dispatcher()


async def on_startup(dp):
    logger.info("Starting bot...")

    Path("data").mkdir(exist_ok=True)

    await init_db()
    logger.info("Database initialized")

    dp.include_router(user_router)
    dp.include_router(admin_router)

    setup_middlewares(dp)

    if WEBHOOK_HOST:
        await bot.set_webhook(WEBHOOK_HOST + WEBHOOK_PATH)
        logger.info(f"Webhook set to {WEBHOOK_HOST + WEBHOOK_PATH}")
    else:
        logger.info("Running in polling mode")

    logger.info("Bot started successfully!")


async def on_shutdown(dp):
    logger.info("Shutting down bot...")
    await dp.storage.close()
    await dp.wait_closed()


def main():
    if WEBHOOK_HOST:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(
            dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True
        )


if __name__ == "__main__":
    main()
