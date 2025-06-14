import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv
from sites_config import SITES

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_site_parser(url):
    domain = urlparse(url).netloc
    return SITES.get(domain)

def handle_doi(doi: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html"
    }

    doi_url = f"https://doi.org/{doi}"
    response = requests.get(doi_url, headers=headers, allow_redirects=True)

    if response.status_code != 200:
        raise Exception(f"Ошибка при переходе по DOI: {response.status_code}")

    final_url = response.url
    parser = get_site_parser(final_url)

    if not parser:
        raise Exception("❌ DOI не поддерживается: сайт не найден в списке.")

    metadata = parser(final_url)
    metadata.update({"doi": doi, "url": final_url})
    return metadata

def save_to_json(data, filename="doi_result.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def send_to_telegram(metadata):
    message = (
        f"📘 *Название:* {metadata['title']}\n"
        f"👨‍🔬 *Авторы:* {metadata['authors']}\n"
        f"📚 *Журнал:* {metadata['journal']} ({metadata['issued']})\n"
        f"📦 *Том:* {metadata['volume']}\n"
        f"📎 *Выпуск:* {metadata['issue']}\n"
        f"📄 *Страницы:* {metadata['pages']}\n\n"
        f"📝 *Аннотация:* {metadata['abstract']}\n\n"
        f"📥 *PDF:* {metadata['pdf_url']}\n"
        f"🔗 *DOI:* https://doi.org/{metadata['doi']}\n"
        f"🌐 *Источник:* {metadata['url']}"
    )

    keyboard = {
        "inline_keyboard": [
            [{"text": "📥 Сохранить PDF", "url": metadata["pdf_url"]}],
            [{"text": "🚀 Опубликовать", "callback_data": "publish_paper"}]
        ]
    }

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "reply_markup": json.dumps(keyboard)
        }
    )

if __name__ == "__main__":
    doi = input("Введите DOI статьи: ").strip()
    try:
        metadata = handle_doi(doi)
        save_to_json(metadata)
        send_to_telegram(metadata)
        print("✅ Успешно обработано и отправлено в Telegram.")
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
