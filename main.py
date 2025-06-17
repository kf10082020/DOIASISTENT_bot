import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import publication_handler, publication_confirm_handler
from dotenv import load_dotenv

# ✅ Загрузка .env
load_dotenv()

# ✅ Переменные окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RAILWAY_ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT", "development")

# ✅ Проверка ключей
if not TOKEN:
    raise RuntimeError("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен.")

# ✅ Инициализация Telegram-приложения
app = ApplicationBuilder().token(TOKEN).build()

# ✅ Обработчики
app.add_handler(CommandHandler("start", publication_handler.start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, publication_handler.handle_text))

for handler in publication_confirm_handler.get_handlers():
    app.add_handler(handler)

# ✅ Запуск (только один из двух)
if RAILWAY_ENVIRONMENT == "production":
    print("🚀 Запуск webhook")
    if not WEBHOOK_URL:
        raise RuntimeError("❌ Ошибка: WEBHOOK_URL не установлен.")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=WEBHOOK_URL
    )
else:
    print("💻 Запуск polling")
    app.run_polling()
