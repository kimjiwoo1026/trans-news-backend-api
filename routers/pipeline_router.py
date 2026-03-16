from fastapi import APIRouter
from services.crawler_service import Crawler
from services.summarizer_service import SummarizerService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pipeline", tags=["Pipeline"])
crawler = Crawler()
summarizer = SummarizerService()

@router.get("/news-summary")
async def news_summary_pipeline(url: str):
    try:
        # 1. 크롤링 (재시도 로직 포함)
        content = await crawler.crawl_article(url)
        if not content:
            return {"status": "FAILURE", "message": "기사 본문을 추출할 수 없습니다. (차단 혹은 구조 변경)", "data": None}
            
        # 2. 요약
        summary = await summarizer.summarize(content)
        
        return {
            "status": "SUCCESS", 
            "message": "분석 성공", 
            "data": {"url": url, "summary": summary}
        }
    except Exception as e:
        logger.critical(f"Unexpected Pipeline Error: {str(e)}")
        return {"status": "FAILURE", "message": "서버 내부 치명적 오류", "data": None}