from typing import Optional, re

import requests
from bs4 import BeautifulSoup
from domain.player import Player
from domain.record import Record
from domain.enums import Enums


def parse_enum(value: str, enum_class):
    for e in enum_class:
        if e.value in value:
            return e
    return list(enum_class)[-1]  # デフォルト（OTHERやUNKNOWN）


def extract_title_and_danni(soup) -> tuple[list[str], Optional[Enums.Danni]]:
    """
    タイトルと段位を取得して title, danni を返す
    """
    heading = soup.select_one("p.headingElementsA01.min.ico03")
    if not heading:
        return [], None

    text = heading.text.strip()

    # 判定
    if any(title in text for title in Enums.Title):
        import re
        raw_titles = re.sub(r"[（）]", "・", text)  # 丸括弧を区切りに変換
        title_list = [t for t in raw_titles.split("・") if t in Enums.Title]
        return title_list, Enums.Danni.DAN9
    else:
        for label, enum_val in Enums.Title:
            if enum_val in text:
                return [], enum_val

    return [], None


def extract_record(soup: BeautifulSoup) -> Record:
    record_table = soup.select_one("h3:-soup-contains('棋士成績') + div table")
    record_rows = record_table.select("tr") if record_table else []

    wins = loses = total_ranking = wins_ranking = winning_rate_ranking = 0

    for row in record_rows:
        th = row.find("th")
        td = row.find("td")
        if not th or not td:
            continue
        label = th.text.strip()
        text = td.text.strip()

        if "今年度成績" in label:
            match = re.search(r"(\d+)勝(\d+)敗", text)
            if match:
                wins = int(match.group(1))
                loses = int(match.group(2))
        elif "勝数ランキング" in label:
            match = re.search(r"(\d+)位", text)
            if match:
                wins_ranking = int(match.group(1))
        elif "勝率ランキング" in label:
            match = re.search(r"(\d+)位", text)
            if match:
                winning_rate_ranking = int(match.group(1))
        elif "連勝ランキング" in label:
            match = re.search(r"(\d+)位", text)
            if match:
                winning_rate_ranking = int(match.group(1))


    return Record(
        wins=wins,
        loses=loses,
        total_ranking=wins + loses,
        wins_ranking=wins_ranking,
        winning_rate_ranking=winning_rate_ranking
    )



def parse_player_detail(url: str) -> Player:
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
    birth_place = find_td("出身地")
    master = find_td("師匠")
    ryuohsen_text = find_td("竜王戦")
    junisen_text = find_td("順位戦")

    title, danni = extract_title_and_danni(soup)

    # 画像URL
    image_tag = soup.select_one("figure.image img")
    image_url = "https://www.shogi.or.jp" + image_tag["src"] if image_tag else ""

    # 対局結果
    result_rows = soup.select("table.tableElements02.tableElements03 tr")[1:]
    result_from_kishi = []
    for row in result_rows:
        cols = row.find_all("td")
        if len(cols) == 4:
            result_from_kishi.append({
                "date": cols[0].text.strip(),
                "result": cols[1].text.strip(),
                "opponent": cols[2].text.strip(),
                "match": cols[3].text.strip(),
            })

    return Player(
        id=kishi_number,
        kishi_number=kishi_number,
        nameKana=name_kana,
        nameRome=name_rome,
        image_url=image_url,
        birth_date=birth_date,
        debut_date=None,
        birth_place=birth_place,
        master=master,
        ryuohsen=ryuohsen_text,
        junisen=junisen_text,
        ryuohsen_class=parse_enum(ryuohsen_text, Enums.RyuohsenClass),
        junisen_class=parse_enum(junisen_text, Enums.JunisenClass),
        danni=danni,
        title=title,
        affiliation=None,
        playing_style=None,
        player_category=Enums.PlayerCategory.KISHI,
        is_active=True,
        result_from_kishi=result_from_kishi,
        record=Record()
    )
