from enum import Enum


class Enums:
    class Title(Enum):
        RYUOH = "竜王"
        MEIJIN = "名人"
        EIOH = "叡王"
        OUI = "王位"
        KIOH = "棋王"
        OUSHO = "王将"
        OUZA = "王座"
        KISEI = "棋聖"

    class JunisenClass(Enum):
        MEIJIN = "名人"
        A = "A級"
        B1 = "B級1組"
        B2 = "B級2組"
        C1 = "C級1組"
        C2 = "C級2組"
        FREE = "フリー"
        NONE = "なし"

    class RyuohsenClass(Enum):
        RYUOH = "竜王"
        CLASS1 = "1組"
        CLASS2 = "2組"
        CLASS3 = "3組"
        CLASS4 = "4組"
        CLASS5 = "5組"
        CLASS6 = "6組"
        NONE = "なし"

    class Danni(Enum):
        DAN4 = "四段"
        DAN5 = "五段"
        DAN6 = "六段"
        DAN7 = "七段"
        DAN8 = "八段"
        DAN9 = "九段"
        NONE = "なし"

    class Affiliation(Enum):
        KANTOU = "関東"
        KANSAI = "関西"
        NONE = "なし"

    class PlayingStyle(Enum):
        NONE = "なし"
        IBISHA = "居飛車"
        HURIBISHA = "振り飛車"
        DUAL = "両刀"

    class PlayerCategory(Enum):
        KISHI = "棋士"
        JORYU = "女流棋士"

    class GameCategory(Enum):
        JUNI = ("順位戦・名人戦", "junni")
        RYUOH = ("竜王戦", "ryuuou")
        EIOH = ("叡王戦", "eiou")
        OUI = ("王位戦", "oui")
        OUZA = ("王座戦", "ouza")
        KISEI = ("棋聖戦", "kisei")
        KIOH = ("棋王戦", "kiou")
        ASAHI_CUP = ("朝日杯戦", "asahi_cup")
        GINGA = ("銀河戦", "ginga")
        NHK = ("NHK杯戦", "nhk")
        JT = ("日本シリーズ", "jt")
        TATSUZIN = ("達人戦", "tatsujinsen")
        SHINJINOH = ("新人王戦", "shinjin")
        KAKOGAWA = ("加古川青流戦", "kakogawa")
        ABEMA = ("ABEMAトーナメント", "abematv")
        SUNTORY = ("東西対抗戦", "suntory")
        OTHER = ("その他", "")

        def __init__(self, label: str, symbol: str):
            self.label = label
            self.symbol = symbol

        @classmethod
        def from_symbol(cls, symbol: str):
            for status in cls:
                if status.symbol == symbol:
                    return status
            return cls.OTHER

        @classmethod
        def from_label(cls, label: str):
            for status in cls:
                if status.label == label:
                    return status
            return cls.OTHER

    class ResultStatus(Enum):
        WIN = ("勝ち", "○")
        DEFEAT = ("負け", "●")
        BYE_WIN = ("不戦勝", "□")
        BYE_DEFEAT = ("不戦敗", "■")
        TBD = ("未実施", "")

        def __init__(self, label: str, symbol: str):
            self.label = label
            self.symbol = symbol

        @classmethod
        def from_symbol(cls, symbol: str):
            for status in cls:
                if status.symbol == symbol:
                    return status
            return cls.TBD

        @classmethod
        def from_label(cls, label: str):
            for status in cls:
                if status.label == label:
                    return status
            return cls.TBD
