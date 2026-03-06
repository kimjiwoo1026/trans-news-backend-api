import requests
from bs4 import BeautifulSoup


class Crawler:

    def crawl_article(self, url: str):

        try:
            res = requests.get(url)
            res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")

            paragraphs = soup.select("p")

            text = " ".join([p.get_text() for p in paragraphs])

            return text.strip()

        except Exception as e:
            print(f"Crawling error: {e}")
            return None