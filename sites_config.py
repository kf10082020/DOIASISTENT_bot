import requests
from bs4 import BeautifulSoup

def fetch_metadata_html(url: str) -> dict:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Заголовок
        title_tag = soup.find("h1", class_="title")
        title = title_tag.get_text(strip=True) if title_tag else "—"

        # Авторы
        authors_tag = soup.find("div", class_="art-authors")
        authors = authors_tag.get_text(" ", strip=True) if authors_tag else "—"

        # Журнал и дата
        journal_tag = soup.find("span", class_="journal-title")
        journal = journal_tag.get_text(strip=True) if journal_tag else "MDPI"

        date_tag = soup.find("div", class_="pubhistory")
        issued = date_tag.get_text(strip=True).split(";")[0].replace("Published: ", "") if date_tag else "—"

        # Том, выпуск, страницы (берём из breadcrumbs)
        breadcrumbs = soup.find("ol", class_="breadcrumb")
        parts = breadcrumbs.get_text(" ", strip=True).split() if breadcrumbs else []
        volume = parts[parts.index("Volume") + 1] if "Volume" in parts else "—"
        issue = parts[parts.index("Issue") + 1] if "Issue" in parts else "—"
        pages = parts[parts.index("Article") + 1] if "Article" in parts else "—"

        # Аннотация
        abstract_tag = soup.find("div", class_="art-abstract in-tab")
        abstract = abstract_tag.get_text(strip=True) if abstract_tag else "Нет аннотации"

        # PDF-ссылка
        pdf_link = soup.find("a", string="Download PDF")
        pdf_url = "https://www.mdpi.com" + pdf_link["href"] if pdf_link else None

        return {
            "title": title,
            "authors": authors,
            "journal": journal,
            "issued": issued[:4],
            "volume": volume,
            "issue": issue,
            "pages": pages,
            "abstract": abstract,
            "conclusion": "—",
            "suggestions": "—",
            "pdf_url": pdf_url,
        }

    except Exception as e:
        return {"error": f"Ошибка парсинга MDPI: {e}"}
