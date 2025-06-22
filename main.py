
from telegram.ext import Updater, CommandHandler

TOKEN = "7485332977:AAEK79wCat0v0_6zim08bH6gV9wpy54ZIc0"

def start(update, context):
    update.message.reply_text("🎬 Iltimos, kino nomi yoki kodini yuboring.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
