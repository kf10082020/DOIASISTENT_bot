from urllib.parse import urlparse
from sites_config import SITES

def handle_doi(doi_url):
    try:
        # Анализируем URL и получаем домен
        parsed_url = urlparse(doi_url)
        domain = parsed_url.netloc.lower().replace("www.", "").strip()

        # Проверяем наличие обработчика для домена
        parser = SITES.get(domain)
        if not parser:
            return {
                "error": f"❌ Неизвестный источник: {domain}"
            }

        # Выполняем обработчик и ловим исключения внутри
        try:
            result = parser(doi_url)
            return result
        except Exception as e:
            # Обработка ошибок внутри обработчика
            return {
                "error": f"⚠️ Ошибка при обработке URL {doi_url} для {domain}: {str(e)}"
            }
    except Exception as e:
        # Общая обработка исключений
        return {
            "error": f"⚠️ Общая ошибка обработки DOI: {str(e)}"
        }
