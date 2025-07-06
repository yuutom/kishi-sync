from dataclasses import dataclass
from typing import Optional

from domain.enums import Enums
from domain.record import Record


@dataclass
class Player:
    id: str
    kishi_number: int
    nameKana: str
    nameRome: str
    image_url: str
    birth_date: str
    debut_date: Optional[str]
    birth_place: str
    master: str
    ryuohsen: str
    junisen: str
    ryuohsen_class: Enums.RyuohsenClass
    junisen_class: Enums.JunisenClass
    danni: Enums.Danni
    title: list[Enums.Title]
    affiliation: Optional[Enums.Affiliation]
    playing_style: Optional[Enums.PlayingStyle]
    player_category: Enums.PlayerCategory
    is_active: bool
