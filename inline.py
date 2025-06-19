
from aiogram import Router, types
router = Router()

@router.inline_query()
async def inline_handler(inline_query: types.InlineQuery):
    await inline_query.answer([], switch_pm_text="Qidiruv natijasi yo‘q", cache_time=1)
