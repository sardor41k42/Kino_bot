
import sqlite3
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

ADMIN_USERNAME = "Usernem_bor"
CHANNEL_USERNAME = "@KINO_QIDIRUV_UZ_BOT"

db = sqlite3.connect("kino.db")
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS kinolar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    kategoriya TEXT,
    tavsif TEXT,
    media_id TEXT,
    media_type TEXT
)
""")
db.commit()

kategoriya_list = ["🎥 Boevik", "😂 Komediya", "🌍 Tarixiy", "💘 Melodrama", "🧙‍♂️ Fantastika"]

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("🎬 Salom! Bu professional kino bot. Kino qidirish uchun /qidir [nomi yoki ID] deb yozing.")

@dp.message_handler(commands=["admin"])
async def admin(message: types.Message):
    if message.from_user.username != ADMIN_USERNAME:
        await message.answer("❌ Siz admin emassiz.")
        return
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("➕ Kino qo‘shish", callback_data="add_kino"))
    await message.answer("👋 Admin paneliga xush kelibsiz", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "add_kino")
async def kino_ask_name(callback: types.CallbackQuery):
    await callback.message.answer("🎞 Kino nomini kiriting:")
    await callback.answer()
    dp.register_message_handler(kino_ask_category, state=None)

async def kino_ask_category(message: types.Message):
    message.conf = {"nom": message.text}
    keyboard = InlineKeyboardMarkup(row_width=2)
    for cat in kategoriya_list:
        keyboard.insert(InlineKeyboardButton(cat, callback_data=f"cat_{cat}"))
    await message.answer("📂 Kategoriya tanlang:", reply_markup=keyboard)
    dp.register_message_handler(kino_ask_category, state=None)
    dp.register_message_handler(kino_ask_description, state=None)

@dp.callback_query_handler(lambda c: c.data.startswith("cat_"))
async def kino_ask_description(callback: types.CallbackQuery):
    kategoriya = callback.data.replace("cat_", "")
    callback.message.conf = {"nom": callback.message.reply_to_message.text, "kategoriya": kategoriya}
    await callback.message.answer("📝 Kino tavsifini yuboring:")
    await callback.answer()
    dp.register_message_handler(kino_ask_media, state=None)

async def kino_ask_media(message: types.Message):
    konf = message.conf if hasattr(message, 'conf') else {}
    konf["tavsif"] = message.text
    await message.answer("📤 Kino faylini yuboring (video/photo/text):")
    message.conf = konf
    dp.register_message_handler(kino_finish, content_types=types.ContentType.ANY, state=None)

async def kino_finish(message: types.Message):
    konf = message.conf
    nom = konf.get("nom")
    kategoriya = konf.get("kategoriya")
    tavsif = konf.get("tavsif")

    media_id = None
    media_type = None

    if message.video:
        media_id = message.video.file_id
        media_type = "video"
    elif message.photo:
        media_id = message.photo[-1].file_id
        media_type = "photo"
    elif message.text:
        media_id = message.text
        media_type = "text"

    cursor.execute("INSERT INTO kinolar (nom, kategoriya, tavsif, media_id, media_type) VALUES (?, ?, ?, ?, ?)",
                   (nom, kategoriya, tavsif, media_id, media_type))
    db.commit()

    # Kanalga yuborish
    caption = f"*{nom}*\nKategoriya: {kategoriya}\n{tavsif}"
    try:
        if media_type == "video":
            await bot.send_video(CHANNEL_USERNAME, media_id, caption=caption, parse_mode="Markdown")
        elif media_type == "photo":
            await bot.send_photo(CHANNEL_USERNAME, media_id, caption=caption, parse_mode="Markdown")
        else:
            await bot.send_message(CHANNEL_USERNAME, caption, parse_mode="Markdown")
        await message.answer("✅ Kino bazaga saqlandi va kanalga yuborildi.")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")

@dp.message_handler(commands=["qidir"])
async def qidir(message: types.Message):
    soz = message.get_args()
    if soz.isdigit():
        cursor.execute("SELECT * FROM kinolar WHERE id = ?", (int(soz),))
    else:
        cursor.execute("SELECT * FROM kinolar WHERE nom LIKE ?", (f"%{soz}%",))
    kino = cursor.fetchone()
    if not kino:
        await message.answer("❌ Kino topilmadi.")
        return
    caption = f"*{kino[1]}*\nKategoriya: {kino[2]}\n{kino[3]}"
    if kino[5] == "video":
        await message.answer_video(kino[4], caption=caption, parse_mode="Markdown")
    elif kino[5] == "photo":
        await message.answer_photo(kino[4], caption=caption, parse_mode="Markdown")
    else:
        await message.answer(caption, parse_mode="Markdown")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
