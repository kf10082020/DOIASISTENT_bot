def get_placeholder(name):
    return f"{name} parser"

def parse_mdpi(url): return {"title": get_placeholder("MDPI"), "authors": "—", "journal": "MDPI", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_springer(url): return {"title": get_placeholder("Springer"), "authors": "—", "journal": "Springer", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_sciencedirect(url): return {"title": get_placeholder("Sciencedirect"), "authors": "—", "journal": "Sciencedirect", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_sagepub(url): return {"title": get_placeholder("Sagepub"), "authors": "—", "journal": "Sagepub", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_tandfonline(url): return {"title": get_placeholder("Tandfonline"), "authors": "—", "journal": "Tandfonline", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_bmcmedicine(url): return {"title": get_placeholder("Bmcmedicine"), "authors": "—", "journal": "Bmcmedicine", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_frontiersin(url): return {"title": get_placeholder("Frontiersin"), "authors": "—", "journal": "Frontiersin", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_routledge(url): return {"title": get_placeholder("Routledge"), "authors": "—", "journal": "Routledge", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_wiley(url): return {"title": get_placeholder("Wiley"), "authors": "—", "journal": "Wiley", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_jstor(url): return {"title": get_placeholder("Jstor"), "authors": "—", "journal": "Jstor", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_muse(url): return {"title": get_placeholder("Muse"), "authors": "—", "journal": "Muse", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_crossref(url): return {"title": get_placeholder("Crossref"), "authors": "—", "journal": "Crossref", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_scholar(url): return {"title": get_placeholder("Scholar"), "authors": "—", "journal": "Scholar", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_doaj(url): return {"title": get_placeholder("Doaj"), "authors": "—", "journal": "Doaj", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_pubmed(url): return {"title": get_placeholder("Pubmed"), "authors": "—", "journal": "Pubmed", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_ijirmf(url): return {"title": get_placeholder("Ijirmf"), "authors": "—", "journal": "Ijirmf", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_eric(url): return {"title": get_placeholder("Eric"), "authors": "—", "journal": "Eric", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_ieee(url): return {"title": get_placeholder("IEEE"), "authors": "—", "journal": "IEEE", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_acm(url): return {"title": get_placeholder("ACM"), "authors": "—", "journal": "ACM", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}
def parse_ssrn(url): return {"title": get_placeholder("SSRN"), "authors": "—", "journal": "SSRN", "issued": "—", "volume": "—", "issue": "—", "pages": "—", "abstract": "—", "conclusion": "—", "suggestions": "—", "pdf_url": "—", "doi": "—", "url": url}

SITES = {
    "www.mdpi.com": parse_mdpi,
    "link.springer.com": parse_springer,
    "www.sciencedirect.com": parse_sciencedirect,
    "journals.sagepub.com": parse_sagepub,
    "www.tandfonline.com": parse_tandfonline,
    "bmcmedicine.biomedcentral.com": parse_bmcmedicine,
    "www.frontiersin.org": parse_frontiersin,
    "www.routledge.com": parse_routledge,
    "onlinelibrary.wiley.com": parse_wiley,
    "www.jstor.org": parse_jstor,
    "muse.jhu.edu": parse_muse,
    "search.crossref.org": parse_crossref,
    "scholar.google.com": parse_scholar,
    "doaj.org": parse_doaj,
    "pubmed.ncbi.nlm.nih.gov": parse_pubmed,
    "www.ijirmf.com": parse_ijirmf,
    "eric.ed.gov": parse_eric,
    "ieeexplore.ieee.org": parse_ieee,
    "dl.acm.org": parse_acm,
    "www.ssrn.com": parse_ssrn,      
}
