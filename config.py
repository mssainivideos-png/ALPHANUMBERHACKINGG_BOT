import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
admin_id_str = os.getenv("ADMIN_ID", "0")
if admin_id_str.isdigit():
    ADMIN_ID = int(admin_id_str)
else:
    ADMIN_ID = 0

DATABASE_NAME = os.getenv("DATABASE_NAME", "bot_database.db")

# Support Group ID
SUPPORT_GROUP_ID = int(os.getenv("SUPPORT_GROUP_ID", "-1003557182463")) # Updated from .env or default

# Channel ID to monitor (FUTURE MILLIONAIRE)
CHANNEL_ID = -1003538093819 # Fixed channel ID from user

# Admin IDs list for flexibility
ADMINS = [ADMIN_ID]
