import httpx
import logging
import asyncio
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}

    async def crawl_article(self, url: str, retries: int = 3):
        async with httpx.AsyncClient(timeout=10.0) as client:
            for attempt in range(retries):
                try:
                    logger.info(f"[{attempt+1}/{retries}] Crawling: {url}")
                    res = await client.get(url, headers=self.headers)
                    res.raise_for_status()
                    
                    soup = BeautifulSoup(res.text, "html.parser")
                    # 본문 영역 정밀 타겟팅
                    article = soup.find('article') or soup.find('div', id='articleBodyContents')
                    content = " ".join([p.get_text() for p in article.find_all('p')]) if article else ""
                    
                    if len(content) > 100:
                        return content.strip()
                    
                except Exception as e:
                    logger.warning(f"Attempt {attempt+1} failed: {str(e)}")
                    if attempt < retries - 1:
                        await asyncio.sleep(1) # 재시도 전 대기
            
            logger.error(f"Final crawl failure for {url}")
            return None