import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Прямой импорт, если файлы находятся в том же каталоге
import publication_handler
import publication_confirm_handler

# Загружаем переменные окружения из .env
load_dotenv()

# Считываем переменные
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RAILWAY_ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT", "local")  # по умолчанию — локальный режим

# Проверка наличия обязательных переменных
if not TOKEN:
    raise RuntimeError("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен.")
if RAILWAY_ENVIRONMENT == "production" and not WEBHOOK_URL:
    raise RuntimeError("❌ Ошибка: WEBHOOK_URL не установлен в production-среде.")

# Инициализация Telegram-приложения
app = ApplicationBuilder().token(TOKEN).build()

# Команда /start
app.add_handler(CommandHandler("start", publication_handler.start))

# Обработка обычного текста
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, publication_handler.handle_text))

# Подключение кнопок
for handler in publication_confirm_handler.get_handlers():
    app.add_handler(handler)

# Выбор режима запуска
if RAILWAY_ENVIRONMENT == "production":
    print("🚀 Запуск через webhook (Railway)")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=WEBHOOK_URL
    )
else:
    print("💻 Запуск локально (polling)")
    app.run_polling()
