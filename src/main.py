from repository.json_repository import JSONRepository
from usecase.scrape_games import scrape_and_save_games
from usecase.scrape_players import scrape_and_save_players


def main():
    # playerの抽出
    repo = JSONRepository("players.json")
    # scrape_and_save_players(repo)

    # 対局結果の抽出
    repo_for_result = JSONRepository("game_results.json")
    scrape_and_save_games(repo_for_result)


if __name__ == "__main__":
    main()
