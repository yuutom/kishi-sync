from abc import ABC, abstractmethod
from dataclasses import is_dataclass, asdict
from typing import List, Any
from enum import Enum
from typing import Type, TypeVar, Dict


class BaseRepository(ABC):
    @abstractmethod
    def save(self, players: List[any]) -> None:
        pass


def serialize_dataclass(obj: Any) -> Any:
    """
    dataclass内の Enum を再帰的に変換して JSON シリアライズ可能な dict に変換
    """
    if isinstance(obj, Enum):
        return EnumMapper.to_int(obj)
    elif is_dataclass(obj):
        return {k: serialize_dataclass(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, list):
        return [serialize_dataclass(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: serialize_dataclass(v) for k, v in obj.items()}
    else:
        return obj


T = TypeVar("T", bound=Enum)


class EnumMapper:
    """
    Enum値 <-> 整数 の双方向マッピングユーティリティ
    """
    _enum_to_int_map: Dict[Type[Enum], Dict[Enum, int]] = {}
    _int_to_enum_map: Dict[Type[Enum], Dict[int, Enum]] = {}

    @classmethod
    def register_enum(cls, enum_cls: Type[T]):
        if enum_cls not in cls._enum_to_int_map:
            cls._enum_to_int_map[enum_cls] = {e: i for i, e in enumerate(enum_cls)}
            cls._int_to_enum_map[enum_cls] = {i: e for i, e in enumerate(enum_cls)}

    @classmethod
    def to_int(cls, enum_val: T) -> int:
        enum_cls = type(enum_val)
        cls.register_enum(enum_cls)
        return cls._enum_to_int_map[enum_cls][enum_val]

    @classmethod
    def from_int(cls, enum_cls: Type[T], value: int) -> T:
        cls.register_enum(enum_cls)
        return cls._int_to_enum_map[enum_cls][value]

