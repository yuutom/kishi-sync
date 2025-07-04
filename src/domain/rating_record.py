from collections import defaultdict
from typing import List
from dataclasses import dataclass

from domain.enums import Enums


@dataclass
class RatingRecord:
    player_number: int
    player_name: str
    player_category: Enums.PlayerCategory
    player_id: str
    opponent_number: int
    opponent_name: str
    opponent_category: Enums.PlayerCategory
    opponent_id: str
    year: int
    date: str
    rating: float
    delta: float
    opponent_rating: float
    opponent_rating_delta: float
    result_status: Enums.ResultStatus
    game_id: int
    game_name: str


initial_rating = 1500.0
K = 32

ratings = defaultdict(lambda: initial_rating)
rating_history: List[RatingRecord] = []