import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from sites_config import SITES

def fetch_crossref_metadata(doi):
    try:
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()['message']
    except Exception as e:
        print(f"Crossref error: {e}")
        return None

def handle_doi(input_text):
    try:
        # Если это DOI (начинается с 10.)
        if input_text.startswith('10.'):
            metadata = fetch_crossref_metadata(input_text)
            if not metadata:
                return {"error": "❌ Не удалось получить данные по этому DOI"}
            
            return {
                "title": ' '.join(metadata.get('title', ['Название не указано'])),
                "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() 
                           for a in metadata.get('author', [])],
                "issued": metadata.get('created', {}).get('date-parts', [[None]])[0][0],
                "journal": ' '.join(metadata.get('container-title', ['Журнал не указан'])),
                "volume": metadata.get('volume'),
                "issue": metadata.get('issue'),
                "pages": metadata.get('page'),
                "abstract": metadata.get('abstract', 'Аннотация недоступна'),
                "pdf_url": metadata.get('link', [{}])[0].get('URL'),
                "doi": input_text
            }
        
        # Если это URL
        domain = urlparse(input_text).netloc.replace("www.", "")
        parser = SITES.get(domain)
        
        if parser:
            return parser(input_text)
            
        return {"error": f"❌ Этот сайт пока не поддерживается: {domain}"}
        
    except Exception as e:
        return {"error": f"⚠️ Ошибка: {str(e)}"}
