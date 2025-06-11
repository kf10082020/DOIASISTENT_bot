import requests
from bs4 import BeautifulSoup
import re

def extract_doi(text):
    match = re.search(r"(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", text, re.I)
    return match.group(1) if match else None

def fetch_crossref(doi):
    try:
        res = requests.get(f"https://api.crossref.org/works/{doi}", timeout=10)
        res.raise_for_status()
        return res.json()["message"]
    except:
        return None

def fetch_pubmed(doi):
    try:
        base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        esearch = f"{base}/esearch.fcgi?db=pubmed&term={doi}&retmode=json"
        pmid = requests.get(esearch, timeout=10).json()["esearchresult"]["idlist"][0]

        efetch = f"{base}/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
        soup = BeautifulSoup(requests.get(efetch).content, "xml")

        return {
            "title": soup.findtext("ArticleTitle", default="—"),
            "authors": [x.text for x in soup.find_all("LastName")],
            "journal": soup.findtext("Title", default="—"),
            "issued": soup.findtext("PubDate", default="—"),
            "abstract": soup.findtext("AbstractText", default="Нет аннотации")
        }
    except:
        return None

def fetch_html_meta(doi_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        soup = BeautifulSoup(requests.get(doi_url, headers=headers, timeout=10).text, "html.parser")
        meta = lambda name: soup.find("meta", {"name": name})
        get = lambda name: meta(name)["content"] if meta(name) else None

        authors = soup.find_all("meta", {"name": "citation_author"})
        author_list = [a["content"] for a in authors] if authors else []

        return {
            "title": get("citation_title"),
            "authors": author_list,
            "journal": get("citation_journal_title"),
            "issued": get("citation_publication_date"),
            "volume": get("citation_volume"),
            "issue": get("citation_issue"),
            "pages": get("citation_firstpage"),
            "abstract": get("description") or "Нет аннотации",
            "pdf_url": get("citation_pdf_url")
        }
    except:
        return None

def build_reply(data):
    if not data:
        return "❌ Не удалось извлечь метаданные."

    authors = data.get("authors")
    if isinstance(authors, list):
        authors = ', '.join(authors)
    authors = authors or "—"

    fields = [
        f"📘 *Название:* {data.get('title', '—')}",
        f"👨‍🔬 *Авторы:* {authors}",
        f"📅 *Год:* {data.get('issued', '—')}",
        f"📚 *Журнал:* {data.get('journal', '—')}",
        f"📦 *Том:* {data.get('volume', '—')}",
        f"📎 *Выпуск:* {data.get('issue', '—')}",
        f"📄 *Страницы:* {data.get('pages', '—')}",
        f"\n📝 *Аннотация:*\n{data.get('abstract', 'Нет аннотации')}"
    ]

    if data.get("pdf_url"):
        fields.append(f"\n📥 *PDF:* [Скачать PDF]({data['pdf_url']})")

    return "\n".join(fields)

def handle_doi(doi_url):
    doi = extract_doi(doi_url)
    if not doi:
        return "❌ DOI не распознан."

    for fetcher in [fetch_crossref, fetch_pubmed, lambda _: fetch_html_meta(doi_url)]:
        data = fetcher(doi)
        if data:
            return build_reply(data)

    return "❌ Не удалось получить данные ни с одного источника."


# === Тест ===
if __name__ == "__main__":
    test_doi = "https://doi.org/10.1080/10811680.2024.2384356"
    print(handle_doi(test_doi))
