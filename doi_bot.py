def build_reply(data):
    import re

    def cleanup(text):
        return re.sub(r"<[^>]+>", "", text or "").strip()

    title = data.get("title", ["—"])[0]
    authors = ", ".join([
        f"{a.get('given', '').strip()} {a.get('family', '').strip()}"
        for a in data.get("author", [])
    ]) or "—"

    year_parts = data.get("issued", {}).get("date-parts", [[None]])
    year = year_parts[0][0] if year_parts and year_parts[0] else "—"

    journal = data.get("container-title", ["—"])[0]
    volume = data.get("volume", "—")
    issue = data.get("issue", "—")
    pages = data.get("page", "—")
    publisher = data.get("publisher", "—")
    url = data.get("URL", "—")

    abstract = cleanup(data.get("abstract", "Нет аннотации."))

    reply = f"""📘 *Название:* {title}
👨‍🔬 *Авторы:* {authors}
📅 *Год:* {year}
📚 *Журнал / Сборник:* {journal}
🔢 *Том:* {volume}
📎 *Выпуск:* {issue}
📄 *Страницы:* {pages}
🏢 *Издатель:* {publisher}

📝 *Аннотация:*
{abstract}

📥 *Ссылка:* [Открыть публикацию]({url})
"""
    return reply
