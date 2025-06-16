import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import publication_handler
import publication_confirm_handler

# ✅ Загрузка переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RAILWAY_ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT")

# ✅ Проверка ключей
if not TOKEN:
    raise RuntimeError("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен.")
if RAILWAY_ENVIRONMENT == "production" and not WEBHOOK_URL:
    raise RuntimeError("❌ Ошибка: WEBHOOK_URL не установлен.")

# ✅ Инициализация Telegram-приложения
app = ApplicationBuilder().token(TOKEN).build()

# ✅ Обработчики команд и текста
app.add_handler(CommandHandler("start", publication_handler.start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, publication_handler.handle_text))

# ✅ Обработчики кнопок
for handler in publication_confirm_handler.get_handlers():
    app.add_handler(handler)

# ✅ Выбор режима
if RAILWAY_ENVIRONMENT == "production":
    print("🚀 Webhook запуск (Railway)")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=WEBHOOK_URL
    )
else:
    print("💻 Polling запуск (локальный)")
    app.run_polling()
