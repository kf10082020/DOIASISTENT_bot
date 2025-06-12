def format_reply(data):
    if "error" in data:
        return data["error"]
    return f"Название: {data.get('title', '—')}
" \
           f"Авторы: {data.get('authors', '—')}
" \
           f"Год: {data.get('issued', '—')}
" \
           f"Журнал: {data.get('journal', '—')}

" \
           f"Аннотация:
{data.get('abstract', 'Нет аннотации')}
"
