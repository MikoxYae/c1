import motor.motor_asyncio
from config import MONGO_URI

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client['thumbnail_bot']
users_col = db['users']


async def ensure_user(user_id: int):
    key = str(user_id)
    if not await users_col.find_one({'_id': key}):
        await users_col.insert_one({
            '_id': key, 'thumbnail': None, 'state': 'idle',
            'video_file_id': None, 'video_caption': None,
            'caption_entities': None, 'image_file_id': None, 'has_spoiler': False
        })
    return key


async def get_user(user_id: int) -> dict:
    key = str(user_id)
    user = await users_col.find_one({'_id': key})
    if not user:
        await ensure_user(user_id)
        user = await users_col.find_one({'_id': key})
    return user


async def update_user(user_id: int, data: dict):
    await users_col.update_one({'_id': str(user_id)}, {'$set': data}, upsert=True)


async def get_thumbnail(user_id: int):
    return (await get_user(user_id)).get('thumbnail')


async def set_thumbnail(user_id: int, file_id: str):
    await update_user(user_id, {'thumbnail': file_id})


async def delete_thumbnail(user_id: int):
    await update_user(user_id, {'thumbnail': None})


async def get_state(user_id: int) -> str:
    return (await get_user(user_id)).get('state', 'idle')


async def set_state(user_id: int, state: str):
    await update_user(user_id, {'state': state})


async def set_waiting_video(user_id: int, video_file_id, caption, caption_entities, has_spoiler=False):
    await update_user(user_id, {
        'state': 'waiting_for_image', 'video_file_id': video_file_id,
        'video_caption': caption, 'caption_entities': caption_entities,
        'image_file_id': None, 'has_spoiler': has_spoiler
    })


async def reset_state(user_id: int, keep_thumbnail: str = None):
    data = {
        'state': 'idle', 'video_file_id': None, 'video_caption': None,
        'caption_entities': None, 'image_file_id': None, 'has_spoiler': False
    }
    if keep_thumbnail:
        data['thumbnail'] = keep_thumbnail
    await update_user(user_id, data)


async def total_users() -> int:
    return await users_col.count_documents({})
