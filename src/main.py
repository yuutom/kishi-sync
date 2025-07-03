from repository.json_repository import JSONRepository
from usecase.scrape_players import scrape_and_save_players


def main():
    repo = JSONRepository("players.json")
    scrape_and_save_players(repo)


if __name__ == "__main__":
    main()
