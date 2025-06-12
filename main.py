import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from doi_handler import handle_doi
from formatter import format_reply
from utils import extract_doi

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 День добрый! Отправь DOI-ссылку, и я найду данные публикации.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    doi = extract_doi(text)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not doi:
        await update.message.reply_text("❌ DOI не найден. Пожалуйста, отправьте корректную ссылку.")
        return

    if query.data == "publish_request":
        await query.edit_message_reply_markup()  # убрать кнопки
        await query.message.reply_text("✅ Запрос на публикацию принят. Мы свяжемся с вами позже.")

    
    metadata = handle_doi(doi)
    reply = format_reply(metadata)

    keyboard = [
        [InlineKeyboardButton("📥 Скачать PDF", url=metadata.get("pdf", "#"))],
        [InlineKeyboardButton("📤 Опубликовать труд", callback_data="publish_request")]
    ]
    await update.message.reply_text(reply, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
