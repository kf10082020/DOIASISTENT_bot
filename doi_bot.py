import os
import logging
import re
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from doi_handler import handle_doi
from formatter import format_reply
from utils import extract_doi

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 День добрый! Отправьте DOI-ссылку, и я найду данные публикации.")

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    doi = extract_doi(text)

    if not doi:
        await update.message.reply_text("❌ DOI не найден. Пожалуйста, отправьте корректную ссылку.")
        return

    await update.message.reply_text("⌛ Обрабатываю запрос, подождите...")

    metadata = handle_doi(doi)
    reply_text, keyboard = format_reply(metadata)
    await update.message.reply_text(reply_text, parse_mode="Markdown", reply_markup=keyboard)

# Обработка кнопок
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "publish_article":
        await query.edit_message_text(
            text="🔔 Ссылка на публикацию вашего научного труда: [Открыть форму](https://your-platform.com/publish)",
            parse_mode="Markdown"
        )

# Запуск бота
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения.")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()
