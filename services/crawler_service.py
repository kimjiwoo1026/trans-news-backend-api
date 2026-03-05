import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Crawler:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def get_domain(self, url):
        return urlparse(url).netloc

    def fetch_html(self, url):
        response = requests.get(url, headers=self.headers, timeout=10)
        return response.text

    def extract_generic(self, soup):

        paragraphs = soup.find_all("p")

        text = []

        for p in paragraphs:
            t = p.get_text(strip=True)
            if len(t) > 30:
                text.append(t)

        if text:
            return "\n".join(text)

        return None

    def extract_naver(self, soup):

        div = soup.find("div", id="dic_area")

        if not div:
            return self.extract_generic(soup)

        paragraphs = div.find_all("p")

        text = []

        for p in paragraphs:
            t = p.get_text(strip=True)
            if len(t) > 10:
                text.append(t)

        if text:
            return "\n".join(text)

        return None

    def parse(self, html, domain):

        soup = BeautifulSoup(html, "html.parser")

        if "naver.com" in domain:
            return self.extract_naver(soup)

        return self.extract_generic(soup)

    def crawl_article(self, url):

        domain = self.get_domain(url)

        html = self.fetch_html(url)

        content = self.parse(html, domain)

        return content