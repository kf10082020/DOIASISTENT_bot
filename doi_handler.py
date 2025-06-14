import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from sites_config import SITES  # импорт словаря доменов и функций

def handle_doi(doi: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html"
    }

    doi_url = f"https://doi.org/{doi}"
    response = requests.get(doi_url, headers=headers, allow_redirects=True)

    if response.status_code != 200:
        raise Exception(f"Ошибка при переходе по DOI: {response.status_code}")

    final_url = response.url
    domain = urlparse(final_url).netloc

    if domain in SITES:
        # Вызов нужного парсера
        try:
            parsed = SITES[domain](final_url)
            parsed.update({
                "doi": doi,
                "url": final_url
            })
            return parsed
        except Exception as e:
            raise Exception(f"Ошибка при парсинге {domain}: {str(e)}")
    else:
        raise Exception(f"❌ Неизвестный домен ({domain}). Поддерживаются только: {', '.join(SITES.keys())}")
