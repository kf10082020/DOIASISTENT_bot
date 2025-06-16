from telegram import Update
from telegram.ext import ContextTypes
from utils import extract_doi  # 🔄 Прямой импорт функции из utils.py

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь DOI статьи.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    doi = extract_doi(text)
    if doi:
        await update.message.reply_text(f"🔎 Найден DOI: {doi}")
    else:
        await update.message.reply_text("❌ DOI не найден.")
