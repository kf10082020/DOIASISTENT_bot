from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.formatter import format_metadata
from parsers import handle_doi
from docx_generator import generate_docx
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("?? Отправьте DOI, и я покажу подробности статьи!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doi = update.message.text.strip().replace("https://doi.org/", "")
    metadata = handle_doi(doi)

    if not metadata:
        await update.message.reply_text("?? Не удалось обработать DOI.")
        return

    text = format_metadata(metadata)
    await update.message.reply_markdown(text)

    output_path = f"temp/{doi.replace('/', '_')}.docx"
    os.makedirs("temp", exist_ok=True)
    generate_docx(metadata, output_path)

    keyboard = [
        [InlineKeyboardButton("?? Скачать черновик", callback_data=f"send_docx|{output_path}")],
        [InlineKeyboardButton("?? Анализировать статью", callback_data="analyze_article")],
        [InlineKeyboardButton("?? Опубликовать статью", callback_data="publish_article")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Что вы хотите сделать дальше?", reply_markup=reply_markup)
