import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from doi_handler import handle_doi
from formatter import format_reply

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()  # Загружает переменные из файла .env


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "🔍 Научный бот для поиска статей\n\n"
        "Отправьте мне:\n"
        "- DOI статьи (например, 10.1038/nature12373)\n"
        "- Или прямую ссылку на статью с поддерживаемого сайта"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text.strip()
    logger.info(f"Получено сообщение: {text}")

    # Пропускаем команды
    if text.startswith('/'):
        return

    await update.message.reply_text("⌛ Обрабатываю запрос, подождите...")

    try:
        metadata = handle_doi(text)
        reply_text, keyboard = format_reply(metadata)

        await update.message.reply_text(
            reply_text,
            parse_mode="Markdown",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await update.message.reply_text("❌ Произошла ошибка при обработке запроса")


def main():
    """Точка входа в приложение"""
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Проверка токена
    if not TOKEN:
        logger.error("Токен не найден! Проверьте файл .env")
        print("=" * 50)
        print("ОШИБКА: TELEGRAM_BOT_TOKEN не найден в переменных окружения")
        print("Убедитесь, что:")
        print("1. Файл .env существует в корне проекта")
        print("2. Содержит строку: TELEGRAM_BOT_TOKEN=ваш_токен")
        print("3. Файл .env не переименован")
        print("=" * 50)
        return

    try:
        app = ApplicationBuilder().token(TOKEN).build()

        # Регистрация обработчиков
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        logger.info("Бот запускается...")
        print("=" * 50)
        print("Бот успешно запущен!")
        print("Остановите бота сочетанием клавиш Ctrl+C")
        print("=" * 50)

        app.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    main()
