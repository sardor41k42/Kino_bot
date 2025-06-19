
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(commands=["admin"])
async def contact_admin(message: types.Message):
    btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Admin bilan bog‘lanish", url="https://t.me/Usernem_bor")]
    ])
    await message.answer("Admin bilan bog‘lanish uchun tugmani bosing:", reply_markup=btn)
