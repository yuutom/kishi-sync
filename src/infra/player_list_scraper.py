import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.shogi.or.jp"


def extract_active_kishi_urls_from_list_page() -> list[str]:
    # 棋士リストの取得
    res = requests.get("https://www.shogi.or.jp/player/")
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    urls = []

    for a_tag in soup.select(f"a[href^='/player/pro/']"):
        href = a_tag.get("href")
        if href.endswith(".html"):
            full_url = BASE_URL + href
            urls.append(full_url)

    # 女流棋士リストの取得
    res = requests.get("https://www.shogi.or.jp/player/lady.html")
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    for a_tag in soup.select(f"a[href^='/player/lady/']"):
        href = a_tag.get("href")
        if href.endswith(".html"):
            full_url = BASE_URL + href
            urls.append(full_url)

    return list(set(urls))
