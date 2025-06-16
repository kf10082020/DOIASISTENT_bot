from urllib.parse import urlparse
from sites_config import SITES

def handle_doi(doi_url):
    """
    Обрабатывает DOI или URL статьи и возвращает метаданные
    """
    try:
        # Если это DOI (начинается с 10.), добавляем https://doi.org/
        if doi_url.startswith("10."):
            doi_url = f"https://doi.org/{doi_url}"
        
        domain = urlparse(doi_url).netloc.replace("www.", "")
        parser = SITES.get(domain)
        
        if not parser:
            return {"error": f"❌ Неизвестный источник: {domain}"}
        
        return parser(doi_url)
    except Exception as e:
        return {"error": f"⚠️ Ошибка обработки DOI: {str(e)}"}
