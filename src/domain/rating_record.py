from collections import defaultdict
from typing import List
from dataclasses import dataclass

from domain.enums import Enums


@dataclass
class RatingRecord:
    player_number: int
    player_category: Enums.PlayerCategory
    date: str
    rating: float
    delta: float
    game_id: int


initial_rating = 1500.0
K = 32

ratings = defaultdict(lambda: initial_rating)
rating_history: List[RatingRecord] = []