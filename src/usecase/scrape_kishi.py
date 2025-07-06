from domain.enums import Enums
from infra.player_list_scraper import extract_active_kishi_urls_from_list_page
from infra.player_scraper import parse_player_detail
from repository.base import BaseRepository


def scrape_and_save_players(repo: BaseRepository):
    player_urls = extract_active_kishi_urls_from_list_page(Enums.PlayerCategory.KISHI.symbol)
    players = [parse_player_detail(url) for url in player_urls]
    repo.save(players)
