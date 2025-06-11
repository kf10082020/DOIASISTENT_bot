# 📌 Обновлённый DOI бот DOIASISTENT_bot
# Поддержка извлечения метаданных с разных платформ по DOI

import os
import re
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")  # секретность: перемещено в переменные окружения

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

SUPPORTED_DOMAINS = {
    "mdpi.com": "mdpi",
    "springer.com": "springer",
    "sciencedirect.com": "elsevier",
    "sagepub.com": "sage",
    "tandfonline.com": "taylor",
    "biomedcentral.com": "bmc",
    "frontiersin.org": "frontiers",
    "routledge.com": "routledge",
    "wiley.com": "wiley",
    "jstor.org": "jstor",
    "muse.jhu.edu": "muse",
    "crossref.org": "crossref",
    "scholar.google.com": "scholar",
    "doaj.org": "doaj",
    "pubmed.ncbi.nlm.nih.gov": "pubmed",
    "ijirmf.com": "ijirmf",
    "eric.ed.gov": "eric",
    "ieeexplore.ieee.org": "ieee",
    "dl.acm.org": "acm",
    "ssrn.com": "ssrn"
}

def extract_domain(doi_url: str) -> str:
    for domain in SUPPORTED_DOMAINS:
        if domain in doi_url:
            return SUPPORTED_DOMAINS[domain]
    return "crossref"  # fallback по умолчанию

def get_crossref_metadata(doi: str):
    headers = {"Accept": "application/vnd.citationstyles.csl+json"}
    url = f"https://doi.org/{doi}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def format_post(meta):
    return f"""
📚 *Название:* {meta.get('title', ['—'])[0]}
👨‍🔬 *Авторы:*
{'; '.join([a['family'] + ', ' + a['given'] for a in meta.get('author', [])])}

📅 *Год:* {meta.get('issued', {}).get('date-parts', [['—']])[0][0]}
📚 *Журнал:* {meta.get('container-title', ['—'])[0]}
📦 *Том:* {meta.get('volume', '—')}
📎 *Выпуск:* {meta.get('issue', '—')}
📄 *Страницы:* {meta.get('page', '—')}

📝 *Аннотация:*
{meta.get('abstract', 'Нет аннотации')}

📥 *PDF:* [Ссылка]({meta.get('URL', '—')})
🔗 *DOI:* https://doi.org/{meta.get('DOI', '—')}
🌐 *Источник:* {extract_domain(meta.get('URL', ''))}
"""

async def handle_doi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doi_input = update.message.text.strip()
    match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", doi_input, re.I)
    if not match:
        await update.message.reply_text("❌ DOI не распознан. Пожалуйста, введите корректный DOI.")
        return
    doi = match.group(0)
    meta = get_crossref_metadata(doi)
    if not meta:
        await update.message.reply_text("⚠️ Не удалось получить метаданные по данному DOI.")
        return
    post = format_post(meta)
    await update.message.reply_markdown(post, disable_web_page_preview=False)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_doi))
    app.run_polling()
