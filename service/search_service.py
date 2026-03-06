import requests


def search_news(keyword: str):

    url = f"https://news.google.com/search?q={keyword}"

    res = requests.get(url)

    if res.status_code != 200:
        return []

    return res.text