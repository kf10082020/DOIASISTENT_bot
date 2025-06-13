from doi_bot import fetch_metadata_html  

# Парсеры для различных источников публикаций  
def parse_mdpi(url):   
    return fetch_metadata_html(url)  

def parse_springer(url):   
    return {"title": "Springer parser", "authors": "—", "journal": "Springer", "issued": "—"}  

def parse_sciencedirect(url):   
    return {"title": "Sciencedirect parser", "authors": "—", "journal": "Sciencedirect", "issued": "—"}  

def parse_sagepub(url):   
    return {"title": "Sagepub parser", "authors": "—", "journal": "Sagepub", "issued": "—"}  

def parse_tandfonline(url):   
    return {"title": "Tandfonline parser", "authors": "—", "journal": "Tandfonline", "issued": "—"}  

def parse_bmcmedicine(url):   
    return {"title": "Bmcmedicine parser", "authors": "—", "journal": "Bmcmedicine", "issued": "—"}  

def parse_frontiersin(url):   
    return {"title": "Frontiersin parser", "authors": "—", "journal": "Frontiersin", "issued": "—"}  

def parse_routledge(url):   
    return {"title": "Routledge parser", "authors": "—", "journal": "Routledge", "issued": "—"}  

def parse_wiley(url):   
    return {"title": "wiley parser", "authors": "—", "journal": "wiley", "issued": "—"}  

def parse_jstor(url):   
    return {"title": "jstor parser", "authors": "—", "journal": "jstor", "issued": "—"}  

def parse_muse(url):   
    return {"title": "Muse parser", "authors": "—", "journal": "Muse", "issued": "—"}  

def parse_crossref(url):   
    return {"title": "crossref parser", "authors": "—", "journal": "crossref", "issued": "—"}  

def parse_scholar(url):   
    return {"title": "scholar parser", "authors": "—", "journal": "scholar", "issued": "—"}  

def parse_doaj(url):   
    return {"title": "Doaj parser", "authors": "—", "journal": "Doaj", "issued": "—"}  

def parse_pubmed(url):   
    return {"title": "Pubmed parser", "authors": "—", "journal": "Pubmed", "issued": "—"}  

def parse_ijirmf(url):   
    return {"title": "Ijirmf parser", "authors": "—", "journal": "Ijirmf", "issued": "—"}  

def parse_eric(url):   
    return {"title": "Eric parser", "authors": "—", "journal": "Eric", "issued": "—"}  

def parse_ieee(url):   
    return {"title": "Ieee parser", "authors": "—", "journal": "Ieee", "issued": "—"}  

def parse_acm(url):   
    return {"title": "acm parser", "authors": "—", "journal": "acm", "issued": "—"}  

def parse_ssrn(url):   
    return {"title": "ssrn parser", "authors": "—", "journal": "ssrn", "issued": "—"}  

# Словарь с соответствием доменных имен и функций парсинга  
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
