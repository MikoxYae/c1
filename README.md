# Miko Bot — Video Thumbnail Bot

  Telegram bot that adds custom thumbnails to videos automatically.

  ## Structure
  ```
  miko.py           ← Main entry (python3 miko.py)
  config.py         ← Settings & messages
  database/db.py    ← MongoDB async (motor)
  plugins/
    start.py        ← /start
    help.py         ← /help
    thumbnail.py    ← photo, video, /mythumb, /delthumb
  ```

  ## Setup
  ```bash
  pip install -r requirements.txt
  ```

  **Environment variables:**
  | Variable | Description |
  |---|---|
  | BOT_TOKEN | Telegram bot token |
  | MONGO_URI | MongoDB connection string |
  | APP_ID | Telegram App ID |
  | API_HASH | Telegram API Hash |
  | START_PIC | Start photo URL (optional) |
  | FORCE_SUB_CHANNEL | Channel ID for force sub |

  ## Run
  ```bash
  python3 miko.py
  ```

  Powered by @World_Fastest_Bots
  