import feedparser


def get_news(keyword: str):

    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries:

        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })

    return articles