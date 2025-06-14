def get_placeholder(name):
    return f"{name} parser"

def create_parser_journal(journal_name):
    def parser(url):
        return {
            "title": get_placeholder(journal_name),
            "authors": "—",
            "journal": journal_name,
            "issued": "—",
            "volume": "—",
            "issue": "—",
            "pages": "—",
            "abstract": "—",
            "conclusion": "—",
            "suggestions": "—",
            "pdf_url": "—",
            "doi": "—",
            "url": url
        }
    return parser

# Создаем словарь сайтов и их соответствующих парсеров
SITES = {
    "www.mdpi.com": create_parser_journal("MDPI"),
    "link.springer.com": create_parser_journal("Springer"),
    "www.sciencedirect.com": create_parser_journal("Sciencedirect"),
    "journals.sagepub.com": create_parser_journal("Sagepub"),
    "www.tandfonline.com": create_parser_journal("Tandfonline"),
    "bmcmedicine.biomedcentral.com": create_parser_journal("Bmcmedicine"),
    "www.frontiersin.org": create_parser_journal("Frontiersin"),
    "www.routledge.com": create_parser_journal("Routledge"),
    "onlinelibrary.wiley.com": create_parser_journal("Wiley"),
    "www.jstor.org": create_parser_journal("Jstor"),
    "muse.jhu.edu": create_parser_journal("Muse"),
    "search.crossref.org": create_parser_journal("Crossref"),
    "scholar.google.com": create_parser_journal("Scholar"),
    "doaj.org": create_parser_journal("Doaj"),
    "pubmed.ncbi.nlm.nih.gov": create_parser_journal("Pubmed"),
    "www.ijirmf.com": create_parser_journal("Ijirmf"),
    "eric.ed.gov": create_parser_journal("Eric"),
    "ieeexplore.ieee.org": create_parser_journal("IEEE"),
    "dl.acm.org": create_parser_journal("ACM"),
    "www.ssrn.com": create_parser_journal("SSRN")
}
