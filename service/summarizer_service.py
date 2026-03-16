import httpx
import logging
from app.config import settings # 설정값 불러오기

logger = logging.getLogger(__name__)

class SummarizerService:
    async def summarize(self, text: str):
        if not settings.DIFY_API_KEY:
            logger.error("DIFY_API_KEY is missing!")
            return "API 설정 오류"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{settings.DIFY_API_URL}/completion",
                    headers={"Authorization": f"Bearer {settings.DIFY_API_KEY}"},
                    json={"inputs": {"news": text[:4000]}, "user": "jiwoo"}
                )
                response.raise_for_status()
                return response.json().get("answer", "요약 결과 없음")
            except Exception as e:
                logger.error(f"AI Server Error: {str(e)}")
                return "AI 요약 서비스 일시 중단"