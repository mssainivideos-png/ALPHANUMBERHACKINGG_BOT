# Tashan-PanelBot 🚀

Advanced Telegram Bot with Auto Join Request Accept, Welcome DM System, and professional Support features.

## ✨ Features
- 🎥 **Auto-Playing Welcome Video**: Sends a high-quality video with professional formatting.
- 📦 **Automatic APK Delivery**: Sends the VIP Panel APK immediately after the welcome video.
- 🤝 **Auto Join Request Handler**: Automatically sends welcome DMs when users request to join the channel.
- 💬 **Live Chat Support System**: Forward user messages to a support group and reply anonymously.
- 🚨 **Channel Leave Monitoring**: Get instant alerts in the support group and send warnings to users when they leave.
- 🛠️ **Professional Formatting**: Bold text, dividers, and attractive emojis for a premium look.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/surendrasaini8024-sys/Tashan-PanelBot.git
   cd Tashan-PanelBot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your `.env` file:
   ```env
   BOT_TOKEN=your_token_here
   ADMIN_ID=your_id_here
   DATABASE_NAME=bot_database.db
   ```

### Running the Bot
- **Windows**: Just double-click `run_bot.bat`
- **Linux/VPS**: 
  ```bash
  python3 main.py
  ```
- **Railway**: 
  1. Connect your GitHub repository to Railway.
  2. Add your Environment Variables (`BOT_TOKEN`, `ADMIN_ID`, etc.) in the Railway dashboard.
  3. Railway will automatically detect the `Procfile` and start the bot.

## 🛠️ Configuration
Update `config.py` with your specific IDs:
- `SUPPORT_GROUP_ID`: Your private support group ID.
- `CHANNEL_ID`: The channel you want to monitor.

## 📝 License
This project is for educational purposes only. Use at your own risk.
