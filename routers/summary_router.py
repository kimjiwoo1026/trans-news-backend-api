from fastapi import APIRouter
from services.summarizer_service import SummarizerService

router = APIRouter(prefix="/summary", tags=["Summary"])
summarizer = SummarizerService()

@router.post("")
async def summarize_text(text: str):
    # 민성 선배님 AI 서버 통한 요약
    summary = await summarizer.summarize(text)
    return {"status": "SUCCESS", "message": "요약 완료", "data": {"summary": summary}}