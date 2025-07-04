from datetime import datetime

from infra.game_result_scraper import parse_game_result
from repository.base import BaseRepository


def scrape_and_save_games(repo: BaseRepository):
    start_year = 2007
    current = datetime.now()

    game_urls = []
    for year in range(start_year, current.year + 1):
        max_month = current.month if year == current.year else 12
        for month in range(1, max_month + 1):
            url = f"https://www.shogi.or.jp/game/result/{year}{month:02}.html"
            game_urls.append(url)
    players = [parse_game_result(url) for url in game_urls]
    repo.save(players)
