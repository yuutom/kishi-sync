from abc import ABC, abstractmethod
from typing import List

from domain.player import Player


class PlayerRepository(ABC):
    @abstractmethod
    def save(self, players: List[Player]) -> None:
        pass
