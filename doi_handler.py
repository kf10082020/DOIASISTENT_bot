import re
from sites_config import site_parsers

def extract_doi(text):
    """Извлекает DOI из текста сообщения"""
    match = re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.I)
    return match[0] if match else None

def identify_site_from_doi(doi):
    """Пытается определить сайт публикации по DOI"""
    for domain in site_parsers:
        if domain.split(".")[0] in doi:
            return domain
    return "crossref"  # fallback

def handle_doi(doi):
    """Основная функция обработки DOI"""
    domain = identify_site_from_doi(doi)
    parser = site_parsers.get(domain, site_parsers["search.crossref.org"])  # default fallback
    return parser(doi)
