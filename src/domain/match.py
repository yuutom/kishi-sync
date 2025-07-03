from dataclasses import dataclass
from typing import Optional

from domain.enums import Enums


@dataclass
class Game:
    game_id: Optional[int]
    game_name: str
    game_category: Enums.GameCategory
    sente_player_id: Optional[int]
    gote_player_id: Optional[int]
    sente_player_result: Optional[Enums.ResultStatus]
    gote_player_result: Optional[Enums.ResultStatus]
    date: list[str]
