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
    
    # Set Bot Menu Button (Play Game)
    try:
        from aiogram.types import MenuButtonWebApp, WebAppInfo
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="Play Game",
                web_app=WebAppInfo(url="https://www.rajastake.com/#/register?invitationCode=671335540634")
            )
        )
        logger.info("Menu button 'Play Game' set successfully.")
    except Exception as e:
        logger.error(f"Failed to set menu button: {e}")
    
    logger.info("Routers registered.")

    # Forcefully break any existing polling connection
    logger.info("Breaking existing polling connections...")
    await bot.set_webhook(url="https://google.com") # Dummy webhook
    await asyncio.sleep(2)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Polling connections broken. Starting clean session...")
    
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
