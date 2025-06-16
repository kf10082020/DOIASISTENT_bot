import os
import logging
from telegram import Update, InlineKeyboardMarkup
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
    await update.message.reply_text(
        "🔍 Научный бот для поиска статей\n\n"
        "Отправьте мне:\n"
        "• DOI статьи (например, 10.1038/nature12373)\n"
        "• Или ссылку на статью с поддерживаемого сайта"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text.startswith('/'):
        return
        
    await update.message.reply_text("🔎 Ищу информацию о статье...")
    
    metadata = handle_doi(text)
    reply_text, keyboard = format_reply(metadata)
    
    await update.message.reply_text(
        reply_text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "publish_request":
        await query.edit_message_reply_markup()
        await query.message.reply_text("📩 Запрос на публикацию отправлен!")

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("❌ Токен бота не найден!")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    logger.info("Бот запущен и готов к работе")
    app.run_polling()

if __name__ == "__main__":
    main()
