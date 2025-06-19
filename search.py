
from aiogram import Router, types
router = Router()

@router.message(lambda msg: msg.text and not msg.text.startswith('/'))
async def search_movie(message: types.Message):
    await message.answer(f"🔍 Qidiruv: '{message.text}' — natija topilmadi.")
