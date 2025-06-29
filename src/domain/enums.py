from enum import Enum


class Enums:
    class Title(Enum):
        RYUOH = "竜王",
        MEIJIN = "名人",
        EIOH = "叡王",
        OUI = "王位",
        KIOH = "棋王",
        OUSHO = "王将",
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
        NONE = "なし"
        DAN4 = "四段"
        DAN5 = "五段"
        DAN6 = "六段"
        DAN7 = "七段"
        DAN8 = "八段"
        DAN9 = "九段"

    class Affiliation(Enum):
        KANTOU = "関東"
        KANSAI = "関西"

    class PlayingStyle(Enum):
        IBISHA = "居飛車"
        HURIBISHA = "振り飛車"
        DUAL = "両刀"

    class PlayerCategory(Enum):
        KISHI = "棋士"
        JORYU = "女流棋士"

    class GameCategory(Enum):
        JUNI = "順位戦・名人戦",
        RYUOH = "竜王戦",
        EIOH = "叡王戦",
        OUI = "王位戦",
        OUZA = "王座戦",
        KISEI = "棋聖戦",
        KIOH = "棋王戦",
        ASAHI_CUP = "朝日杯戦",
        GINGA = "銀河戦",
        NHK = "NHK杯戦",
        JT = "日本シリーズ",
        TATSUZIN = "達人戦",
        SHINJINOH = "新人王戦",
        KAKOGAWA = "加古川青流戦",
        ABEMA = "ABEMAトーナメント",
        SUNTORY = "東西対抗戦"

    class ResultStatus(Enum):
        WIN = "勝ち",
        DEFEAT = "負け",
        BYE_WIN = "不戦勝",
        BYE_DEFEAT = "不戦敗",
        TBD = "未実施"
