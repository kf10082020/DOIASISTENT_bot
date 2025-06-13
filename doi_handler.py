import requests
from bs4 import BeautifulSoup

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

    # Пока поддерживаем только MDPI
    if "mdpi.com" in final_url:
        return parse_mdpi_article(final_url, doi)

    raise Exception("❌ DOI не поддерживается: реализована только поддержка MDPI.")

def parse_mdpi_article(url: str, doi: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Ошибка при загрузке страницы MDPI: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    def get_meta(name):
        tag = soup.find("meta", {"name": name})
        return tag["content"].strip() if tag and tag.get("content") else "—"

    title = get_meta("citation_title")
    authors_list = [meta["content"].strip() for meta in soup.find_all("meta", {"name": "citation_author"}) if meta.get("content")]
    authors = ", ".join(authors_list) if authors_list else "—"
    journal = get_meta("citation_journal_title")

    # Для года берем первые 4 цифры из даты публикации (обычно в формате YYYY/MM/DD)
    pub_date = get_meta("citation_publication_date")
    year = pub_date.split("/")[0] if pub_date and pub_date != "—" else "—"

    volume = get_meta("citation_volume")
    issue = get_meta("citation_issue")

    first_page = get_meta("citation_firstpage")
    last_page = get_meta("citation_lastpage")
    pages = f"{first_page}–{last_page}" if first_page != "—" and last_page != "—" else "—"

    pdf_url = get_meta("citation_pdf_url")

    # Ищем аннотацию: у MDPI она обычно внутри div с классом "art-abstract" или "abstract"
    abstract_tag = soup.find("div", class_="art-abstract") or soup.find("div", class_="abstract")
    abstract = abstract_tag.get_text(strip=True) if abstract_tag else "Нет аннотации"

    return {
        "title": title,
        "authors": authors,
        "journal": journal,
        "issued": year,
        "volume": volume,
        "issue": issue,
        "pages": pages,
        "abstract": abstract,
        "conclusion": "—",
        "suggestions": "—",
        "pdf_url": pdf_url,
        "doi": doi,
        "url": url
    }
