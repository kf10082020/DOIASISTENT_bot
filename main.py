async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "👋 Привет! Я научный бот. Отправь мне:\n"
        "- DOI статьи (например, 10.1038/nature12373)\n"
        "- Или прямую ссылку на статью с поддерживаемого сайта"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text.strip()
    
    # Пропускаем команды
    if text.startswith('/'):
        return
        
    await update.message.reply_text("⌛ Обрабатываю запрос, подождите...")
    
    # Передаем текст как есть в handle_doi
    metadata = handle_doi(text)
    reply_text, keyboard = format_reply(metadata)
    
    await update.message.reply_text(
        reply_text,
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
