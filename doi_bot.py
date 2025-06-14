import os
import telebot
from dotenv import load_dotenv
from doi_handler import handle_doi

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализируем бота
bot = telebot.TeleBot(TOKEN)

# Обработка всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        doi = message.text.strip().replace("https://doi.org/", "")
        data = handle_doi(doi)

        reply = f"📘 *Название:* {data['title']}\n" \
                f"👨‍🔬 *Авторы:* {data['authors']}\n\n" \
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

# Запускаем бота
if __name__ == '__main__':
    print("🤖 Бот запущен...")
    bot.infinity_polling()
