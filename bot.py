import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from wikimedia import search_wikipedia, get_random_article, get_today_on_history, set_language
from voice_utils import transcribe_voice

BOT_TOKEN = os.getenv("BOT_TOKEN", "your-bot-token-here")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to WikiGenie Bot!
Use /help to see available commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🤖 *WikiGenie Commands*:
/search <query> - Search Wikipedia
/random - Random article
/today - On this day in history
/lang <code> - Change language (e.g. en, hi)
/voice - Send voice message to search
    """)

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("❗ Usage: /search <query>")
        return
    result = search_wikipedia(query)
    await update.message.reply_text(result, disable_web_page_preview=True)

async def random_article(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_random_article()
    await update.message.reply_text(result, disable_web_page_preview=True)

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_today_on_history()
    await update.message.reply_text(result)

async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = " ".join(context.args)
    if not code:
        await update.message.reply_text("❗ Usage: /lang <code> (e.g. en, hi, es)")
        return
    success = set_language(code)
    if success:
        await update.message.reply_text(f"✅ Language changed to {code}")
    else:
        await update.message.reply_text("❌ Invalid language code.")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.voice:
        await update.message.reply_text("Please send a voice message.")
        return
    file = await update.message.voice.get_file()
    path = await file.download_to_drive()
    text = transcribe_voice(path)
    if text:
        result = search_wikipedia(text)
        await update.message.reply_text(f"🎤 You said: *{text}*

{result}", parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await update.message.reply_text("❌ Could not understand voice.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("random", random_article))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("lang", lang))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))
    app.run_polling()

if __name__ == "__main__":
    main()