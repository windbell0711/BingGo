"""
-*- coding: utf-8 -*-
@Github  : windbell0711/BingGo
@File    : config.py
"""
from __future__ import annotations
from typing import List, Dict, Tuple

friend_fight = False

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

    "R": 8,
    "N": 9,
    "B": 10,
    "Q": 11,
    "K": 12,
    "P": 13
}

typ_num2str = {
    0: "将",
    1: "车",
    2: "马",
    3: "相",
    4: "士",
    5: "炮",
    6: "帅",
    7: "兵",
    8: "R ",
    9: "N ",
    10: "B ",
    11: "Q ",
    12: "K ",
    13: "P "
}

init_lineup = [
    "R", "N", "B", "K", " ", "Q", "B", "N", "R", "",
    "P", "P", "P", "P", "P", "P", "P", "P", "P", "",
    " ", " ", " ", " ", " ", " ", " ", " ", " ", "",
    " ", " ", " ", " ", " ", " ", " ", " ", " ", "",
    " ", " ", " ", " ", " ", " ", " ", " ", " ", "",
    "兵", " ", "兵", " ", "兵", " ", "兵", " ", "兵", "",
    " ", "炮", " ", " ", " ", " ", " ", "炮", " ", "",
    " ", " ", " ", " ", " ", " ", " ", " ", " ", "",
    "车", "马", "相", "士", "帅", "士", "相", "马", "车", ""
]



# init_lineup = {
#     80: "车",
#     81: "马",
#     82: "相",
#     83: "士",
#     84: "帅",
#     85: "士",
#     86: "相",
#     87: "马",
#     88: "车",
#     61: "炮",
#     64: "炮",
#     67: "炮",
#     50: "兵",
#     52: "兵",
#     54: "兵",
#     56: "兵",
#     58: "兵",
#
#     0: "R",
#     1: "N",
#     2: "B",
#     3: "K",
#     5: "Q",
#     6: "B",
#     7: "N",
#     8: "R",
#     10: "P",
#     11: "P",
#     12: "P",
#     13: "P",
#     14: "P",
#     15: "P",
#     16: "P",
#     17: "P",
#     18: "P"
# }
