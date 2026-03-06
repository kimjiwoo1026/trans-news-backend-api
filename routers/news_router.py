from fastapi import APIRouter
from services.rss_service import get_news
from services.crawler_service import Crawler

router = APIRouter()

crawler = Crawler()


@router.get("/news")
def news(keyword: str):
    return get_news(keyword)


@router.get("/article")
def article(url: str):

    content = crawler.crawl_article(url)

    if not content:
        return {"error": "기사 본문 추출 실패"}

    return {"content": content}