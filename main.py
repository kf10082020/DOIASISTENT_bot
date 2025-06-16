import os
from telegram.ext import ApplicationBuilder

from handlers import publication_handler, publication_confirm_handler

app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

app.add_handler(CommandHandler("start", publication_handler.start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, publication_handler.handle_text))
for h in publication_confirm_handler.get_handlers():
    app.add_handler(h)

if os.getenv("RAILWAY_ENVIRONMENT") == "production":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=os.getenv("WEBHOOK_URL")
    )
else:
    app.run_polling()
