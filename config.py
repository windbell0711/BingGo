from __future__ import annotations
from typing import List, Dict

typ_dict = {
    "将": 0,
    "车": 1,
    "马": 2,
    "相": 3,
    "士": 4,
    "炮": 5,
    "帅": 6,
    "兵": 7,

    "城": 8,
    "骑": 9,
    "教": 10,
    "后": 11,
    "王": 12,
    "外国兵": 13,

    "rook": 8,
    "knight": 9,
    "bishop": 10,
    "queen": 11,
    "king": 12,
    "pawn": 13
}

init_lineup = {
    80: "车",
    81: "马",
    82: "相",
    83: "士",
    84: "帅",
    85: "士",
    86: "相",
    87: "马",
    88: "车",
    61: "炮",
    64: "炮",
    67: "炮",
    50: "兵",
    52: "兵",
    54: "兵",
    56: "兵",
    58: "兵",

    0: "rook",
    1: "knight",
    2: "bishop",
    3: "king",
    5: "queen",
    6: "bishop",
    7: "knight",
    8: "rook",
    10: "pawn",
    11: "pawn",
    12: "pawn",
    13: "pawn",
    14: "pawn",
    15: "pawn",
    16: "pawn",
    17: "pawn",
    18: "pawn"
}
