from infra.game_result_scraper import parse_game_result
from repository.base import BaseRepository


def scrape_and_save_games(repo: BaseRepository):
    game_urls = [
        "https://www.shogi.or.jp/game/result/202401.html",
        "https://www.shogi.or.jp/game/result/202402.html",
        "https://www.shogi.or.jp/game/result/202403.html",
        "https://www.shogi.or.jp/game/result/202404.html",
        "https://www.shogi.or.jp/game/result/202405.html",
        "https://www.shogi.or.jp/game/result/202406.html",
        "https://www.shogi.or.jp/game/result/202407.html",
        "https://www.shogi.or.jp/game/result/202408.html",
        "https://www.shogi.or.jp/game/result/202409.html",
        "https://www.shogi.or.jp/game/result/202410.html",
        "https://www.shogi.or.jp/game/result/202411.html",
        "https://www.shogi.or.jp/game/result/202412.html",
    ]
    players = [parse_game_result(url) for url in game_urls]
    repo.save(players)
