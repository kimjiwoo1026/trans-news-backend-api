import requests
import time
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self):

        # HTTP 연결 재사용
        self.session = requests.Session()

        # 크롤링 차단 방지
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }


    def crawl_article(self, url: str):

        retry = 3   # 최대 3번 재시도

        for attempt in range(retry):

            try:

                res = self.session.get(
                    url,
                    headers=self.headers,
                    timeout=5
                )

                res.raise_for_status()

                soup = BeautifulSoup(res.text, "html.parser")

                paragraphs = soup.select("p")

                text = " ".join([p.get_text() for p in paragraphs])

                return text.strip()

            except Exception as e:

                print(f"Retry {attempt+1}/{retry} failed: {e}")

                time.sleep(1)   # 재시도 전 대기

        return None