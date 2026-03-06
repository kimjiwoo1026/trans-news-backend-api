from fastapi import APIRouter
from services.crawler_service import Crawler
from services.summarizer_service import SummarizerService

router = APIRouter()

crawler = Crawler()
summarizer = SummarizerService()


@router.get("/news-summary")
def news_summary(url: str, model: str = "t5"):

    content = crawler.crawl_article(url)

    if not content:
        return {"error": "기사 본문 추출 실패"}

    summary = summarizer.summarize(content, model)

    return {
        "url": url,
        "model": model,
        "summary": summary
    }