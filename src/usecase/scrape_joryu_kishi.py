from domain.enums import Enums
from infra.joryu_kishi_scraper import parse_joryu_kishi_detail
from infra.player_list_scraper import extract_active_kishi_urls_from_list_page
from repository.base import BaseRepository


def scrape_and_save_joryu_kishi(repo: BaseRepository):
    joryu_kishi_urls = extract_active_kishi_urls_from_list_page(Enums.PlayerCategory.JORYU.symbol)
    players = [parse_joryu_kishi_detail(url) for url in joryu_kishi_urls]
    repo.save(players)
