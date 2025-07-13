import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from wikimedia import search_wikipedia, random_article, today_in_history
from voice_utils import transcribe_voice

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Default language
USER_LANGUAGES = {}

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *WikiGenie Bot!*\n\n"
        "Type `/search <topic>` to get started or try one of these:\n"
        "`/random` — Random Wikipedia article\n"
        "`/today` — Events from today in history\n"
        "`/lang` — Change your language\n"
        "`/voice` — Try voice search (English only)\n\n"
        "_Powered by Wikimedia API._",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 *Help Menu*\n\n"
        "`/search <query>` — Search Wikipedia\n"
        "`/random` — Get a random article\n"
        "`/today` — See today's events\n"
        "`/lang` — Change content language\n"
        "`/voice` — Voice message to Wikipedia search\n"
        "`/help` — Show this message",
        parse_mode="Markdown"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("❌ Please provide a search term. Example: `/search Albert Einstein`", parse_mode="Markdown")
        return

    lang = USER_LANGUAGES.get(update.effective_user.id, "en")
    result = search_wikipedia(query, lang)
    await update.message.reply_text(result, parse_mode="Markdown", disable_web_page_preview=True)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = USER_LANGUAGES.get(update.effective_user.id, "en")
    result = random_article(lang)
    await update.message.reply_text(result, parse_mode="Markdown", disable_web_page_preview=True)

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = USER_LANGUAGES.get(update.effective_user.id, "en")
    result = today_in_history(lang)
    await update.message.reply_text(result, parse_mode="Markdown", disable_web_page_preview=True)

async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English", callback_data="lang_en")],
        [InlineKeyboardButton("Hindi", callback_data="lang_hi")],
        [InlineKeyboardButton("Spanish", callback_data="lang_es")],
        [InlineKeyboardButton("French", callback_data="lang_fr")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌐 Choose a language:", reply_markup=reply_markup)

async def handle_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = query.data.split("_")[1]
    USER_LANGUAGES[query.from_user.id] = lang_code
    await query.edit_message_text(f"✅ Language set to *{lang_code.upper()}*", parse_mode="Markdown")

async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎤 Send a voice message and I'll search Wikipedia for what you say!")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = USER_LANGUAGES.get(user_id, "en")

    try:
        file = await update.message.voice.get_file()
        file_path = f"voice_{user_id}.ogg"
        await file.download_to_drive(file_path)

        text = transcribe_voice(file_path)
        if not text:
            await update.message.reply_text("❌ Could not understand your voice message.")
            return

        await update.message.reply_text(f"🎤 You said: *{text}*", parse_mode="Markdown")

        result = search_wikipedia(text, lang)
        await update.message.reply_text(result, parse_mode="Markdown", disable_web_page_preview=True)

        os.remove(file_path)
    except Exception as e:
        logger.error(f"Voice error: {e}")
        await update.message.reply_text("⚠️ Error processing voice message.")

# --- Main ---

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("random", random))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("lang", lang))
    app.add_handler(CommandHandler("voice", voice))
    app.add_handler(CallbackQueryHandler(handle_lang_callback))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    logger.info("🤖 WikiGenie Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
