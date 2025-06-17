import os
import re
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# Загружаем переменные среды
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен в .env")

# Парсеры для сайтов
def parse_mdpi(doi): return requests.get(f"https://api.crossref.org/works/{doi}").json()['message']
def parse_springer(doi): return requests.get(f"https://api.crossref.org/works/{doi}").json()['message']
def parse_sciencedirect(doi): return requests.get(f"https://api.crossref.org/works/{doi}").json()['message']
def parse_pubmed(doi): return requests.get(f"https://api.crossref.org/works/{doi}").json()['message']
def parse_wiley(doi): return requests.get(f"https://api.crossref.org/works/{doi}").json()['message']
def parse_ssrn(doi): return requests.get(f"https://api.crossref.org/works/{doi}").json()['message']

site_parsers = {
    "www.mdpi.com": parse_mdpi,
    "link.springer.com": parse_springer,
    "www.sciencedirect.com": parse_sciencedirect,
    "pubmed.ncbi.nlm.nih.gov": parse_pubmed,
    "onlinelibrary.wiley.com": parse_wiley,
    "www.ssrn.com": parse_ssrn,
}

def extract_doi(text: str):
    match = re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.I)
    return match[0] if match else None

def get_domain_from_doi(doi: str):
    try:
        url = requests.get(f"https://doi.org/{doi}", allow_redirects=True, timeout=10).url
        return urlparse(url).netloc
    except Exception:
        return None

def fetch_metadata(doi: str):
    domain = get_domain_from_doi(doi)
    if domain in site_parsers:
        return site_parsers[domain](doi)
    else:
        # fallback через CrossRef
        return requests.get(f"https://api.crossref.org/works/{doi}").json()['message']

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    doi = extract_doi(text)
    if not doi:
        await update.message.reply_text("❌ DOI не найден.")
        return

    try:
        data = fetch_metadata(doi)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при получении данных: {e}")
        return

    title = data.get("title", ["—"])[0]
    authors = ", ".join([f"{a.get('family', '')} {a.get('given', '')}" for a in data.get("author", [])]) or "—"
    journal = data.get("container-title", ["—"])[0]
    year = data.get("published-print", {}).get("date-parts", [[None]])[0][0] or data.get("issued", {}).get("date-parts", [[None]])[0][0]

    msg = f"""📘 *{title}*
👨‍🔬 *Авторы:* {authors}
📚 *Журнал:* {journal}
📅 *Год:* {year}
🔗 *DOI:* https://doi.org/{doi}
"""
    await update.message.reply_markdown(msg)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Отправьте DOI-ссылку, и я найду публикацию.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
