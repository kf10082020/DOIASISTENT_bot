def format_metadata(metadata: dict) -> str:
    return (
        f"📘 *Название:* {metadata.get('title', '—')}\n"
        f"👨‍🔬 *Авторы:* {metadata.get('authors', '—')}\n"
        f"📚 *Журнал:* {metadata.get('journal', '—')}\n"
        f"📅 *Год:* {metadata.get('issued', '—')}\n"
        f"📦 *Том:* {metadata.get('volume', '—')}  №{metadata.get('issue', '—')}\n"
        f"📄 *Страницы:* {metadata.get('pages', '—')}\n\n"
        f"📝 *Аннотация:*\n{metadata.get('abstract', '—')}\n\n"
        f"🔚 *Выводы:*\n{metadata.get('conclusion', '—')}\n\n"
        f"💡 *Предложения:*\n{metadata.get('suggestions', '—')}\n\n"
        f"📥 *PDF:* {metadata.get('pdf_url', 'Нет')}\n"
        f"🔗 *DOI:* {metadata.get('doi', '—')}\n"
        f"🌐 *Источник:* {metadata.get('url', '—')}"
    )
