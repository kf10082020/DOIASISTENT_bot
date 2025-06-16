import os
import openai

# Получение ключа из .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_text(prompt: str) -> str:
    """
    Отправляет текст на анализ в GPT и возвращает результат.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Можно заменить на "gpt-3.5-turbo" при необходимости
            messages=[
                {"role": "system", "content": "Ты помощник научного редактора. Анализируй статью строго, чётко и по делу."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Ошибка при анализе: {e}"
