import re
import unicodedata

import requests
from bs4 import BeautifulSoup
from domain.player import Player
from domain.enums import Enums
from infra.wikipedia_scraper import parse_wikipedia_detail


def parse_enum(value: str, enum_class):
    normalized_value = unicodedata.normalize("NFKC", value)

    matched = []
    for e in enum_class:
        enum_value = unicodedata.normalize("NFKC", e.value)
        index = normalized_value.find(enum_value)
        if index != -1:
            matched.append((index, e))

    if matched:
        return sorted(matched, key=lambda x: x[0])[0][1]

    return list(enum_class)[-1]


def extract_title(soup) -> list[Enums.Title]:
    """
    タイトルと段位を取得して title, danni を返す
    """
    heading = soup.select_one("p.headingElementsA01.min.ico03")
    if not heading:
        return []

    text = heading.text.strip()

    title_values = [e.value for e in Enums.Title]

    # 判定
    if any(val in text for val in title_values):
        raw_titles = re.sub(r"[（）]", "・", text)
        title_list = [parse_enum(t, Enums.Title) for t in raw_titles.split("・") if t in title_values]
        return title_list

    return []


def parse_kishi_detail(url: str) -> Player:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    # 名前
    name_kana = soup.select_one("span.jp").text.strip()
    name_rome = soup.select_one("span.en").text.strip()

    # 各種情報取得
    def find_td(th_text):
        th = soup.find("th", string=th_text)
        return th.find_next("td").text.strip() if th else ""

    kishi_number = int(find_td("棋士番号"))
    birth_date = find_td("生年月日")
    match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", birth_date)
    if match:
        year, month, day = match.groups()
        birth_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    birth_place = find_td("出身地")
    master = find_td("師匠")
    ryuohsen_text = find_td("竜王戦")
    junisen_text = find_td("順位戦")

    title = extract_title(soup)

    # 画像URL
    image_tag = soup.select_one("figure.image img")
    image_url = "https://www.shogi.or.jp" + image_tag["src"] if image_tag else ""

    debut_date, affiliation, danni = parse_wikipedia_detail(f"https://ja.wikipedia.org/wiki/{name_kana}")

    return Player(
        id=f"pro_{kishi_number}",
        kishi_number=kishi_number,
        nameKana=name_kana,
        nameRome=name_rome,
        image_url=image_url,
        birth_date=birth_date,
        debut_date=debut_date,
        birth_place=birth_place,
        master=master,
        ryuohsen=ryuohsen_text,
        junisen=junisen_text,
        ryuohsen_class=parse_enum(ryuohsen_text, Enums.RyuohsenClass),
        junisen_class=parse_enum(junisen_text, Enums.JunisenClass),
        danni=danni,
        title=title,
        affiliation=affiliation,
        player_category=Enums.PlayerCategory.KISHI,
        is_active=True,
    )
