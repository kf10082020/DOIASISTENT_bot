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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.critical("Токен Telegram не найден! Завершение.")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 День добрый! Отправь DOI-ссылку, и я найду данные публикации.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        doi = extract_doi(text)

        if not doi:
            await update.message.reply_text("❌ DOI не найден. Пожалуйста, отправьте корректную ссылку.")
            return

        await update.message.reply_text("⌛ Обрабатываю запрос, подождите...")

        metadata = handle_doi(doi)
        if not isinstance(metadata, dict):
            logger.warning("Некорректный формат данных от handle_doi: %s", metadata)
            await update.message.reply_text("⚠️ Возникла ошибка при обработке запроса.")
            return

        reply = format_reply(metadata)

        keyboard = [
            [InlineKeyboardButton("📥 Скачать PDF", url=metadata.get("pdf_url", "#"))],
            [InlineKeyboardButton("📤 Опубликовать труд", callback_data="publish_request")]
        ]

        await update.message.reply_text(
            reply, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except Exception as e:
        logger.exception("Ошибка в handle_message: %s", e)
        await update.message.reply_text("🔴 Произошла непредвиденная ошибка. Попробуйте снова.")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        if query.data == "publish_request":
            try:
                await query.edit_message_reply_markup(reply_markup=None)
            except Exception:
                logger.warning("Не удалось убрать клавиатуру.")
            await query.message.reply_text("✅ Запрос на публикацию принят. Мы свяжемся с вами позже.")
        else:
            logger.info("Получен неизвестный callback_data: %s", query.data)

    except Exception as e:
        logger.exception("Ошибка в handle_callback: %s", e)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))

    logger.info("Бот запущен и слушает сообщения.")
    app.run_polling()

if __name__ == "__main__":
    main()
