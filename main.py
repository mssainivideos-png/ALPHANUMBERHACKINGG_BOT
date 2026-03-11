import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN, DATABASE_NAME
from database import Database
from handlers import user, admin, support

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Bot is starting...")
    
    # Initialize Database
    db = Database(DATABASE_NAME)
    await db.create_tables()
    logger.info("Database initialized.")

    # Initialize Bot and Dispatcher with optimized properties
    bot = Bot(
        token=BOT_TOKEN, 
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True # Disabling link previews speeds up message sending
        )
    )
    dp = Dispatcher()

    # Register Routers
    dp.include_router(user.router)
    dp.include_router(admin.router)
    dp.include_router(support.router)
    
    logger.info("Routers registered.")

    # Drop updates and delete webhook
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Pending updates dropped. Starting polling...")
    
    try:
        # We explicitly tell dispatcher to resolve all used update types (including chat_member)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Error during polling: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
