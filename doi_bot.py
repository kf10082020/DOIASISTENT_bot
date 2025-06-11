import requests
from bs4 import BeautifulSoup
import re

# --- Основные методы ---

def fetch_metadata_crossref(doi):
    try:
        url = f"https://api.crossref.org/works/{doi}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()["message"]
    except Exception:
        return None

def fetch_metadata_pubmed(doi):
    try:
        query = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={doi}&retmode=json"
        r = requests.get(query, timeout=10)
        r.raise_for_status()
        pmid = r.json()["esearchresult"]["idlist"][0]

        fetch = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
        r = requests.get(fetch, timeout=10)
        soup = BeautifulSoup(r.content, "xml")
        return {
            "title": soup.find("ArticleTitle").text,
            "authors": [x.text for x in soup.find_all("LastName")],
            "journal": soup.find("Title").text,
            "issued": soup.find("PubDate").text,
            "abstract": soup.find("AbstractText").text
        }
    except Exception:
        return None

def fetch_metadata_html(doi_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(doi_url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        def meta(name):
            tag = soup.find("meta", {"name": name})
            return tag["content"] if tag else None

        return {
            "title": meta("citation_title"),
            "authors": meta("citation_author"),
            "journal": meta("citation_journal_title"),
            "issued": meta("citation_publication_date"),
            "volume": meta("citation_volume"),
            "issue": meta("citation_issue"),
            "pages": meta("citation_firstpage"),
            "abstract": meta("description"),
            "pdf_url": meta("citation_pdf_url")
        }
    except Exception:
        return None

def build_reply(data):
    if not data:
        return "❌ Не удалось извлечь метаданные."

    authors = ", ".join(data.get("authors", [])) if isinstance(data.get("authors"), list) else data.get("authors", "—")

    reply = f"📘 *Название:* {data.get('title', '—')}\n"
    reply += f"👨‍🔬 *Авторы:* {authors}\n"
    reply += f"📅 *Год:* {data.get('issued', '—')}\n"
    reply += f"📚 *Журнал:* {data.get('journal', '—')}\n"
    reply += f"📦 *Том:* {data.get('volume', '—')}\n"
    reply += f"📎 *Выпуск:* {data.get('issue', '—')}\n"
    reply += f"📄 *Страницы:* {data.get('pages', '—')}\n"
    reply += f"\n📝 *Аннотация:*\n{data.get('abstract', 'Нет аннотации')}\n"
    if data.get("pdf_url"):
        reply += f"\n📥 *PDF:* [Скачать PDF]({data['pdf_url']})\n"

    return reply

# --- Основной обработчик ---

def handle_doi(doi_url):
    doi = re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", doi_url, re.I)
    if not doi:
        return "❌ DOI не распознан."
    doi = doi[0]

    data = fetch_metadata_crossref(doi)
    if not data:
        data = fetch_metadata_pubmed(doi)
    if not data:
        data = fetch_metadata_html(doi_url)

    return build_reply(data)

# Пример вызова
if __name__ == "__main__":
    sample_doi = "https://doi.org/10.1080/10811680.2024.2384356"
    print(handle_doi(sample_doi))
