from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from config import START_MSG, START_PIC
from database.db import ensure_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await ensure_user(user_id)
    if START_PIC:
        try:
            await update.message.reply_photo(photo=START_PIC, caption=START_MSG, parse_mode='HTML')
            return
        except Exception:
            pass
    await update.message.reply_text(START_MSG, parse_mode='HTML')


def register(app):
    app.add_handler(CommandHandler('start', start))
