from fastapi import APIRouter
from services.rss_service import get_news

router = APIRouter(prefix="/news", tags=["News"])

@router.get("")
async def list_news(keyword: str):
    try:
        data = await get_news(keyword)
        return {"status": "SUCCESS", "message": "뉴스 검색 성공", "data": data}
    except Exception as e:
        return {"status": "FAILURE", "message": str(e), "data": None}