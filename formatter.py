def parse_mdpi_article(url: str, doi: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    def safe_get(name):
        tag = soup.find("meta", {"name": name})
        return tag["content"] if tag else "—"

    title = safe_get("citation_title")
    authors = [tag["content"] for tag in soup.find_all("meta", {"name": "citation_author"})]
    journal = safe_get("citation_journal_title")
    year = safe_get("citation_publication_date").split("/")[0]
    volume = safe_get("citation_volume")
    issue = safe_get("citation_issue")
    pages = safe_get("citation_firstpage") + "–" + safe_get("citation_lastpage")
    pdf_url = safe_get("citation_pdf_url")
    
    return {
        "title": title,
        "authors": ", ".join(authors),
        "journal": journal,
        "issued": year,
        "volume": volume,
        "issue": issue,
        "pages": pages if "—" not in pages else "—",
        "abstract": "—",        # Можно парсить отдельно при необходимости
        "conclusion": "—",      # Нет в структуре MDPI по умолчанию
        "suggestions": "—",     # Нет в структуре MDPI по умолчанию
        "pdf_url": pdf_url,
        "doi": doi,
        "url": url
    }
