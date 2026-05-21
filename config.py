import os

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
MONGO_URI = os.environ.get('MONGO_URI', '')
APP_ID = int(os.environ.get('APP_ID', '27570787'))
API_HASH = os.environ.get('API_HASH', '')
START_PIC = os.environ.get('START_PIC', '')
FORCE_SUB_CHANNEL = int(os.environ.get('FORCE_SUB_CHANNEL', '-1002432405855'))

START_MSG = (
    '🎬 <b>Video Cover/Thumbnail Bot</b>\n\n'
    'Add a custom cover/thumbnail to your videos instantly!\n\n'
    '📸 <b>How to use:</b>\n'
    '• Send a photo — it will be saved as your thumbnail\n'
    '• Send any video — thumbnail will be added automatically\n\n'
    '🛠 <b>Commands:</b>\n'
    '• /mythumb — See your saved thumbnail\n'
    '• /delthumb — Remove your thumbnail\n'
    '• /help — Get help guide\n\n'
    '⚡ <b>Powered by:</b> @World_Fastest_Bots'
)

HELP_MSG = (
    '🎬 <b>Video Thumbnail Bot - Help</b>\n\n'
    '1. Send a photo → saved as thumbnail\n'
    '2. Send a video → thumbnail added automatically\n\n'
    '🛠 <b>Commands:</b>\n'
    '• /start — Start the bot\n'
    '• /mythumb — See your thumbnail\n'
    '• /delthumb — Remove thumbnail\n'
    '• /help — Show this guide\n\n'
    '⚡ <b>Powered by:</b> @World_Fastest_Bots'
)

FORCE_SUB_MSG = (
    '🔒 <b>Join Required</b>\n\n'
    'Please join our channel first:\n'
    '⚡ <b>@World_Fastest_Bots</b>\n\n'
    'Join and try again.'
)
