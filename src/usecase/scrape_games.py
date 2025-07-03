from infra.game_result_scraper import parse_game_result
from repository.base import BaseRepository


def scrape_and_save_games(repo: BaseRepository):
    start_year = 2019
    end_year = 2025

    game_urls = []
    for year in range(start_year, end_year):
        for month in range(1, 13):
            url = f"https://www.shogi.or.jp/game/result/{year}{month:02}.html"
            game_urls.append(url)
    players = [parse_game_result(url) for url in game_urls]
    repo.save(players)
