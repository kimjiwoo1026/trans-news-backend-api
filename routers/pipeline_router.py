from fastapi import APIRouter
from services.crawler_service import Crawler
from services.summarizer_service import summarize_text

router = APIRouter()

crawler = Crawler()

@router.get("/news-summary")
def news_summary(url: str):

    content = crawler.crawl_article(url)

    if not content:
        return {"error": "기사 본문 추출 실패"}

    summary = summarize_text(content)

    return {
        "url": url,
        "content": content[:500],
        "summary": summary
    }