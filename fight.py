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
            90: "车",
            91: "马",
            92: "相",
            93: "士",
            94: "帅",
            95: "士",
            96: "相",
            97: "马",
            98: "车",
            71: "炮",
            77: "炮",
            60: "兵",
            62: "兵",
            64: "兵",
            66: "兵",
            68: "兵",

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
    beach = Beach()
    pao = Qizi(idt=10086, p=60, typ=5, beach=beach)  # 炮
    bingo = Qizi(idt=8000, p=50, typ=7, beach=beach)  # 兵
    pawn = Qizi(idt=12345, p=10, typ=13, beach=beach)  # Pawn
    beach.set(p=60, qizi=pao)
    beach.set(p=50, qizi=bingo)
    beach.set(p=10, qizi=pawn)
    pao.get_ma()
    print(pao.ma)
