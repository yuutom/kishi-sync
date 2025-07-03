from collections import defaultdict
from domain.rating_record import RatingRecord
from domain.enums import Enums
from typing import List
import json

from repository.base import EnumMapper

INITIAL_RATING = 1500
K = 32


def expected_score(ra, rb):
    return 1 / (1 + 10 ** ((rb - ra) / 400))


def actual_score(result_code):
    if result_code == Enums.ResultStatus.WIN:
        return 1.0
    elif result_code == Enums.ResultStatus.DEFEAT:
        return 0.0
    elif result_code == Enums.ResultStatus.BYE_WIN:
        return 1.0
    elif result_code == Enums.ResultStatus.BYE_DEFEAT:
        return 0.0
    else:
        return None


def calculate_rating_history(games: List[dict]) -> List[RatingRecord]:
    ratings = defaultdict(lambda: INITIAL_RATING)
    history = []

    sorted_games = sorted(games, key=lambda g: (g["date"][0], g["game_id"]))

    for game in sorted_games:
        sp = game["sente_player_number"]
        spc = game["sente_player_category"]
        gp = game["gote_player_number"]
        gpc = game["gote_player_category"]
        sr = actual_score(EnumMapper.from_int(Enums.ResultStatus, game["sente_player_result"]))
        gr = actual_score(EnumMapper.from_int(Enums.ResultStatus, game["gote_player_result"]))
        date = game["date"][0]
        gid = game["game_id"]

        if sr is None or gr is None or sp == -1 or gp == -1:
            continue

        ra, rb = ratings[sp], ratings[gp]
        ea = expected_score(ra, rb)
        eb = 1 - ea

        new_ra = ra + K * (sr - ea)
        new_rb = rb + K * (gr - eb)

        history.append(RatingRecord(sp, spc, date, round(new_ra, 2), round(new_ra - ra, 2), gid))
        history.append(RatingRecord(gp, gpc, date, round(new_rb, 2), round(new_rb - rb, 2), gid))

        ratings[sp] = new_ra
        ratings[gp] = new_rb

    return history
