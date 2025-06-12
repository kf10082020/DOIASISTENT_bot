def parse_mdpi(url):
    return {"title": "MDPI parser (заглушка)", "authors": "—", "journal": "MDPI", "issued": "—"}

def parse_springer(url):
    return {"title": "Springer parser (заглушка)", "authors": "—", "journal": "Springer", "issued": "—"}

def parse_sciencedirect(url):
    return {"title": "Sciencedirect parser (заглушка)", "authors": "—", "journal": "Sciencedirect", "issued": "—"}

def parse_sagepub(url):
    return {"title": "Sagepub parser (заглушка)", "authors": "—", "journal": "Sagepub", "issued": "—"}

def parse_tandfonline(url):
    return {"title": "Tandfonline parser (заглушка)", "authors": "—", "journal": "Tandfonline", "issued": "—"}

def parse_bmcmedicine(url):
    return {"title": "Bmcmedicine parser (заглушка)", "authors": "—", "journal": "Bmcmedicine", "issued": "—"}

def parse_frontiersin(url):
    return {"title": "Frontiersin parser (заглушка)", "authors": "—", "journal": "Frontiersin", "issued": "—"}

def parse_routledge(url):
    return {"title": "Routledge parser (заглушка)", "authors": "—", "journal": "Routledge", "issued": "—"}

def parse_wiley(url):
    return {"title": "wiley parser (заглушка)", "authors": "—", "journal": "wiley", "issued": "—"}

def parse_jstor(url):
    return {"title": "jstor parser (заглушка)", "authors": "—", "journal": "jstor", "issued": "—"}

def parse_muse(url):
    return {"title": "Muse parser (заглушка)", "authors": "—", "journal": "Muse", "issued": "—"}

def parse_crossref(url):
    return {"title": "crossref parser (заглушка)", "authors": "—", "journal": "crossref", "issued": "—"}

def parse_scholar(url):
    return {"title": "scholar parser (заглушка)", "authors": "—", "journal": "scholar", "issued": "—"}

def parse_doaj(url):
    return {"title": "Doaj parser (заглушка)", "authors": "—", "journal": "Doaj", "issued": "—"}

def parse_pubmed(url):
    return {"title": "Pubmed parser (заглушка)", "authors": "—", "journal": "Pubmed", "issued": "—"}

def parse_ijirmf(url):
    return {"title": "Ijirmf parser (заглушка)", "authors": "—", "journal": "Ijirmf", "issued": "—"}

def parse_eric(url):
    return {"title": "Eric parser (заглушка)", "authors": "—", "journal": "Eric", "issued": "—"}

def parse_ieee(url):
    return {"title": "Ieee parser (заглушка)", "authors": "—", "journal": "Ieee", "issued": "—"}

def parse_acm(url):
    return {"title": "acm parser (заглушка)", "authors": "—", "journal": "acm", "issued": "—"}

def parse_ssrn(url):
    return {"title": "ssrn parser (заглушка)", "authors": "—", "journal": "ssrn", "issued": "—"}


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
