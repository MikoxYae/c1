import logging
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from telegram.ext import Application
from config import BOT_TOKEN

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_errors.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_plugins(app):
    from plugins import start, help, thumbnail
    start.register(app)
    help.register(app)
    thumbnail.register(app)
    print('✅ All plugins loaded.')


def main():
    if not BOT_TOKEN:
        print('❌ BOT_TOKEN is not set!')
        sys.exit(1)
    print('🚀 Starting Miko Bot...')
    app = Application.builder().token(BOT_TOKEN).build()
    load_plugins(app)
    print('🎬 Bot is running...')
    app.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()
