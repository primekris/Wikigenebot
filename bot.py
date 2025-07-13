from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from wiki import search_wikipedia, random_article, today_on_history, set_language, current_lang
from handlers import start_handler, help_handler, voice_handler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"  # Replace this later

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: /search <query>")
        return
    query = " ".join(context.args)
    result = search_wikipedia(query)
    await update.message.reply_text(result, disable_web_page_preview=True)

async def random_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random_article())

async def today_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(today_on_history())

async def lang_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        lang = context.args[0]
        set_language(lang)
        await update.message.reply_text(f"🌐 Language set to: {lang.upper()}")
    else:
        await update.message.reply_text(f"🌐 Current language: {current_lang.upper()}\nUse /lang <code> to change (e.g., /lang hi)")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start_handler))
app.add_handler(CommandHandler("help", help_handler))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("random", random_cmd))
app.add_handler(CommandHandler("today", today_cmd))
app.add_handler(CommandHandler("lang", lang_cmd))
app.add_handler(CommandHandler("voice", voice_handler))
app.add_handler(MessageHandler(filters.VOICE, voice_handler))

if __name__ == "__main__":
    print("Bot started...")
    app.run_polling()