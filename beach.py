"""
-*- coding: utf-8 -*-
@Time    : 2025-01-19
@Author  : TheWindbell07
@File    : beach.py
"""
from qizi import *

class Beach:
    def __init__(self):
        self.beach: List[Qizi] = [None] * 90  # 沙场，每行末尾无子
        # self.soldiers: Dict[int: List[Qizi]]  # TODO: 有待商议

    def __getitem__(self, item):
        """返回该位置棋子或None"""
        return self.beach[item]

    def set(self, qizi, p: int):
        """将指定位置设定为棋子或None"""
        self.beach[p] = qizi
        return True

    def continuously_set(self, qizis: dict):
        i = 0
        for key, value in qizis.items():
            if isinstance(value, str):
                value = config.typ_dict[value]
            qizi = Qizi(idt=i, p=key, typ=value, beach=self)
            self.set(qizi, key)
            i += 1
        return True

    def move_son(self, pfrom: int, pto: int):
        self.set(qizi=self[pfrom], p=pto)
        return True

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
    pao = Qizi(idt=10086, p=60, typ=5, beach=beach)  # 炮
    bingo = Qizi(idt=8000, p=50, typ=7, beach=beach)  # 兵
    pawn = Qizi(idt=12345, p=10, typ=13, beach=beach)  # Pawn
    beach.set(qizi=pao, p=60)
    beach.set(qizi=bingo, p=50)
    beach.set(qizi=pawn, p=10)
    pao.get_ma()
    print(pao.ma)
    pao.move(10)
    print(beach.beach)
