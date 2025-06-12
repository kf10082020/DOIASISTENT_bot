from urllib.parse import urlparse
from sites_config import SITES

def handle_doi(doi_url):
    try:
        domain = urlparse(doi_url).netloc.replace("www.", "")
        parser = SITES.get(domain)
        if not parser:
            return {"error": f"❌ Неизвестный источник: {domain}"}
        return parser(doi_url)
    except Exception as e:
        return {"error": f"⚠️ Ошибка обработки DOI: {str(e)}"}
