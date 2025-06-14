import requests
from urllib.parse import urlparse
from sites_config import SITES  # Убедись, что этот файл есть и корректный

def handle_doi(doi: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html"
    }

    doi_url = f"https://doi.org/{doi}"

    try:
        response = requests.get(doi_url, headers=headers, allow_redirects=True)
    except Exception as e:
        raise Exception(f"Ошибка подключения к https://doi.org: {str(e)}")

    if response.status_code != 200:
        raise Exception(f"Ошибка при переходе по DOI (код: {response.status_code})")

    final_url = response.url
    domain = urlparse(final_url).netloc.lower()

    print(f"[DEBUG] DOI: {doi}")
    print(f"[DEBUG] Redirected URL: {final_url}")
    print(f"[DEBUG] Domain parsed: {domain}")
    print(f"[DEBUG] Known domains: {list(SITES.keys())}")

    if domain in SITES:
        try:
            parsed = SITES[domain](final_url)
            return parsed
        except Exception as e:
            raise Exception(f"Ошибка при парсинге сайта {domain}: {str(e)}")
    else:
        raise Exception(f"Домен {domain} не поддерживается")
