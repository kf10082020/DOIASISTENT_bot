# doi_bot.py
import telebot
from doi_handler import handle_doi
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise Exception("❌ Токен Telegram не найден. Убедись, что TELEGRAM_BOT_TOKEN задан в .env")

bot = telebot.TeleBot(TOKEN)

# Обработка входящего сообщения (любой текст)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        doi = message.text.strip().replace("https://doi.org/", "")
        data = handle_doi(doi)

        reply = f"📘 *Название:* {data['title']}\n" \
                f"👨\u200d🔬 *Авторы:* {data['authors']}\n\n" \
                f"📅 *Год:* {data['issued']}\n" \
                f"📚 *Журнал:* {data['journal']}\n" \
                f"📦 *Том:* {data['volume']}\n" \
                f"📎 *Выпуск:* {data['issue']}\n" \
                f"📄 *Страницы:* {data['pages']}\n\n" \
                f"📝 *Аннотация:* {data['abstract']}\n\n" \
                f"📥 *PDF:* {data['pdf_url']}\n" \
                f"🔗 *DOI:* https://doi.org/{doi}\n" \
                f"🌐 *Источник:* {data['url']}"

        bot.send_message(message.chat.id, reply, parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: {str(e)}")

# Запуск бота
if __name__ == "__main__":
    print("🤖 Бот запущен. Ожидание сообщений...")
    bot.infinity_polling()
