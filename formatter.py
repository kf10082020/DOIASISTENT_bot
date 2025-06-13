from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.helpers import escape_markdown

PUBLISH_URL = "https://yourpublicationform.com"
MAX_LENGTH = 4000

def format_reply(data):
    if "error" in data:
        return data["error"], None

    # Подготовка текста
    text = f"""📘 *Название:* {data.get('title', '—')}
👨‍🔬 *Авторы:* {data.get('authors', '—')}
📅 *Год:* {data.get('issued', '—')}
📚 *Журнал:* {data.get('journal', '—')}
📦 *Том:* {data.get('volume', '—')}
📎 *Выпуск:* {data.get('issue', '—')}
📄 *Страницы:* {data.get('pages', '—')}

📝 *Аннотация:*
{data.get('abstract', 'Нет аннотации')}

✅ *Выводы:*
{data.get('conclusion', '—')}

💡 *Предложения:*
{data.get('suggestions', '—')}
"""

    if len(text) > MAX_LENGTH:
        text = text[:MAX_LENGTH - 3] + "..."

    # Кнопки
    buttons = []
    if data.get("pdf_url"):
        buttons.append([InlineKeyboardButton("📥 Скачать PDF", url=data["pdf_url"])])
    buttons.append([InlineKeyboardButton("🚀 Опубликовать труд", url=PUBLISH_URL)])

    keyboard = InlineKeyboardMarkup(buttons)
    return text, keyboard
