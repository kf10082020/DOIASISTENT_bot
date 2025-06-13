from urllib.parse import urlparse
from sites_config import SITES

def handle_doi(doi_url):
    try:
        domain = urlparse(doi_url).netloc.lower().replace("www.", "")
        parser = SITES.get(domain)
        if not parser:
            return {"error": f"❌ Неизвестный источник: {domain}"}
        try:
            return parser(doi_url)
        except Exception as e:
            return {"error": f"⚠️ Ошибка вызова обработчика для {domain}: {str(e)}"}
    except Exception as e:
        return {"error": f"⚠️ Ошибка обработки DOI: {str(e)}"}
