import re
import time
import random
import logging
import requests
import urllib.robotparser

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logging.basicConfig(level=logging.INFO)


NOISE_PATTERNS = [
    "무단전재", "재배포", "기사제보", "구독", "바로가기", "Copyright"
]

MIN_P_LEN = 20


class Crawler:

    def __init__(self):

        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        retry = Retry(
            total=2,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retry)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)


    def _respect_rate_limit(self):
        time.sleep(random.uniform(0.8, 1.5))


    def _robots_allowed(self, url):

        parsed = urlparse(url)

        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        rp = urllib.robotparser.RobotFileParser()

        try:
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch(self.headers["User-Agent"], url)
        except:
            return True


    def fetch_html(self, url):

        if not self._robots_allowed(url):
            logging.warning(f"robots.txt blocked: {url}")
            return None

        try:

            self._respect_rate_limit()

            res = self.session.get(url, timeout=(3, 7))
            res.raise_for_status()

            return res.text

        except requests.RequestException as e:

            logging.error(f"request failed: {url} | {e}")

            return None


    def _clean_text(self, text):

        text = re.sub(r"\s+", " ", text)

        if any(noise in text for noise in NOISE_PATTERNS):
            return None

        return text.strip()


    def _extract_paragraphs(self, root):

        if not root:
            return []

        paragraphs = []

        for p in root.find_all("p"):

            txt = p.get_text(separator=" ", strip=True)

            if len(txt) < MIN_P_LEN:
                continue

            txt = self._clean_text(txt)

            if txt:
                paragraphs.append(txt)

        return paragraphs


    def _join(self, paragraphs):

        if not paragraphs:
            return "[ERROR] 본문 추출 실패"

        return "\n\n".join(paragraphs)


    def extract_naver(self, soup):

        root = soup.find("article") or soup.find("div", id="dic_area")

        return self._join(self._extract_paragraphs(root))


    def extract_daum(self, soup):

        root = soup.find("section", {"dmcf-ptype": "general"})

        return self._join(self._extract_paragraphs(root))


    def extract_chosun(self, soup):

        root = soup.find("div", class_="article-body") or soup.find("div", class_="par")

        return self._join(self._extract_paragraphs(root))


    def extract_generic(self, soup):

        candidates = []

        for node in soup.find_all(["article", "main", "section", "div"]):

            text_len = len(node.get_text(strip=True))

            if text_len > 500:
                candidates.append((text_len, node))

        if not candidates:
            return "[ERROR] 본문 추출 실패"

        candidates.sort(reverse=True)

        root = candidates[0][1]

        return self._join(self._extract_paragraphs(root))


    def parse(self, html, domain):

        soup = BeautifulSoup(html, "lxml")

        for br in soup.find_all("br"):
            br.replace_with("\n")

        parsers = {
            "naver.com": self.extract_naver,
            "daum.net": self.extract_daum,
            "chosun.com": self.extract_chosun
        }

        for key in parsers:

            if key in domain:
                return parsers[key](soup)

        return self.extract_generic(soup)


    def extract_article(self, url):

        domain = urlparse(url).netloc

        html = self.fetch_html(url)

        if not html:
            return "[ERROR] HTML 로딩 실패"

        return self.parse(html, domain)