import os
import logging
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# --- Логирование ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Метаданные ---
def fetch_metadata_crossref(doi):
    try:
        r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=10)
        r.raise_for_status()
        return r.json()["message"]
    except Exception as e:
        logger.error(f"Crossref error: {e}")
        return None

def fetch_metadata_pubmed(doi):
    try:
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={doi}&retmode=json"
        r = requests.get(search_url, timeout=10)
        pmid = r.json()["esearchresult"]["idlist"][0]
        fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
        soup = BeautifulSoup(requests.get(fetch_url).content, "xml")
        return {
            "title": soup.find("ArticleTitle").text,
            "authors": [x.text for x in soup.find_all("LastName")],
            "journal": soup.find("Title").text,
            "issued": soup.find("PubDate").text,
            "abstract": soup.find("AbstractText").text
        }
    except Exception as e:
        logger.error(f"PubMed error: {e}")
        return None

def fetch_metadata_html(doi_url):
    try:
        r = requests.get(doi_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        meta = lambda name: soup.find("meta", {"name": name})
        get = lambda name: meta(name)["content"] if meta(name) else None
        return {
            "title": get("citation_title"),
            "authors": get("citation_author"),
            "journal": get("citation_journal_title"),
            "issued": get("citation_publication_date"),
            "volume": get("citation_volume"),
            "issue": get("citation_issue"),
            "pages": get("citation_firstpage"),
            "abstract": get("description"),
            "pdf_url": get("citation_pdf_url")
        }
    except Exception as e:
        logger.error(f"HTML metadata error: {e}")
        return None

def build_reply(data):
    if not data:
        return "❌ Не удалось извлечь метаданные."
    
    authors = ", ".join(data.get("authors", [])) if isinstance(data.get("authors"), list) else data.get("authors", "—")
    
    reply = f"📘 *Название:* {data.get('title', '—')}\n"
    reply += f"👨‍🔬 *Авторы:* {authors}\n"
    reply += f"📅 *Год:* {data.get('issued', '—')}\n"
    reply += f"📚 *Журнал:* {data.get('journal', '—')}\n"
    reply += f"📦 *Том:* {data.get('volume', '—')}\n"
    reply += f"📎 *Выпуск:* {data.get('issue', '—')}\n"
    reply += f"📄 *Страницы:* {data.get('pages', '—')}\n"
    reply += f"\n📝 *Аннотация:*\n{data.get('abstract', 'Нет аннотации')}\n"
    
    if data.get("pdf_url"):
        reply += f"\n📥 *PDF:* [Скачать PDF]({data['pdf_url']})\n"
    
    return reply

def extract_doi(text):
    match = re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.I)
    return match[0] if match else None

def handle_doi(doi_url):
    try:
        # Здесь должна быть ваша логика обработки DOI
        # Временно возвращаем тестовые данные
        return {
            "title": "Пример статьи",
            "authors": ["Иванов И.И.", "Петров П.П."],
            "journal": "Научный журнал",
            "issued": "2023",
            "volume": "10",
            "issue": "3",
            "pages": "100-110",
            "abstract": "Это тестовая аннотация",
            "pdf_url": "https://example.com/article.pdf"
        }
    except Exception as e:
        logger.error(f"DOI handling error: {e}")
        return {"error": f"Ошибка обработки DOI: {str(e)}"}

def format_reply(data):
    if "error" in data:
        return data["error"], None
    
    text = build_reply(data)
    keyboard = None
    
    return text, keyboard

# --- Обработчики Telegram ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добрый день! Отправь мне DOI-ссылку, и я выведу метаданные статьи.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    doi = extract_doi(text)
    
    if not doi:
        await update.message.reply_text("❌ DOI не найден. Отправь корректную ссылку.")
        return
    
    await update.message.reply_text("⌛ Обрабатываю запрос...")
    
    metadata = handle_doi(doi)
    reply_text, keyboard = format_reply(metadata)
    
    await update.message.reply_text(
        reply_text,
        reply_markup=keyboard,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "publish_article":
        await query.edit_message_text(
            text="🔔 Ссылка на публикацию вашего научного труда: [Открыть форму](https://your-platform.com/publish)",
            parse_mode="Markdown"
        )

# --- Основная функция ---
def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения.")
    
    app = ApplicationBuilder().token(token).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))
    
    logger.info("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
