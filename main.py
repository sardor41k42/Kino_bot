from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackContext
import uuid

TOKEN = "7485332977:AAEK79wCat0v0_6zim08bH6gV9wpy54ZIc0"
ADMIN_ID = 6689677013

# kino_baza = {"kalit": {"nom": "...", "link": "..."}}
kino_baza = {}
foydalanuvchilar = set()

def start(update: Update, context: CallbackContext):
    foydalanuvchilar.add(update.message.chat_id)
    update.message.reply_text("🎬 Kino nomi yoki kodi yuboring.")

def add(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        return update.message.reply_text("⛔ Siz admin emassiz.")
    try:
        matn = update.message.text.replace("/add ", "")
        nom, qolgani = matn.split("=")
        if "|" in qolgani:
            link, kod = qolgani.split("|")
            kalitlar = [nom.strip().lower(), kod.strip().upper()]
        else:
            link = qolgani
            kalitlar = [nom.strip().lower()]
        for kalit in kalitlar:
            kino_baza[kalit] = {"nom": nom.strip(), "link": link.strip()}
        update.message.reply_text(f"✅ Qo‘shildi: {nom.strip()}")
    except:
        update.message.reply_text("❗ Format: /add Avatar=https://link | AVT123")

def qidir(update: Update, context: CallbackContext):
    text = update.message.text.strip().lower()
    kino = kino_baza.get(text)
    if kino:
        update.message.reply_text(f"🎬 {kino['nom']}\n▶️ {kino['link']}")
    else:
        update.message.reply_text("❌ Topilmadi. Kino nomi yoki kodini tekshiring.")

def list_kino(update: Update, context: CallbackContext):
    if kino_baza:
        nomlar = set(k["nom"] for k in kino_baza.values())
        ro‘yxat = "\n".join([f"🎬 {n}" for n in nomlar])
        update.message.reply_text(f"📃 Barcha kinolar:\n{ro‘yxat}")
    else:
        update.message.reply_text("📭 Kino bazasi bo‘sh.")

def panel(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        return update.message.reply_text("⛔ Siz admin emassiz.")
    update.message.reply_text(f"📊 Statistika:\n👥 Foydalanuvchi: {len(foydalanuvchilar)}\n🎞 Kinolar: {len(set(k['nom'] for k in kino_baza.values()))}")

def inlinequery(update: Update, context: CallbackContext):
    query = update.inline_query.query.strip().lower()
    results = []
    for kalit, data in kino_baza.items():
        if query in kalit:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=data["nom"],
                    input_message_content=InputTextMessageContent(f"🎬 {data['nom']}\n▶️ {data['link']}")
                )
            )
    update.inline_query.answer(results)

# Registratsiya
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("add", add))
dp.add_handler(CommandHandler("panel", panel))
dp.add_handler(CommandHandler("list", list_kino))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, qidir))
dp.add_handler(InlineQueryHandler(inlinequery))

updater.start_polling()
updater.idle()
