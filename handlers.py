from telegram import Update
from telegram.ext import ContextTypes
from voice_utils import voice_to_text
from wiki import search_wikipedia

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to WikiGenieBot!\nUse /help to see all features."
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Available Commands:\n"
        "/search <query> – Search Wikipedia\n"
        "/random – Get a random article\n"
        "/today – On this day in history\n"
        "/lang <code> – Change language\n"
        "/voice – Send voice to search"
    )

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    file_path = await file.download_to_drive()
    query = voice_to_text(file_path)
    if query:
        result = search_wikipedia(query)
        await update.message.reply_text(f"🎙️ Voice input: {query}\n\n{result}")
    else:
        await update.message.reply_text("❌ Sorry, couldn't understand voice.")