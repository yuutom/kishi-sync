from dataclasses import dataclass

from domain.enums import Enums


@dataclass
class ResultFromKishi:
    game_name: str
    game_category: Enums.GameCategory
    opponent_number: int
    opponent_name: str
    result_status: Enums.ResultStatus
    date: str
