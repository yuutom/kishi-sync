import json
from typing import List

from repository.base import BaseRepository, serialize_dataclass


class JSONRepository(BaseRepository):
    def __init__(self, output_path: str = "players.json"):
        self.output_path = output_path

    def save(self, targets: List[any]) -> None:
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(
                [serialize_dataclass(target) for target in targets],
                f,
                ensure_ascii=False,
                indent=2
            )
