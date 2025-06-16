import telebot
from dotenv import load_dotenv
import os
from doi_handler import handle_doi

# Загружаем переменные окружения из .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверка на наличие токена
if not BOT_TOKEN:
    raise ValueError("❌ Переменная TELEGRAM_BOT_TOKEN не найдена. Проверь .env файл.")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        doi = message.text.strip().replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
        if not doi:
            bot.send_message(message.chat.id, "⚠️ Пожалуйста, введите корректный DOI-ссылку.")
            return

        data = handle_doi(doi)

        reply = (
            f"📘 *Название:* {data.get('title', '—')}\n"
            f"👨‍🔬 *Авторы:* {data.get('authors', '—')}\n\n"
            f"📅 *Год:* {data.get('issued', '—')}\n"
            f"📚 *Журнал:* {data.get('journal', '—')}\n"
            f"📦 *Том:* {data.get('volume', '—')}\n"
            f"📎 *Выпуск:* {data.get('issue', '—')}\n"
            f"📄 *Страницы:* {data.get('pages', '—')}\n\n"
            f"📝 *Аннотация:* {data.get('abstract', '—')}\n\n"
            f"📥 *PDF:* {data.get('pdf_url', '—')}\n"
            f"🔗 *DOI:* https://doi.org/{doi}\n"
            f"🌐 *Источник:* {data.get('url', '—')}"
        )

        bot.send_message(message.chat.id, reply, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: {str(e)}")

# Запуск только для Railway или локального окружения
if __name__ == "__main__":
    print("🤖 DOI бот запущен и ждёт сообщений...")
    bot.polling(non_stop=True)  # Важно! Только один polling-процесс!
