import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import publication_handler, publication_confirm_handler

# 🔁 Загрузка переменных из .env
load_dotenv()

# 🔐 Получение токена и URL webhook
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ENV = os.getenv("ENV", "development")  # можно задать: development или production

# 🚫 Проверка наличия токена
if not TOKEN:
    raise RuntimeError("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен.")

# 🤖 Инициализация приложения
app = ApplicationBuilder().token(TOKEN).build()

# 📌 Обработчики команд
app.add_handler(CommandHandler("start", publication_handler.start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, publication_handler.handle_text))

# 📎 Подключение подтверждающих обработчиков
for handler in publication_confirm_handler.get_handlers():
    app.add_handler(handler)

# 🚀 Запуск в нужном режиме
if ENV == "production":
    if not WEBHOOK_URL:
        raise RuntimeError("❌ Ошибка: WEBHOOK_URL не установлен.")
    print("🚀 Запуск в режиме webhook...")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=WEBHOOK_URL
    )
else:
    print("💻 Запуск в режиме polling...")
    app.run_polling()
