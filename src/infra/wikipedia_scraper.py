import re

import requests
from bs4 import BeautifulSoup
from domain.enums import Enums


def parse_wikipedia_detail(url: str):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    info_box = soup.select_one("table.infobox")

    affiliation = Enums.Affiliation.NONE
    danni = Enums.Danni.NONE
    debut_date = None

    if info_box:
        rows = info_box.select("tr")
        for row in rows:
            th = row.find("th")
            td = row.find("td")
            if not th or not td:
                continue
            label = th.text.strip()
            value = td.text.strip()

            # プロ入り年月日の抽出と整形
            if "プロ入り年月日" in label:
                date_match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", value)
                if date_match:
                    year, month, day = map(int, date_match.groups())
                    debut_date = f"{year:04d}-{month:02d}-{day:02d}"

            # 所属
            elif "所属" in label:
                if "関東" in value:
                    affiliation = Enums.Affiliation.KANTOU
                elif "関西" in value:
                    affiliation = Enums.Affiliation.KANSAI

            # 段位
            elif "段位" in label:
                for d in Enums.Danni:
                    if d.value in value:
                        danni = d
                        break

    return debut_date, affiliation, danni
