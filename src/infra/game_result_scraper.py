import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from domain.enums import Enums
from domain.game import Game


def extract_year_month(soup: BeautifulSoup) -> tuple[int, int]:
    heading = soup.find("h2", class_="headingElementsA01")
    if heading:
        m = re.search(r"(\d{4})年(\d{1,2})月", heading.text)
        if m:
            return int(m.group(1)), int(m.group(2))
    raise ValueError("年・月の情報を取得できませんでした。")


def parse_dates_with_context(year: int, month: int, text: str) -> list[str]:
    """
    例: "1月7・8日" → ["2024-01-07", "2024-01-08"]
    """
    text = text.replace("（", "").replace("）", "")
    m = re.search(r"\d+月([\d・]+)日", text)
    if not m:
        return []
    days = m.group(1).split("・")
    return [
        datetime(year, month, int(day)).strftime("%Y-%m-%d")
        for day in days if day.isdigit()
    ]


def parse_game_result(url: str) -> List[Game]:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    year, month = extract_year_month(soup)
    table = soup.select_one("table.tableElements01")
    rows = table.find_all("tr")

    games = []
    current_date = None
    game_id = 1

    for row in rows:
        cols = row.find_all("td")

        if len(cols) == 1 and "月" in cols[0].text:
            date_text = cols[0].text.strip()
            current_date = parse_dates_with_context(year, month, date_text)
            continue

        # 通常の対局行（6列）
        if len(cols) != 6:
            continue

        game_name = cols[0].get_text(strip=True)
        sente_player_name = cols[2].get_text(strip=True)
        gote_player_name = cols[3].get_text(strip=True)
        a_tag = cols[0].find("a")
        if a_tag and a_tag.get("href"):
            category_symbol = a_tag["href"].strip("/").split("/")[-1]
            game_category = Enums.GameCategory.from_symbol(category_symbol)
        else:
            game_category = Enums.GameCategory.OTHER

        # 結果記号（○ ●など）
        sente_result = Enums.ResultStatus.from_symbol(cols[1].get_text(strip=True))
        gote_result = Enums.ResultStatus.from_symbol(cols[4].get_text(strip=True))

        # プレイヤー番号とカテゴリ
        def extract_player_info(a_tag):
            if not a_tag or not a_tag.get("href"):
                return -1, Enums.PlayerCategory.OTHER
            href = a_tag["href"]
            match = re.search(r"/player/(pro|lady)/(\d+)\.html", href)
            if match:
                category = Enums.PlayerCategory.from_symbol(match.group(1))
                number = int(match.group(2))
                return number, category
            return -1, Enums.PlayerCategory.OTHER

        sente_number, sente_category = extract_player_info(cols[2].find("a"))
        gote_number, gote_category = extract_player_info(cols[3].find("a"))

        games.append(Game(
            game_id=game_id,
            game_name=game_name,
            game_category=game_category,
            sente_player_number=sente_number,
            sente_player_name=sente_player_name,
            sente_player_category=sente_category,
            sente_player_id=sente_category.symbol + "_" + str(sente_number),
            sente_player_result=sente_result,
            gote_player_number=gote_number,
            gote_player_name=gote_player_name,
            gote_player_category=gote_category,
            gote_player_id=gote_category.symbol + "_" + str(gote_number),
            gote_player_result=gote_result,
            date=current_date,
            year=year,
        ))
        game_id += 1

    return games
