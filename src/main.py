from repository.json_repository import JSONPlayerRepository
from usecase.scrape_players import scrape_and_save_players


def main():
    repo = JSONPlayerRepository("players.json")
    scrape_and_save_players(repo)


if __name__ == "__main__":
    main()
