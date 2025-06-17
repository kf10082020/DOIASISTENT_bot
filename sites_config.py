import requests

# Универсальный парсер через Crossref API
def fetch_meta_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()["message"]

        return {
            "title": data.get("title", ["—"])[0],
            "authors": ", ".join([f'{a.get("given", "")} {a.get("family", "")}' for a in data.get("author", [])]),
            "journal": data.get("container-title", ["—"])[0],
            "issued": str(data.get("issued", {}).get("date-parts", [[None]])[0][0]),
            "volume": data.get("volume", "—"),
            "issue": data.get("issue", "—"),
            "pages": data.get("page", "—"),
            "abstract": data.get("abstract", "Нет аннотации"),
            "doi": data.get("DOI", doi),
            "source": "crossref"
        }
    except Exception as e:
        print(f"❌ Ошибка получения метаданных: {e}")
        return {"title": "—", "authors": "—", "journal": "—", "issued": "—"}

# Подключаем API-парсеры (все используют Crossref как базу)
def parse_mdpi(doi): return fetch_meta_crossref(doi)
def parse_springer(doi): return fetch_meta_crossref(doi)
def parse_sciencedirect(doi): return fetch_meta_crossref(doi)
def parse_sagepub(doi): return fetch_meta_crossref(doi)
def parse_tandfonline(doi): return fetch_meta_crossref(doi)
def parse_bmcmedicine(doi): return fetch_meta_crossref(doi)
def parse_frontiersin(doi): return fetch_meta_crossref(doi)
def parse_wiley(doi): return fetch_meta_crossref(doi)
def parse_pubmed(doi): return fetch_meta_crossref(doi)
def parse_ieee(doi): return fetch_meta_crossref(doi)
def parse_acm(doi): return fetch_meta_crossref(doi)
def parse_ssrn(doi): return fetch_meta_crossref(doi)
def parse_crossref(doi): return fetch_meta_crossref(doi)
def parse_doaj(doi): return fetch_meta_crossref(doi)

# Соответствие доменов и функций
site_parsers = {
    "www.mdpi.com": parse_mdpi,
    "link.springer.com": parse_springer,
    "www.sciencedirect.com": parse_sciencedirect,
    "journals.sagepub.com": parse_sagepub,
    "www.tandfonline.com": parse_tandfonline,
    "bmcmedicine.biomedcentral.com": parse_bmcmedicine,
    "www.frontiersin.org": parse_frontiersin,
    "onlinelibrary.wiley.com": parse_wiley,
    "pubmed.ncbi.nlm.nih.gov": parse_pubmed,
    "ieeexplore.ieee.org": parse_ieee,
    "dl.acm.org": parse_acm,
    "www.ssrn.com": parse_ssrn,
    "search.crossref.org": parse_crossref,
    "doaj.org": parse_doaj
}
