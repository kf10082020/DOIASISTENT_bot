def parse_mdpi(url):
    return {"title": "MDPI parser (заглушка)", "authors": "—", "journal": "MDPI", "issued": "—"}

def parse_springer(url):
    return {"title": "Springer parser (заглушка)", "authors": "—", "journal": "Springer", "issued": "—"}

SITES = {
    "www.mdpi.com": parse_mdpi,
    "link.springer.com": parse_springer
}
