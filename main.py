import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from doi_handler import handle_doi
from formatter import format_reply
from utils import extract_doi

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text("👋 День добрый! Отправь DOI-ссылку, и я найду данные публикации.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text.strip()
    doi = extract_doi(text)

    if not doi:
        await update.message.reply_text("❌ DOI не найден. Пожалуйста, отправьте корректную ссылку.")
        return

    await update.message.reply_text("⌛ Обрабатываю запрос, подождите...")

    metadata = handle_doi(text)  # Передаем полный текст, так как handle_doi сам разберет DOI
    reply_text, keyboard = format_reply(metadata)
    
    await update.message.reply_text(
        reply_text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()

    if query.data == "publish_request":
        await query.edit_message_reply_markup()
        await query.message.reply_text("✅ Запрос на публикацию принят. Мы свяжемся с вами позже.")

def main():
    """Запуск бота"""
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("❌ TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    logger.info("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
