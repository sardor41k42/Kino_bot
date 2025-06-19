import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import start, register, search, forward_new_post, inline, contact_admin

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(register.router)
    dp.include_router(search.router)
    dp.include_router(forward_new_post.router)
    dp.include_router(inline.router)
    dp.include_router(contact_admin.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
