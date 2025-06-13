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
from doi_bot import handle_button
from doi_handler import handle_doi
from formatter import format_reply
from utils import extract_doi

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка токена
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.critical("Токен Telegram не найден! Завершение.")
    exit(1)

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "👋 День добрый! Отправь DOI-ссылку, и я найду данные публикации."
        )
    except Exception as e:
        logger.exception("Ошибка при обработке команды /start: %s", e)

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        doi = extract_doi(text)

        if not doi:
            await update.message.reply_text("❌ DOI не найден. Пожалуйста, отправьте корректную ссылку.")
            return

        await update.message.reply_text("⌛ Обрабатываю запрос, подождите...")

        # Обработка DOI
        metadata = handle_doi(doi)
        if not isinstance(metadata, dict):
            # Если ответ не словарь — логируем и возвращаем ошибку
            logger.warning("Некорректный формат данных от handle_doi: %s", metadata)
            await update.message.reply_text("⚠️ Возникла ошибка при обработке запроса.")
            return

        reply = format_reply(metadata)

        # Создаем клавиатуру
        keyboard = [
            [InlineKeyboardButton("📥 Скачать PDF", url=metadata.get("pdf", "#"))],
            [InlineKeyboardButton("📤 Опубликовать труд", callback_data="publish_request")]
        ]

        await update.message.reply_text(
            reply, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except Exception as e:
        logger.exception("Ошибка в handle_message: %s", e)
        await update.message.reply_text("🔴 Произошла непредвиденная ошибка. Попробуйте снова.")

# Обработка нажатий на кнопки
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        if query.data == "publish_request":
            # Удаляем кнопки
            try:
                await query.edit_message_reply_markup(reply_markup=None)
            except Exception:
                # Иногда бывает, что сообщения уже изменены или кнопки отсутствуют
                logger.warning("Не удалось убрать клавиатуру.")
            await query.message.reply_text("✅ Запрос на публикацию принят. Мы свяжемся с вами позже.")

        else:
            # Обработка неизвестных data
            logger.info("Получен неизвестный callback_data: %s", query.data)

    except Exception as e:
        logger.exception("Ошибка в handle_callback: %s", e)

# Создаем и запускаем бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрация хендлеров
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))
    # Еще можно добавить обработчик ошибок
    # app.add_error_handler(error_handler)

    # Запуск polling
    logger.info("Бот запущен и слушает сообщения.")
    app.run_polling()

if __name__ == "__main__":
    main()
