from infra.scraper import parse_player_detail
from repository.base import PlayerRepository


def scrape_and_save_players(repo: PlayerRepository):
    # 仮：手動でURL列挙（後で一覧ページから抽出）
    player_urls = [
        "https://www.shogi.or.jp/player/pro/307.html",
        "https://www.shogi.or.jp/player/pro/123.html"
    ]
    players = [parse_player_detail(url) for url in player_urls]
    repo.save(players)
