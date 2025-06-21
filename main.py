from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackContext
import uuid

# Token va admin ID
TOKEN = "7485332977:AAEK79wCat0v0_6zim08bH6gV9wpy54ZIc0"
ADMIN_ID = 6689677013

# Baza
kino_baza = {}  # {'kino nomi': 'link'}
foydalanuvchilar = set()

# /start
def start(update: Update, context: CallbackContext):
    foydalanuvchilar.add(update.message.chat_id)
    update.message.reply_text("🎬 Salom! Kino nomini yuboring yoki @KINO_QIDIRUV_UZB_BOT orqali izlang.")

# Kino qo‘shish
def add(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        return update.message.reply_text("⛔ Siz admin emassiz.")
    try:
        matn = update.message.text.replace("/add ", "")
        nom, link = matn.split("=")
        kino_baza[nom.strip().lower()] = link.strip()
        update.message.reply_text(f"✅ Kino qo‘shildi: {nom.strip()}")
    except:
        update.message.reply_text("❗ Format noto‘g‘ri. Misol: /add Avatar=https://link")

# Kino qidirish
def qidir(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    javob = kino_baza.get(text)
    if javob:
        update.message.reply_text(f"🎬 {text.title()}\n▶️ {javob}")
    else:
        update.message.reply_text("❌ Bunday kino topilmadi.")

# Kino ro‘yxati
def list_kino(update: Update, context: CallbackContext):
    if kino_baza:
        javob = "\n".join([f"🎬 {k}" for k in kino_baza.keys()])
        update.message.reply_text(f"📃 Barcha kinolar:\n{javob}")
    else:
        update.message.reply_text("📭 Kino bazasi bo‘sh.")

# Admin panel
def panel(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        return update.message.reply_text("⛔ Siz admin emassiz.")
    kinolar_soni = len(kino_baza)
    user_soni = len(foydalanuvchilar)
    update.message.reply_text(f"📊 Statistika:\n👥 Foydalanuvchilar: {user_soni}\n🎞 Kinolar: {kinolar_soni}")

# Inline query
def inlinequery(update: Update, context: CallbackContext):
    query = update.inline_query.query.lower()
    results = []
    for nom, link in kino_baza.items():
        if query in nom:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=nom.title(),
                    input_message_content=InputTextMessageContent(f"🎬 {nom.title()}\n▶️ {link}")
                )
            )
    update.inline_query.answer(results)

# Yozuvlar
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# Komandalar
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("add", add))
dp.add_handler(CommandHandler("panel", panel))
dp.add_handler(CommandHandler("list", list_kino))

# Xabarlar
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, qidir))
dp.add_handler(InlineQueryHandler(inlinequery))

updater.start_polling()
updater.idle()
