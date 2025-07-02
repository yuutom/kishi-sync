import json
from typing import List

from domain.player import Player
from repository.base import PlayerRepository, serialize_dataclass


class JSONPlayerRepository(PlayerRepository):
    def __init__(self, output_path: str = "players.json"):
        self.output_path = output_path

    def save(self, players: List[Player]) -> None:
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(
                [serialize_dataclass(player) for player in players],
                f,
                ensure_ascii=False,
                indent=2
            )
