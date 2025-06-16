import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверка токена
if not TOKEN:
    logger.error("Токен не найден!")
    print("=" * 50)
    print("Проверьте что:")
    print(f"1. Файл .env существует по пути: {env_path}")
    print("2. Содержит строку: TELEGRAM_BOT_TOKEN=ваш_токен")
    print("3. Файл не переименован")
    print("Текущие переменные окружения:", dict(os.environ))
    print("=" * 50)
    exit(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен! Отправьте мне DOI или ссылку на статью")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    await update.message.reply_text(f"Обрабатываю: {text}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен")
    print("=" * 50)
    print("Бот успешно запущен!")
    print("=" * 50)

    app.run_polling()


if __name__ == "__main__":
    main()
