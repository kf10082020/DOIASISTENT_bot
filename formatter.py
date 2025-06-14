import requests
from bs4 import BeautifulSoup

def parse_mdpi_article(url: str, doi: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    def safe_get(name):
        tag = soup.find("meta", {"name": name})
        return tag["content"] if tag else "—"

    def extract_abstract():
        meta = soup.find("meta", {"name": "dc.Description"})
        if meta and meta.get("content"):
            return meta["content"]
        # Альтернатива: попробовать найти <div class="art-abstract">
        abstract_div = soup.find("div", class_="art-abstract")
        if abstract_div:
            return abstract_div.get_text(strip=True)
        return "—"

    title = safe_get("citation_title")
    authors = [tag["content"] for tag in soup.find_all("meta", {"name": "citation_author"})]
    journal = safe_get("citation_journal_title")
    year = safe_get("citation_publication_date").split("/")[0]
    volume = safe_get("citation_volume")
    issue = safe_get("citation_issue")
    pages = safe_get("citation_firstpage") + "–" + safe_get("citation_lastpage")
    pdf_url = safe_get("citation_pdf_url")
    abstract = extract_abstract()

    return {
        "title": title,
        "authors": ", ".join(authors) if authors else "—",
        "journal": journal,
        "issued": year,
        "volume": volume,
        "issue": issue,
        "pages": pages if "—" not in pages else "—",
        "abstract": abstract,
        "conclusion": "—",      # Можно распарсить из текста статьи по <section> если понадобится
        "suggestions": "—",     # То же самое
        "pdf_url": pdf_url,
        "doi": doi,
        "url": url
    }
