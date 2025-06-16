def parse_springer(url):
    """Реальный парсер для Springer"""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            "title": soup.find('h1', {'class': 'c-article-title'}).text.strip(),
            "authors": [a.text.strip() for a in soup.select('.c-article-author-list__item a')],
            "journal": soup.find('a', {'data-test': 'journal-title'}).text.strip(),
            "issued": soup.find('time')['datetime'].split('-')[0],
            "volume": soup.find('b', {'data-test': 'journal-volume'}).text.strip(),
            "issue": soup.find('b', {'data-test': 'journal-issue'}).text.strip(),
            "pages": soup.find('span', {'data-test': 'article-page-range'}).text.strip(),
            "abstract": soup.find('section', {'id': 'Abs1'}).text.strip(),
            "pdf_url": f"https://link.springer.com{soup.find('a', {'data-test': 'pdf-link'})['href']}",
            "doi": url.split('doi.org/')[-1],
            "url": url
        }
    except Exception as e:
        print(f"Springer parser error: {e}")
        return get_placeholder("Springer")(url)
