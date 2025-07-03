from infra.game_result_scraper import parse_game_result
from repository.base import BaseRepository


def scrape_and_save_games(repo: BaseRepository):
    game_urls = [
        "https://www.shogi.or.jp/game/result/202401.html",
    ]
    players = [parse_game_result(url) for url in game_urls]
    repo.save(players)
