from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

TOKEN = os.getenv("7485332977:AAEK79wCat0v0_6zim08bH6gV9wpy54ZIc0")
ADMIN_ID = int(os.getenv("6689677013"))

kino_baza = {}

def start(update, context):
    update.message.reply_text("🎬 Salom! Kino nomini yuboring.")

def qidir(update, context):
    text = update.message.text.lower()
    javob = kino_baza.get(text, "❌ Bunday kino topilmadi.")
    update.message.reply_text(javob)

def add(update, context):
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("⛔ Siz admin emassiz.")
        return
    try:
        matn = update.message.text.replace("/add ", "")
        nom, link = matn.split("=")
        kino_baza[nom.strip().lower()] = link.strip()
        update.message.reply_text("✅ Qo‘shildi.")
    except:
        update.message.reply_text("❗ Format: /add kino=link")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("add", add))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, qidir))

updater.start_polling()
updater.idle()
