import requests
from bs4 import BeautifulSoup

def handle_doi(doi: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html"
    }

    # Переходим по DOI
    doi_url = f"https://doi.org/{doi}"
    response = requests.get(doi_url, headers=headers, allow_redirects=True)

    if response.status_code != 200:
        raise Exception(f"Ошибка запроса: {response.status_code}")

    final_url = response.url

    # Обработка MDPI
    if "mdpi.com" in final_url:
        return parse_mdpi_article(final_url, doi)

    raise Exception("❌ DOI не поддерживается: пока реализована только поддержка MDPI.")

def parse_mdpi_article(url: str, doi: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find("meta", {"name": "citation_title"})["content"]
    authors = [meta["content"] for meta in soup.find_all("meta", {"name": "citation_author"})]
    journal = soup.find("meta", {"name": "citation_journal_title"})["content"]
    year = soup.find("meta", {"name": "citation_publication_date"})["content"].split("/")[0]
    pdf_url = soup.find("meta", {"name": "citation_pdf_url"})["content"]

    return {
        "title": title,
        "authors": authors,
        "journal": journal,
        "year": year,
        "doi": doi,
        "url": url,
        "pdf_url": pdf_url
    }
