import re
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup
from domain.player import Player
from domain.record import Record
from domain.enums import Enums
from domain.result_from_kishi import ResultFromKishi


def parse_enum(value: str, enum_class):
    for e in enum_class:
        if e.value in value:
            return e
    return list(enum_class)[-1]


def extract_title_and_danni(soup) -> tuple[list[Enums.Title], Optional[Enums.Danni]]:
    """
    タイトルと段位を取得して title, danni を返す
    """
    heading = soup.select_one("p.headingElementsA01.min.ico03")
    if not heading:
        return [], None

    text = heading.text.strip()

    title_values = [e.value for e in Enums.Title]

    # 判定
    if any(val in text for val in title_values):
        raw_titles = re.sub(r"[（）]", "・", text)
        title_list = [parse_enum(t, Enums.Title) for t in raw_titles.split("・") if t in title_values]
        return title_list, Enums.Danni.DAN9
    else:
        for danni_enum in Enums.Danni:
            if danni_enum.value in text:
                return [], danni_enum

    return [], None


def extract_record(soup: BeautifulSoup) -> Record:
    record_table = soup.select_one("h3:-soup-contains('棋士成績') + div table")
    record_rows = record_table.select("tr") if record_table else []

    wins = loses = consecutive_wins = total_ranking = consecutive_wins_ranking = wins_ranking = winning_rate_ranking = 0

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
        elif "対局数ランキング" in label:
            match = re.search(r"(\d+)位", text)
            if match:
                total_ranking = int(match.group(1))
        elif "連勝ランキング" in label:
            match = re.search(r"(\d+)位", text)
            if match:
                consecutive_wins_ranking = int(match.group(1))
            match = re.search(r"(\d+)連勝", text)
            if match:
                consecutive_wins = int(match.group(1))

    return Record(
        wins=wins,
        loses=loses,
        consecutive_wins=consecutive_wins,
        total_ranking=total_ranking,
        wins_ranking=wins_ranking,
        winning_rate_ranking=winning_rate_ranking,
        consecutive_wins_ranking=consecutive_wins_ranking,
    )


def normalize_match_date_list(raw: str) -> list[str]:
    dates = []

    # 一般形式：2025/5/29,30 など
    match = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})(?:,(\d{1,2})(?:/(\d{1,2}))?)?", raw)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day1 = int(match.group(3))
        day2 = match.group(4)
        month2 = match.group(5)

        # 最初の日付
        try:
            date1 = datetime(year, month, day1).strftime("%Y-%m-%d")
            dates.append(date1)
        except ValueError:
            pass  # 無効な日付はスキップ

        # 2日目があれば
        if day2:
            m2 = int(month2) if month2 else month  # 2日目の月が省略されている場合は同じ月
            try:
                date2 = datetime(year, m2, int(day2)).strftime("%Y-%m-%d")
                dates.append(date2)
            except ValueError:
                pass

        return dates

    # 単一日付形式：2025/6/18
    match = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})", raw)
    if match:
        try:
            date = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            return [date.strftime("%Y-%m-%d")]
        except ValueError:
            return []

    return [raw]


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
    match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", birth_date)
    if match:
        year, month, day = match.groups()
        birth_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
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
            opponent_link = cols[2].find("a")["href"] if cols[2].find("a") else None
            opponent_match = re.search(r"/player/pro/(\d+)\.html", opponent_link) if opponent_link else None
            opponent_number = int(opponent_match.group(1)) if opponent_match else None
            symbol = cols[1].text.strip()
            result_status = Enums.ResultStatus.from_symbol(symbol)

            a_tag = cols[3].find("a")
            if a_tag and a_tag.get("href"):
                category_symbol = a_tag["href"].strip("/").split("/")[-1]
                game_category = Enums.GameCategory.from_symbol(category_symbol)
            else:
                game_category = Enums.GameCategory.OTHER

            result_from_kishi.append(
                ResultFromKishi(
                    game_name=cols[3].text.strip(),
                    game_category=game_category,
                    opponent_number=opponent_number,
                    opponent_name=cols[2].text.strip(),
                    result_status=result_status,
                    date=normalize_match_date_list(cols[0].text.strip())
                )
            )
    print(name_kana)

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
        affiliation=Enums.Affiliation.NONE,
        playing_style=Enums.PlayingStyle.NONE,
        player_category=Enums.PlayerCategory.KISHI,
        is_active=True,
        result_from_kishi=result_from_kishi,
        record=extract_record(soup)
    )
