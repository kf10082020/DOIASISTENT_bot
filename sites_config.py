import requests
from bs4 import BeautifulSoup

def parse_springer(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            "title": soup.find('h1').get_text(strip=True),
            "authors": [a.get_text(strip=True) 
                       for a in soup.select('.authors__name')],
            "journal": soup.select_one('.journal-title').get_text(strip=True),
            "issued": soup.select_one('.ArticleCitation_Year').get_text(strip=True),
            "volume": soup.select_one('.ArticleCitation_Volume').get_text(strip=True),
            "issue": soup.select_one('.ArticleCitation_Issue').get_text(strip=True),
            "pages": soup.select_one('.ArticleCitation_Pages').get_text(strip=True),
            "abstract": soup.select_one('.Abstract').get_text(strip=True),
            "pdf_url": f"https://link.springer.com{soup.select_one('.pdf-link')['href']}",
            "doi": url.split('doi.org/')[-1]
        }
    except Exception as e:
        print(f"Springer parser error: {e}")
        return {"error": "❌ Не удалось обработать статью Springer"}
