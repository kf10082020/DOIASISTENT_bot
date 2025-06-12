import requests
from bs4 import BeautifulSoup
import re
from parsers.sites_config import SITES

def fetch_metadata_crossref(doi):
    try:
        r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=10)
        r.raise_for_status()
        return r.json()["message"]
    except:
        return None

def fetch_metadata_html(doi_url):
    try:
        r = requests.get(doi_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        return {
            "title": soup.find("meta", {"name": "citation_title"})["content"],
            "authors": soup.find("meta", {"name": "citation_author"})["content"],
            "journal": soup.find("meta", {"name": "citation_journal_title"})["content"],
            "issued": soup.find("meta", {"name": "citation_publication_date"})["content"],
            "abstract": soup.find("meta", {"name": "description"})["content"],
        }
    except:
        return None

def handle_doi(doi_url):
    doi_match = re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", doi_url, re.I)
    if not doi_match:
        return {"error": "DOI не распознан."}
    doi = doi_match[0]

    data = fetch_metadata_crossref(doi)
    if not data:
        domain = requests.utils.urlparse(doi_url).netloc
        if domain in SITES:
            return SITES[domain](doi_url)
        data = fetch_metadata_html(doi_url)
    return data if data else {"error": "Не удалось извлечь данные."}
