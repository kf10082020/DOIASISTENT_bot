import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Прямой импорт, так как все файлы в одном каталоге
import publication_handler
import publication_confirm_handler

# Загрузка переменных окружения из .env
load_dotenv()

# Получение значений токена и URL
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RAILWAY_ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT")

# Проверка наличия обязательных переменных
if not TOKEN:
    raise RuntimeError("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен.")
if RAILWAY_ENVIRONMENT == "production" and not WEBHOOK_URL:
    raise RuntimeError("❌ Ошибка: WEBHOOK_URL не установлен для production-среды.")

# Создание приложения Telegram
app = ApplicationBuilder().token(TOKEN).build()

# Обработчик команды /start
app.add_handler(CommandHandler("start", publication_handler.start))

# Обработчик текстовых сообщений (без команд)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, publication_handler.handle_text))

# Обработчики кнопок из модуля подтверждения публикации
for handler in publication_confirm_handler.get_handlers():
    app.add_handler(handler)

# Запуск: Webhook или Polling в зависимости от среды
if RAILWAY_ENVIRONMENT == "production":
    print("🚀 Запуск в режиме Webhook (Railway)")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=WEBHOOK_URL
    )
else:
    print("💻 Запуск в режиме Polling (локально)")
    app.run_polling()
