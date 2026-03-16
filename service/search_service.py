import feedparser
import httpx

async def get_news(keyword: str):
    # RSS와 검색을 통합하여 비동기로 수집
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        feed = feedparser.parse(res.text)
        return [{"title": e.title, "link": e.link, "date": e.published} for e in feed.entries[:10]]