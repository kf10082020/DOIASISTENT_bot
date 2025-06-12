from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def format_reply(data):
    if "error" in data:
        return data["error"], None  # Без кнопок

    title = data.get('title', '—')
    authors = data.get('authors', '—')
    issued = data.get('issued', '—')
    journal = data.get('journal', '—')
    volume = data.get('volume', '—')
    issue = data.get('issue', '—')
    pages = data.get('pages', '—')
    abstract = data.get('abstract', 'Нет аннотации')
    conclusions = data.get('conclusions', 'Нет данных')
    recommendations = data.get('recommendations', 'Нет данных')
    pdf_url = data.get('pdf_url')

    text = (
        f"📘 *Название:* {title}\n"
        f"👨‍🔬 *Авторы:* {authors}\n"
        f"📅 *Год:* {issued}\n"
        f"📚 *Журнал:* {journal}\n"
        f"📦 *Том:* {volume}\n"
        f"📮 *Выпуск:* {issue}\n"
        f"📄 *Страницы:* {pages}\n\n"
        f"📝 *Аннотация:*\n{abstract}\n\n"
        f"🔍 *Выводы:*\n{conclusions}\n\n"
        f"💡 *Предложения:*\n{recommendations}"
    )

    # Создание кнопок
    buttons = []

    if pdf_url:
        buttons.append([InlineKeyboardButton("📥 Скачать PDF", url=pdf_url)])

    buttons.append([
        InlineKeyboardButton("📝 Опубликовать научный труд", callback_data="publish_article")
    ])

    return text, InlineKeyboardMarkup(buttons)
