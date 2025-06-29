from dataclasses import dataclass


@dataclass
class Record:
    wins: int
    loses: int
    wins_ranking: int
    consecutive_wins: int
    consecutive_wins_ranking: int
    winning_rate_ranking: int
