"""
-*- coding: utf-8 -*-
@Time    : 2025-01-19
@Author  : TheWindbell07
@File    : beach.py
"""
from __future__ import annotations

from qizi import *


class Beach:
    def __init__(self):
        self.beach: List[Qizi]  = [None] * 90  # 沙场，每行末尾无子
        self.pieces: List[Qizi] = []  # 全体士兵，index为id，死后不移除

    def __getitem__(self, item):
        """返回该位置棋子或None"""
        return self.beach[item]

    def set_son(self, qizi, p: int) -> int | None:
        """将指定位置设定为棋子或None"""
        self.beach[p] = qizi
        if qizi is None:
            return None
        self.pieces.append(qizi)
        qizi.idt = len(self.pieces) - 1
        return qizi.idt

    def quick_set(self, qizis: dict):
        for key, value in qizis.items():
            if isinstance(value, str):
                value = config.typ_dict[value]
            qizi = Qizi(p=key, typ=value, beach=self)
            self.set_son(qizi, key)
        return True

    def move_son(self, pfrom: int, pto: int) -> int:
        """移动棋子，包括吃子"""
        self.beach[pto] = self.beach[pfrom]  # 移动到新位置
        self.beach[pfrom] = None  # 从原位置移除
        self[pto].p = pto
        return self[pto].idt

    def virtual_move(self, qizi, p: int):
        """虚拟移动，用于将死判断"""
        self.beach[p] = qizi
        if qizi is None:
            return None

    def valid(self, x: int) -> bool:  # 合法
        """检测当前位置合法"""
        if x % 10 == 9:
            return False
        if not 0 <= x <= 89:
            return False
        return True

    def occupied(self, x: int) -> bool:  # 非空
        """检测当前位置合法并且有子"""
        if self.valid(x) and self.beach[x] is not None:
            return True
        return False

    def not_occupied(self, x: int) -> bool:  # 非空
        """检测当前位置合法并且有子"""
        if self.valid(x) and self.beach[x] is None:
            return True
        return False

    def ch_occupied(self, x: int) -> bool:  # 中
        if self.occupied(x) and not self.beach[x].camp_intl:
            return True
        return False

    def in_occupied(self, x: int) -> bool:  # 国
        if self.occupied(x) and self.beach[x].camp_intl:
            return True
        return False


if __name__ == '__main__':
    beach = Beach()
    pao = Qizi(p=60, typ=5, beach=beach)  # 炮
    bingo = Qizi(p=50, typ=7, beach=beach)  # 兵
    pawn = Qizi(p=10, typ=13, beach=beach)  # Pawn
    beach.set_son(qizi=pao, p=60)
    beach.set_son(qizi=bingo, p=50)
    beach.set_son(qizi=pawn, p=10)
    pao.get_ma()
    print(pao.ma)
    pao.move(10)
    print(beach.beach)
