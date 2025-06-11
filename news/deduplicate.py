import re

def deduplicate_articles(article_lists):
    seen_urls = set()
    seen_titles = set()
    unique_articles = []

    def normalize(text):
        return re.sub(r'[^a-z0-9]', '', text.lower())

    for source in article_lists:
        for art in source:
            url = art.get("url", "").strip()
            title = normalize(art.get("title", "") or "")
            
            if not url or not title:
                continue
            
            if url in seen_urls or title in seen_titles:
                continue
            
            seen_urls.add(url)
            seen_titles.add(title)
            unique_articles.append(art)

    return unique_articles
