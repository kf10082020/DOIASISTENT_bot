import re

def extract_doi(text: str) -> str or None:
    # Простая регулярка для DOI (можно улучшить)
    pattern = r"10.\d{4,9}/[-._;()/:A-Z0-9]+"
    matches = re.findall(pattern, text, flags=re.I)
    return matches[0] if matches else None
