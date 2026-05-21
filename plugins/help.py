from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from config import HELP_MSG


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MSG, parse_mode='HTML')


def register(app):
    app.add_handler(CommandHandler('help', help_command))
