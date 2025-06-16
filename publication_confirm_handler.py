from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes, CallbackQueryHandler
import os

# �������� ��������� ������������
async def send_draft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    draft_path = "templates/sample_generated_article.docx"
    if not os.path.exists(draft_path):
        await update.callback_query.message.reply_text("?? �������� ���� �� ������������.")
        return

    await update.callback_query.message.reply_document(
        document=InputFile(draft_path),
        caption="?? �������� ����� ������. ��������� ��� ����� �����������.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("? � ��������, �� �����", callback_data="confirm_ready")]
        ])
    )

# ������������� ���������� � ����������
async def confirm_ready_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "?? ������������. ������ ������ � ����������.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("?? ������������ ������", callback_data="final_publish")]
        ])
    )

# ��������� ���� � ���������� (��������)
async def final_publish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("? ������ ������������! (�������� ��������)")

# ����������� ������������
def get_handlers():
    return [
        CallbackQueryHandler(send_draft, pattern="^send_draft$"),
        CallbackQueryHandler(confirm_ready_callback, pattern="^confirm_ready$"),
        CallbackQueryHandler(final_publish_callback, pattern="^final_publish$")
    ]
