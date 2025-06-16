import re

def extract_doi(text):
    """Извлекает DOI из текста сообщения"""
    match = re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.I)
    return match[0] if match else None
