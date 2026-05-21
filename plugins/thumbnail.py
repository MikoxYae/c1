import io
import logging
from PIL import Image
from telegram import Update, MessageEntity
from telegram.error import TelegramError
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import FORCE_SUB_CHANNEL, FORCE_SUB_MSG
from database import db

logger = logging.getLogger(__name__)


async def is_user_joined(user_id: int, context) -> bool:
    try:
        member = await context.bot.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator', 'restricted']
    except Exception as e:
        logger.error(f'Force sub check failed (allowing user): {e}')
        return True


async def prepare_thumbnail(file_id: str, context) -> io.BytesIO:
    """Download photo and resize to <=320x320 JPEG for use as video thumbnail."""
    tg_file = await context.bot.get_file(file_id)
    buf = io.BytesIO()
    await tg_file.download_to_memory(buf)
    buf.seek(0)
    img = Image.open(buf).convert('RGB')
    img.thumbnail((320, 320), Image.LANCZOS)
    out = io.BytesIO()
    img.save(out, format='JPEG', quality=85)
    out.seek(0)
    out.name = 'thumbnail.jpg'
    return out


async def my_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thumbnail = await db.get_thumbnail(update.message.from_user.id)
    if thumbnail:
        try:
            await update.message.reply_photo(
                photo=thumbnail,
                caption='🖼️ <b>Your Current Thumbnail</b>\n\nUse /delthumb to remove it.',
                parse_mode='HTML'
            )
        except Exception:
            await update.message.reply_text('❌ Cannot load thumbnail. Please set a new one.')
    else:
        await update.message.reply_text('❌ No thumbnail saved. Send a photo to set one.')


async def delete_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if await db.get_thumbnail(user_id):
        await db.delete_thumbnail(user_id)
        await update.message.reply_text('✅ Thumbnail removed!')
    else:
        await update.message.reply_text('❌ No thumbnail to delete.')


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not await is_user_joined(user_id, context):
        await update.message.reply_text(FORCE_SUB_MSG, parse_mode='HTML')
        return
    photos = update.message.photo
    largest = max(photos, key=lambda p: p.file_size)
    state = await db.get_state(user_id)
    if state == 'waiting_for_image':
        user = await db.get_user(user_id)
        try:
            entities = [
                MessageEntity(type=e['type'], offset=e['offset'], length=e['length'], user=e.get('user'))
                for e in (user.get('caption_entities') or [])
            ] or None
            thumb_buf = await prepare_thumbnail(largest.file_id, context)
            await context.bot.send_video(
                chat_id=update.message.chat_id,
                video=user['video_file_id'],
                thumbnail=thumb_buf,
                caption=user['video_caption'],
                caption_entities=entities,
                supports_streaming=True,
                has_spoiler=user.get('has_spoiler', False),
                reply_to_message_id=update.message.message_id - 1
            )
            await db.reset_state(user_id, keep_thumbnail=largest.file_id)
        except TelegramError as e:
            logger.error(f'send_video error: {e}')
            await update.message.reply_text(f'❌ Error: {e}')
    else:
        await db.set_thumbnail(user_id, largest.file_id)
        await db.set_state(user_id, 'idle')
        await update.message.reply_text('✅ Thumbnail saved! Now send me a video.')


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not await is_user_joined(user_id, context):
        await update.message.reply_text(FORCE_SUB_MSG, parse_mode='HTML')
        return
    video = update.message.video
    if not video:
        return await update.message.reply_text('❌ Send a valid video.')
    saved = await db.get_thumbnail(user_id)
    if saved:
        try:
            thumb_buf = await prepare_thumbnail(saved, context)
            await context.bot.send_video(
                chat_id=update.message.chat_id,
                video=video.file_id,
                thumbnail=thumb_buf,
                caption=update.message.caption,
                caption_entities=update.message.caption_entities,
                supports_streaming=True,
                reply_to_message_id=update.message.message_id
            )
            return
        except TelegramError as e:
            logger.error(f'send_video error: {e}')
            await update.message.reply_text('❌ Error applying thumbnail. Send a fresh photo.')
            await db.delete_thumbnail(user_id)
            return
    entities = [
        {'offset': e.offset, 'length': e.length, 'type': e.type,
         'user': e.user.to_dict() if e.type == 'text_mention' else None}
        for e in (update.message.caption_entities or [])
    ]
    await db.set_waiting_video(user_id, video.file_id, update.message.caption, entities)
    await update.message.reply_text('✅ Video received! Now send a photo for the cover.')


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'check_join':
        if await is_user_joined(query.from_user.id, context):
            await query.edit_message_text(
                '✅ <b>Welcome!</b>\n\nSend a photo to set thumbnail, then send a video!\n\n'
                '⚡ <b>Powered by:</b> @World_Fastest_Bots',
                parse_mode='HTML'
            )
        else:
            await query.answer('Please join the channel first!', show_alert=True)


def register(app):
    app.add_handler(CommandHandler('mythumb', my_thumbnail))
    app.add_handler(CommandHandler('delthumb', delete_thumbnail))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
