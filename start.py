from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging
import os

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔍 Kino qidirish", switch_inline_query_current_chat=""),
        InlineKeyboardButton("📢 Reklama haqida", callback_data="reklama"),
        InlineKeyboardButton("🔗 Admin bilan bog‘lanish", url="https://t.me/Usernem_bor")
    )
    await message.answer("Assalomu alaykum! Kino botga xush kelibsiz.
Pastdagi tugmalar orqali xizmatlardan foydalaning:", reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == "reklama")
async def reklama_haqida(call: types.CallbackQuery):
    await call.message.answer("📢 Reklama uchun murojaat: @Usernem_bor")
    await call.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
