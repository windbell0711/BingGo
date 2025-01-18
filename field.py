"""
-*- coding: utf-8 -*-
@Time    : 2025-01-18 13:56
@Author  : TheWindbell07
@File    : field.py
"""
from move import *


class War:
    def __init__(self):
        pass

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
