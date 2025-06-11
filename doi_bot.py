import os
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Заменить на свой токен
TOKEN = os.getenv("TOKEN") or "7822435522:AAH-ZTQuCCxSr385076vyljKLwO8k5Un3DU"

# Настройка логов
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# === ФУНКЦИЯ 1 === ПОЛУЧЕНИЕ МЕТАДАННЫХ ИЗ CROSSREF ===
def fetch_metadata_from_crossref(doi: str):
    url = f"https://api.crossref.org/works/{doi}"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Ошибка при получении Crossref: {e}")
    return None

# === ФУНКЦИЯ 2 === ПАРСИНГ HTML-КАРТОЧКИ ПУБЛИКАЦИИ (резервный путь) ===
def fetch_metadata_from_html(doi_url: str):
    try:
        res = requests.get(doi_url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.find("meta", attrs={"name": "citation_title"})
        authors = soup.find_all("meta", attrs={"name": "citation_author"})
        year = soup.find("meta", attrs={"name": "citation_publication_date"})
        journal = soup.find("meta", attrs={"name": "citation_journal_title"})
        pages = soup.find("meta", attrs={"name": "citation_firstpage"})

        return {
            "title": title["content"] if title else "—",
            "authors": [a["content"] for a in authors] if authors else [],
            "year": year["content"] if year else "—",
            "journal": journal["content"] if journal else "—",
            "pages": pages["content"] if pages else "—",
            "download_link": doi_url
        }
    except Exception as e:
        logger.error(f"Ошибка при HTML-парсинге: {e}")
        return None

# === ФОРМИРОВАНИЕ РЕСПОНСА ===
import re

def clean_html(text):
    return re.sub('<[^<]+?>', '', text)

def build_reply(data):
    title    = data.get("title", ["–"])[0]
    authors  = ", ".join([a.get("family", "") for a in data.get("author", [])])
    issued   = data.get("issued", {}).get("date-parts", [[None]])[0][0] or "—"
    journal  = data.get("container-title", ["–"])[0]
    volume   = data.get("volume", "–")
    issue    = data.get("issue", "–")
    pages    = data.get("page", "–")
    url      = data.get("URL", "–")
    abstract = data.get("abstract", "—")
    abstract_clean = clean_html(abstract)
    abstract_ru = "перевод временно отключен"

    text = (
        f"*📘 Название:* {title}\n"
        f"*✍️ Авторы:* {authors}\n"
        f"*📅 Год:* {issued}\n"
        f"*🏛 Журнал:* {journal}\n"
        f"*📑 Том / Выпуск / Страницы:* {volume} / {issue} / {pages}\n"
        f"*🔗 DOI / URL:* {url}\n\n"
        f"*📝 Аннотация:* {abstract_clean[:500]}...\n"
        f"*🔄 Перевод:* {abstract_ru}"
    )
    return text
        )
    else:
        return (
            f"📖 *Название:* {data['title']}\n"
            f"👨‍🔬 *Авторы:* {', '.join(data['authors']) or '—'}\n"
            f"📅 *Год:* {data['year']}\n"
            f"📚 *Журнал:* {data['journal']}\n"
            f"📄 *Страницы:* {data['pages']}\n"
            f"🔗 *Ссылка:* {data['download_link']}"
        )

# === ОБРАБОТЧИК СООБЩЕНИЙ С DOI ===
async def handle_doi(update: Update, context: CallbackContext):
    doi_url = update.message.text.strip()
    if "doi.org/" not in doi_url:
        await update.message.reply_text("❗ Пожалуйста, отправьте ссылку вида `https://doi.org/...`")
        return

    doi = doi_url.split("doi.org/")[-1]
    metadata = fetch_metadata_from_crossref(doi)

    if metadata:
        response = build_response(metadata)
    else:
        fallback_data = fetch_metadata_from_html(doi_url)
        if fallback_data:
            response = build_response(fallback_data)
        else:
            response = "⚠️ Не удалось получить информацию по ссылке."

    await update.message.reply_text(response, parse_mode="Markdown")

# === СТАРТ КОМАНДА ===
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Отправьте мне DOI статьи, и я найду по ней информацию.")

# === ОСНОВНОЙ ЦИКЛ ===
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_doi))
    app.run_polling()

if __name__ == "__main__":
    main()
