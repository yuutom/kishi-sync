from dataclasses import dataclass

from domain.enums import Enums


@dataclass
class Game:
    game_id: int
    game_name: str
    game_category: Enums.GameCategory
    sente_player_number: int
    sente_player_name: str
    sente_player_category: Enums.PlayerCategory
    sente_player_id: str
    sente_player_result: Enums.ResultStatus
    gote_player_number: int
    gote_player_name: str
    gote_player_category: Enums.PlayerCategory
    gote_player_id: str
    gote_player_result: Enums.ResultStatus
    date: list[str]
    year: int
