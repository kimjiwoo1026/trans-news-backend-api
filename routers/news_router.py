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

    return {"content": content}

from services.crawler_service import Crawler

crawler = Crawler()

@router.get("/article")
def article(url: str):

    content = crawler.crawl_article(url)

    return {"content": content}