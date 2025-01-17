"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Author  : Lilold333
@Coauthor: TheWindbell07
@File    : move.py
"""

def is_mycamp(is_camp_intl: bool) -> bool:
    return mycamp == is_camp_intl

def valid(x: int) -> bool:
    """检测当前位置合法 test2"""
    if x % 10 == 9:
        return False
    if not 0 <= x <= 89:
        return False
    return True
test2 = valid  # 别名适配

def not_occupied(x: int) -> bool:
    """检测当前位置合法并且没有子 test"""
    if valid(x) and beach[x] is None:
        return True
    return False
test = not_occupied

def not_mine(x: int) -> bool:
    """检测当前位置合法并且不是友方 eat"""
    if not valid(x):
        return False
    if beach[x] is not None:
        if is_mycamp(beach[x].camp_intl):
            return False
    return True
eat = not_mine

def enemy_occupied(x: int) -> bool:
    """检测当前位置合法并且是敌方 special_eat"""
    if not_mine(x) and not_occupied(x):
        return True
    return False
special_eat = enemy_occupied


mycamp = 0  # 阵营 0-中象 1-国象
beach = []  # 沙场，每行末尾无子


class Qizi:
    def __init__(self, idt: int, p: int, typ: int):
        self.idt = idt  # id
        self.p = p  # 位置代码
        self.typ = typ  # 种类
        self.camp_intl = (typ < 7)  # False-中象; True-国象
        self.ma = []  # 可移动位置

    def get_ma(self):
        ma = []  # move available positions
        if self.typ in (1, 8, 11):  # 直走
            p = self.p + 1
            while not_occupied(p):
                ma.append(p)
                p += 1
            if enemy_occupied(p):
                ma.append(p)
            p = self.p - 1
            while not_occupied(p):
                ma.append(p)
                p += -1
            if enemy_occupied(p):
                ma.append(p)
            p = self.p + 10
            while not_occupied(p):
                ma.append(p)
                p += 10
            if enemy_occupied(p):
                ma.append(p)
            p = self.p - 10
            while not_occupied(p):
                ma.append(p)
                p += -10
            if enemy_occupied(p):
                ma.append(p)
        if self.typ in (10, 11):  # 斜走的走子
            p = self.p + 11
            while not_occupied(p):
                ma.append(p)
                p += 11
            if enemy_occupied(p):
                ma.append(p)
            p = self.p - 11
            while not_occupied(p):
                ma.append(p)
                p += -11
            if enemy_occupied(p):
                ma.append(p)
            p = self.p + 9
            while not_occupied(p):
                ma.append(p)
                p += 9
            if enemy_occupied(p):
                ma.append(p)
            p = self.p - 9
            while not_occupied(p):
                ma.append(p)
                p += -9
            if enemy_occupied(p):
                ma.append(p)
        if self.typ == 2:  # 有马腿马
            p = self.p
            if not_occupied(p + 1):  # 马腿处子的判断
                if not_mine(p + 12):  # 落点吃子判断
                    ma.append(p + 12)
                if not_mine(p - 8):
                    ma.append(p - 8)
            if not_occupied(p - 1):
                if not_mine(p - 12):
                    ma.append(p - 12)
                if not_mine(p + 8):
                    ma.append(p + 8)
            if not_occupied(p + 10):
                if not_mine(p + 21):
                    ma.append(p + 21)
                if not_mine(p + 19):
                    ma.append(p + 19)
            if not_occupied(p - 10):
                if not_mine(p - 21):
                    ma.append(p - 21)
                if not_mine(p - 19):
                    ma.append(p - 19)
        if self.typ == 9:  # 无马腿马
            p = self.p
            if valid(p + 1):  # 马腿处子的判断
                if not_mine(p + 12):  # 落点吃子判断
                    ma.append(p + 12)
                if not_mine(p - 8):
                    ma.append(p - 8)
            if valid(p - 1):
                if not_mine(p - 12):
                    ma.append(p - 12)
                if not_mine(p + 8):
                    ma.append(p + 8)
            if valid(p + 10):
                if not_mine(p + 21):
                    ma.append(p + 21)
                if not_mine(p + 19):
                    ma.append(p + 19)
            if valid(p - 10):
                if not_mine(p - 21):
                    ma.append(p - 21)
                if not_mine(p - 19):
                    ma.append(p - 19)
        if self.typ == 3:  # xiang
            p = self.p
            if not_occupied(p + 11):  # xiang腿处子的判断
                if not_mine(p + 22):  # 落点吃子判断
                    ma.append(p + 22)
            if not_occupied(p - 11):
                if not_mine(p - 22):
                    ma.append(p - 22)
            if not_occupied(p + 9):
                if not_mine(p + 18):
                    ma.append(p + 18)
            if not_occupied(p - 9):
                if not_mine(p - 18):
                    ma.append(p - 18)
        if self.typ in (4, 12):  # shi king
            p = self.p
            if not_mine(p - 11):
                ma.append(p - 11)
            if not_mine(p + 11):
                ma.append(p + 11)
            if not_mine(p - 9):
                ma.append(p - 9)
            if not_mine(p + 9):
                ma.append(p + 9)
        if self.typ == 6:  # shuai
            p = self.p
            if not p % 10 == 3:
                ma.append(p - 1)
            if not p % 10 == 5:
                ma.append(p + 1)
            if not p // 10 == 6:
                ma.append(p - 10)
            if not p // 10 == 8:
                ma.append(p + 10)
        if self.typ in (7, 12):  # bingo king
            p = self.p
            if not p % 10 == 0:
                ma.append(p + 1)
            if not p % 10 == 8:
                ma.append(p - 1)
            if not p // 10 == 0:
                ma.append(p - 10)
        if self.typ == 12:  # king
            p = self.p
            if not p // 10 == 8:
                ma.append(p + 10)
        if self.typ == 13:  # pawn
            p = self.p
            if not_occupied(p + 10):
                ma.append(p + 10)
            if enemy_occupied(p + 11):
                ma.append(p + 11)
            if enemy_occupied(p + 9):
                ma.append(p + 9)
        if self.typ == 5:  # pao
            p = self.p + 1
            while not_occupied(p):
                ma.append(p)
                p += 1
            while not_occupied(p):
                p += 1
            if enemy_occupied(p):
                ma.append(p)
            p = self.p + 10
            while not_occupied(p):
                ma.append(p)
                p += 10
            while not_occupied(p):
                p += 10
            if enemy_occupied(p):
                ma.append(p)
            p = self.p - 1
            while not_occupied(p):
                ma.append(p)
                p += -1
            while not_occupied(p):
                p += -1
            if enemy_occupied(p):
                ma.append(p)
            p = self.p - 10
            while not_occupied(p):
                ma.append(p)
                p += -10
            while not_occupied(p):
                p += -10
            if enemy_occupied(p):
                ma.append(p)
        self.ma = ma


if __name__ == '__main__':
    beach: list[Qizi] = [None] * 90
    pao = Qizi(idt=10086, p=60, typ=5)  # 炮
    bingo = Qizi(idt=8000, p=50, typ=7)  # 兵
    pawn = Qizi(idt=12345, p=10, typ=13)  # Pawn
    beach[60], beach[50], beach[10] = pao, bingo, pawn
    pao.get_ma()
    print(pao.ma)
