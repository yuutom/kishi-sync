import json

from repository.json_repository import JSONRepository
from usecase.calculate_rating import calculate_rating_history
from usecase.scrape_games import scrape_and_save_games
from usecase.scrape_joryu_kishi import scrape_and_save_joryu_kishi
from usecase.scrape_players import scrape_and_save_players


def main():
    # playerの抽出
    repo = JSONRepository("players.json")
    scrape_and_save_players(repo)

    # 女流棋士の抽出
    repo = JSONRepository("joryu_kishi.json")
    scrape_and_save_joryu_kishi(repo)

    # 対局結果の抽出
    repo_for_result = JSONRepository("game_results.json")
    scrape_and_save_games(repo_for_result)

    # レーティング計算
    repo_for_raging = JSONRepository("rating_history.json")
    with open("game_results.json", encoding="utf-8") as f:
        game_data = json.load(f)

    flat_games = [g for day in game_data for g in day]
    history = calculate_rating_history(flat_games)
    repo_for_raging.save(history)


if __name__ == "__main__":
    main()
