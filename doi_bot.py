import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN") or "8000984168:AAGRe1CYnGUJ6RRBLCO9qAM3fjbPaXcvSsQ"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне DOI статьи, и я найду по ней информацию.")

def fetch_metadata(doi):
    headers = {"Accept": "application/vnd.citationstyles.csl+json"}
    url = f"https://doi.org/{doi.strip()}" esponse = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    return None

def build_reply(data):
    title = data.get("title", [""])[0]
    authors = ", ".join([author.get("family", "") for author in data.get("author", [])])
    year = data.get("issued", {}).get("date-parts", [[None]])[0][0]
    journal = data.get("container-title", [""])[0]
    volume = data.get("volume", "")
    issue = data.get("issue", "")
    pages = data.get("page", "")
    url = data.get("URL", "")

    text = f"📄 *{title}*
"
    text += f"👤 Авторы: {authors}
"
    text += f"📅 Год: {year}
"
    text += f"📚 Журнал: {journal}
"
    text += f"📦 Том: {volume} | Выпуск: {issue} | Страницы: {pages}
"
    text += f"🔗 [Ссылка на статью]({url})
"

    buttons = [
        [InlineKeyboardButton("🔗 Ссылка на статью", url=url)],
        [InlineKeyboardButton("📤 Поделиться", switch_inline_query=url)],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    return text, reply_markup

async def handle_doi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doi = update.message.text.strip().replace("https://doi.org/", "").replace("doi:", "").strip()
    data = fetch_metadata(doi)
    if data:
        reply, keyboard = build_reply(data)
        await update.message.reply_markdown(reply, reply_markup=keyboard, disable_web_page_preview=True)
    else:
        await update.message.reply_text("Не удалось найти информацию по этому DOI.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_doi))
    app.run_polling()

if __name__ == "__main__":
    main()
