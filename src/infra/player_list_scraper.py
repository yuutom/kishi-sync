import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.shogi.or.jp"


def extract_active_kishi_urls_from_list_page(symbol: str) -> list[str]:
    res = requests.get("https://www.shogi.or.jp/player/lady.html")
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    urls = []

    for a_tag in soup.select(f"a[href^='/player/{symbol}/']"):
        href = a_tag.get("href")
        if href.endswith(".html"):
            full_url = BASE_URL + href
            urls.append(full_url)

    return list(set(urls))
