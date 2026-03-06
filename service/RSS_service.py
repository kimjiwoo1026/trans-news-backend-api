import feedparser


def get_news(keyword: str):

    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"

    feed = feedparser.parse(url)

    news_list = []

    for entry in feed.entries[:10]:
        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })

    return news_list