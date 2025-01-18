"""
-*- coding: utf-8 -*-
@Time    : 2025-01-18 13:56
@Author  : TheWindbell07
@File    : fight.py
"""
from move import *


class War:
    def __init__(self):
        self.beach = Beach()
        self.beach.continuously_set(qizis={
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
        })

    def move_son(self, pfrom: int, pto: int):
        self.beach.set(qizi=self.beach[pfrom], p=pto)


if __name__ == '__main__':
    war = War()
    beach = war.beach
    print(beach[18])
