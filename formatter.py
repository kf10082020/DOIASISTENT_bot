
def format_reply(metadata: dict) -> str:
    return f"*Название:* {metadata['title']}\n" \
           f"*Авторы:* {", ".join(metadata['authors'])}\n" \
           f"*Журнал:* {metadata['journal']}\n" \
           f"*Год:* {metadata['year']}\n" \
           f"*DOI:* {metadata['doi']}"
