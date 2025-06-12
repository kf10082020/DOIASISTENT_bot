
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from parsers.doi_handler import handle_doi
from utils.formatter import format_reply

load_dotenv()
TOKEN = os.getenv("DOIASISTENT_bot")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь DOI-ссылку для получения информации.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doi_url = update.message.text.strip()
    metadata = handle_doi(doi_url)
    reply = format_reply(metadata)
    await update.message.reply_text(reply, parse_mode="Markdown")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
