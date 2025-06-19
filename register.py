
from aiogram import Router, types
router = Router()

@router.message()
async def register_user(message: types.Message):
    # Bu yerda userni bazaga qo‘shish mumkin
    pass
