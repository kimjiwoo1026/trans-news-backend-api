import feedparser
from urllib.parse import quote


def get_news(keyword: str):
    if not keyword or not keyword.strip():
        return []

    encoded_keyword = quote(keyword.strip())
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"

    feed = feedparser.parse(url)

    if getattr(feed, "bozo", 0):
        return []

    news_list = []

    for entry in feed.entries[:10]:
        news_list.append({
            "title": getattr(entry, "title", ""),
            "link": getattr(entry, "link", ""),
            "published": getattr(entry, "published", "")
        })

    return news_list