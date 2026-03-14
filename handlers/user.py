import os
import asyncio
import logging
from aiogram import Router, F, types, Bot
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile, ChatJoinRequest, ChatMemberUpdated
from database import Database
from config import DATABASE_NAME, CHANNEL_ID, SUPPORT_GROUP_ID

router = Router()
db = Database(DATABASE_NAME)
logger = logging.getLogger(__name__)

# File paths (Relative to project root for compatibility)
VIDEO_PATH = "video_2026.mp4"
APK_CANDIDATE_PATHS = [
    "𝗠𝗔𝗚𝗜𝗖 𝗧𝗢𝗢𝗟 𝗣𝗥𝗢.apk",
]

# In-memory file ID cache to speed up media sending
FILE_ID_CACHE = {
    "video": None,
    "apk": None
}

def get_apk_path():
    for path in APK_CANDIDATE_PATHS:
        if os.path.exists(path):
            return path
    return APK_CANDIDATE_PATHS[0]

def get_welcome_kb():
    builder = InlineKeyboardBuilder()
    # Row 1: Play Game (Most important)
    builder.row(types.InlineKeyboardButton(
        text="🎮 PLAY GAME 🎮", 
        url="https://www.rajastake.com/#/register?invitationCode=671335540634"
    ))
    # Row 2: Tashan Official Link
    builder.row(types.InlineKeyboardButton(
        text="TASHAN OFFICIAL LINK 🚀", 
        url="https://www.rajastake.com/#/register?invitationCode=671335540634"
    ))
    # Row 3: Support Links
    builder.row(
        types.InlineKeyboardButton(text="⚡ Number Prediction", url="https://t.me/+ERspzgqr5cQ5NmRl"),
        types.InlineKeyboardButton(text="⚡ Loss recover DM ME", url="https://t.me/m/wmqbc6OcNjBh")
    )
    return builder.as_markup()


def build_leave_group_warning(user) -> str:
    username_line = f"👤 <b>Username:</b> @{user.username}\n" if getattr(user, "username", None) else ""
    return (
        "🚨 <b>USER LEFT CHANNEL</b> 🚨\n\n"
        f"👤 <b>User:</b> {user.full_name}\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
        f"{username_line}"
        "━━━━━━━━━━━━━━━━━\n"
        "⚠️ <b>Isne channel leave kar diya hai!</b>"
    )


def build_leave_user_warning() -> str:
    return (
        "⚠️ <b>Important Notice!</b>\n\n"
        "Aapne hamara official channel leave kar diya hai. \n"
        "Bot ke saare features aur support active rakhne ke liye channel join rakhein! ✅\n\n"
        "🔗 <b>Join Again:</b> https://t.me/+z-VeYV2I6MoxNDhl"
    )

async def send_welcome_dm(user_id: int, bot: Bot, full_name: str):
    """Function to send the full welcome package (APK only, no video) sequentially for better reliability"""
    welcome_caption = (
        f"<b>👋 Welcome Brother, {full_name}!</b>\n"
        "━━━━━━━━━━━━━━━━━\n"
        "🚀 <b>PREMIUM HACK UPDATE</b> 🔥\n"
        "🆕 <b>LATEST VERSION RELEASED</b> ✅\n"
        "━━━━━━━━━━━━━━━━━\n"
        "👀 <b>PROOF DEKH LO SAB LOG</b> 😱🔥\n"
        "💯 <b>REAL + WORKING PROOF</b> ✅\n"
        "━━━━━━━━━━━━━━━━━\n"
        "⤵️ <b>QUICK ACTIONS BELOW</b> 👇"
    )

    apk_caption = (
        "<b>📥 CLICK AND INSTALL NOW</b>\n"
        "━━━━━━━━━━━━━━━━━\n"
        "⚠️ <b>IMPORTANT:</b> Pahle Video Dekho Uske Baad Use Karo!\n"
        "✅ <b>100% ACCURATE NUMBER SHOTS</b>\n"
        "💎 <b>VIP PANEL ACTIVATED</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "▶️ <b>START WINNING NOW</b> ▶️"
    )
    
    # 1. Send Welcome Message First
    try:
        await bot.send_message(
            chat_id=user_id, 
            text=welcome_caption, 
            reply_markup=get_welcome_kb()
        )
        logger.info(f"Welcome text message sent to {user_id}")
    except Exception as e:
        logger.error(f"Error sending welcome text to {user_id}: {e}")

    # 2. Wait a tiny bit to avoid flood limits
    await asyncio.sleep(0.5)

    # 3. Send APK Second
    try:
        apk_path = get_apk_path()
        if os.path.exists(apk_path):
            apk = FSInputFile(apk_path)
            await bot.send_document(
                chat_id=user_id, 
                document=apk, 
                caption=apk_caption
            )
            logger.info(f"APK sent to {user_id}")
        else:
            logger.error(f"APK file NOT FOUND at: {os.path.abspath(apk_path)}")
    except Exception as e:
        logger.error(f"Error sending APK to {user_id}: {e}")

@router.message(CommandStart())
async def cmd_start(message: types.Message, bot: Bot):
    user = message.from_user
    await db.add_user(user.id, user.username, user.full_name)
    await send_welcome_dm(user.id, bot, user.full_name)

# Auto Welcome when user joins a channel via Join Request
@router.chat_join_request()
async def auto_welcome_join_request(request: ChatJoinRequest, bot: Bot):
    if request.chat.id != CHANNEL_ID:
        return

    user = request.from_user
    await db.add_user(user.id, user.username, user.full_name)

    try:
        await bot.approve_chat_join_request(chat_id=request.chat.id, user_id=user.id)
    except Exception as e:
        logger.error(f"Failed to approve join request for user {user.id}: {e}")

    try:
        await send_welcome_dm(user.id, bot, user.full_name)
    except Exception as e:
        logger.error(f"Failed to send welcome DM after join request for user {user.id}: {e}")

# Monitor users leaving the channel
@router.chat_member()
async def on_chat_member_update(update: ChatMemberUpdated, bot: Bot):
    """Detect when a user leaves the channel and send warnings"""
    if update.chat.id != CHANNEL_ID:
        return

    # User statuses that mean they are NO LONGER a member
    leaving_statuses = ["left", "kicked"]
    # User statuses that mean they WERE a member
    member_statuses = ["member", "administrator", "creator"]

    if update.old_chat_member.status in member_statuses and \
       update.new_chat_member.status in leaving_statuses:
        
        user = update.new_chat_member.user
        await db.update_user_status(user.id, 0)
        group_warning = build_leave_group_warning(user)
        user_warning = build_leave_user_warning()
        
        try:
            await bot.send_message(SUPPORT_GROUP_ID, group_warning)
        except Exception as e:
            logger.error(f"Failed to send leave warning to group for user {user.id}: {e}")

        try:
            await bot.send_message(user.id, user_warning)
        except Exception as e:
            logger.error(f"Failed to send leave warning to user {user.id}: {e}")

@router.message(Command("support"))
async def cmd_support(message: types.Message):
    await message.answer("💬 To contact support, just send your message here in this chat. Our team will reply to you as soon as possible.")

@router.callback_query(F.data == "number_prediction")
async def number_prediction(callback: types.CallbackQuery):
    await callback.answer("Predicting numbers...")

@router.callback_query(F.data == "loss_recover")
async def loss_recover(callback: types.CallbackQuery):
    await callback.answer("Recovering loss...")
