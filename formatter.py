from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def format_reply(data):
    if "error" in data:
        return data["error"], None

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

    # Кнопки
    buttons = []
    if data.get("pdf_url"):
        buttons.append([
            InlineKeyboardButton("📥 Скачать PDF", url=data["pdf_url"])
        ])
    buttons.append([
        InlineKeyboardButton("🚀 Опубликовать труд", url="https://yourpublicationform.com")  # можно заменить на webhook
    ])

    keyboard = InlineKeyboardMarkup(buttons)
    return text, keyboard