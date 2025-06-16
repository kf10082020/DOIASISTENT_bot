from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes, CallbackQueryHandler
import os

# Отправка черновика
async def send_docx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        # Путь к .docx передаётся в callback_data: send_docx|путь
        path = query.data.split("|")[1]
        await query.message.reply_document(
            document=InputFile(path),
            filename=os.path.basename(path),
            caption="📎 Вот ваш сгенерированный черновик."
        )
    except Exception as e:
        await query.message.reply_text(f"⚠️ Ошибка при отправке файла: {e}")

# Заглушка для анализа
async def analyze_article(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("🧠 GPT-анализ пока не подключён. Будет доступен скоро!")

# Заглушка для публикации
async def publish_article(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("📤 Статья опубликована! (эмуляция)")

# Регистрация всех кнопок
def get_handlers():
    return [
        CallbackQueryHandler(send_docx, pattern="^send_docx"),
        CallbackQueryHandler(analyze_article, pattern="^analyze_article$"),
        CallbackQueryHandler(publish_article, pattern="^publish_article$")
    ]
