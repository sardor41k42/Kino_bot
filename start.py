from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Assalomu alaykum! 👋")

@dp.message_handler(lambda m: m.text and m.text.lower() == "salom")
async def reply_salom(message: types.Message):
    await message.answer("Salom, yaxshimisiz? 😊")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
