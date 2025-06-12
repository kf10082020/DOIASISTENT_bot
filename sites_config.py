def parse_mdpi(url):
    return {"title": "MDPI parser (заглушка)", "authors": "—", "journal": "MDPI", "issued": "—"}

def parse_springer(url):
    return {"title": "Springer parser (заглушка)", "authors": "—", "journal": "Springer", "issued": "—"}

def parse_springer(url):
    return {"title": "Sciencedirect parser (заглушка)", "authors": "—", "journal": "Sciencedirect", "issued": "—"}

def parse_springer(url):
    return {"title": "journals.sagepub parser (заглушка)", "authors": "—", "journal": "journals.sagepub", "issued": "—"}

def parse_springer(url):
    return {"title": "tandfonline parser (заглушка)", "authors": "—", "journal": "tandfonline", "issued": "—"}

def parse_springer(url):
    return {"title": "bmcmedicine.biomedcentral parser (заглушка)", "authors": "—", "journal": "bmcmedicine.biomedcentral", "issued": "—"}

def parse_springer(url):
    return {"title": "frontiersin parser (заглушка)", "authors": "—", "journal": "frontiersin", "issued": "—"}

def parse_springer(url):
    return {"title": "routledge parser (заглушка)", "authors": "—", "journal": "routledge", "issued": "—"}

def parse_springer(url):
    return {"title": "onlinelibrary.wiley parser (заглушка)", "authors": "—", "journal": "onlinelibrary.wiley", "issued": "—"}

def parse_springer(url):
    return {"title": "jstor parser (заглушка)", "authors": "—", "journal": "jstor", "issued": "—"}

def parse_springer(url):
    return {"title": "muse.jhu parser (заглушка)", "authors": "—", "journal": "muse.jhu", "issued": "—"}

def parse_springer(url):
    return {"title": "search.crossref parser (заглушка)", "authors": "—", "journal": "search.crossref", "issued": "—"}

def parse_springer(url):
    return {"title": "scholar.google parser (заглушка)", "authors": "—", "journal": "scholar.google", "issued": "—"}

def parse_springer(url):
    return {"title": "doaj.org parser (заглушка)", "authors": "—", "journal": "doaj.org", "issued": "—"}

def parse_springer(url):
    return {"title": "pubmed.ncbi.nlm.nih parser (заглушка)", "authors": "—", "journal": "pubmed.ncbi.nlm.nih", "issued": "—"}

def parse_springer(url):
    return {"title": "ijirmf parser (заглушка)", "authors": "—", "journal": "ijirmf", "issued": "—"}

def parse_springer(url):
    return {"title": "ieeexplore.ieee parser (заглушка)", "authors": "—", "journal": "ieeexplore.ieee", "issued": "—"}

def parse_springer(url):
    return {"title": "dl.acm parser (заглушка)", "authors": "—", "journal": "dl.acm", "issued": "—"}

def parse_springer(url):
    return {"title": "ssrn.com parser (заглушка)", "authors": "—", "journal": "ssrn.com", "issued": "—"}




SITES = {
    "www.mdpi.com": parse_mdpi,
    "link.springer.com": parse_springer,
    "www.sciencedirect.com": parse_sciencedirect,
    "journals.sagepub.com": parse_journals.sagepub,
    "www.tandfonline.com": parse_tandfonline,
    "bmcmedicine.biomedcentral.com": parse_bmcmedicine.biomedcentral,
    "www.frontiersin.org": parse_frontiersin,
    "www.routledge.com": parse_routledge,
    "onlinelibrary.wiley.com": parse_onlinelibrary.wiley,
    "www.jstor.org": parse_jstor,
    "muse.jhu.edu": parse_muse.jhu,
    "search.crossref.org": parse_search.crossref,
    "scholar.google.com": parse_scholar.google,
    "doaj.org": parse_doaj,
    "pubmed.ncbi.nlm.nih.gov": parse_pubmed.ncbi.nlm.nih.gov,
    "www.ijirmf.com": parse_ijirmf,
    "eric.ed.gov": parse_eric.ed,
    "ieeexplore.ieee.org": parse_ieeexplore.ieee,
    "dl.acm.org": parse_dl.acm,
    "www.ssrn.com": parse_www.ssrn,      
}
