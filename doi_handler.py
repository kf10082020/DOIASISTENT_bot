from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from sites_config import SITES

def fetch_real_metadata(doi_url):
    """Получение реальных метаданных через Crossref API"""
    try:
        if doi_url.startswith('10.'):
            doi_url = f"https://doi.org/{doi_url}"
        
        # Проверяем, это DOI или прямой URL
        if 'doi.org' in doi_url:
            doi = doi_url.split('doi.org/')[-1]
            url = f"https://api.crossref.org/works/{doi}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()['message']
        else:
            # Для прямых URL используем парсеры из sites_config
            domain = urlparse(doi_url).netloc.replace("www.", "")
            parser = SITES.get(domain)
            if parser:
                return parser(doi_url)
            return None
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return None

def handle_doi(doi_url):
    """Основная функция обработки DOI/URL"""
    try:
        # Получаем реальные метаданные
        data = fetch_real_metadata(doi_url)
        if not data:
            return {"error": "❌ Не удалось получить данные статьи"}
            
        # Стандартизируем структуру данных
        return {
            "title": data.get("title", "Название не указано"),
            "authors": data.get("author", []),
            "issued": data.get("created", {}).get("date-parts", [[""]])[0][0],
            "journal": data.get("container-title", [""])[0],
            "volume": data.get("volume", ""),
            "issue": data.get("issue", ""),
            "pages": data.get("page", ""),
            "abstract": data.get("abstract", "Аннотация недоступна"),
            "pdf_url": data.get("link", [{}])[0].get("URL", ""),
            "doi": doi_url if doi_url.startswith('10.') else ""
        }
    except Exception as e:
        return {"error": f"⚠️ Ошибка обработки: {str(e)}"}
