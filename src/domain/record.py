from dataclasses import dataclass
from typing import Optional


@dataclass
class Record:
    wins: Optional[int]
    loses: Optional[int]
    consecutive_wins: Optional[int]
    total_ranking: Optional[int]
    wins_ranking: Optional[int]
    consecutive_wins_ranking: Optional[int]
    winning_rate_ranking: Optional[int]
