"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Author  : Lilold333
@Coauthor: TheWindbell07
@File    : move.py
"""

mycamp = 0  # 阵营 0-中象 1-国象

def is_mycamp(is_camp_intl: bool) -> bool:
    return mycamp == is_camp_intl


class Beach:
    def __init__(self):
        self.beach: list[Qizi] = [None] * 90  # 沙场，每行末尾无子

    def __getitem__(self, item):
        """返回该位置棋子或None"""
        return self.beach[item]

    def set(self, qizi, p: int):
        """将指定位置设定为棋子或None"""
        self.beach[p] = qizi

    def valid(self, x: int) -> bool:  # 合法
        """检测当前位置合法 test2"""
        if x % 10 == 9:
            return False
        if not 0 <= x <= 89:
            return False
        return True
    test2 = valid  # 别名适配
    
    def not_occupied(self, x: int) -> bool:  # 空
        """检测当前位置合法并且没有子 test"""
        if self.valid(x) and self.beach[x] is None:
            return True
        return False
    test = not_occupied
    
    def not_mine(self, x: int) -> bool:  # 空 / 敌
        """检测当前位置合法并且不是友方 eat"""
        if not self.valid(x):
            return False
        if self.beach[x] is not None:
            if is_mycamp(self.beach[x].camp_intl):
                return False
        return True
    eat = not_mine
    
    def enemy_occupied(self, x: int) -> bool:  # 敌
        """检测当前位置合法并且是敌方 special_eat"""
        if self.not_mine(x) and not self.not_occupied(x):
            return True
        return False
    special_eat = enemy_occupied


class Qizi:
    def __init__(self, idt: int, p: int, typ: int, beach):
        self.idt = idt  # id
        self.p = p  # 位置代码
        self.typ = typ  # 种类
        self.camp_intl = (typ > 7)  # False-中象; True-国象
        self.beach = beach  # 所在沙场地址
        self.ma = []  # 可移动位置

    def get_ma(self):
        # 快捷使用位置子判断方法
        valid = self.beach.valid
        not_occupied = self.beach.not_occupied
        not_mine = self.beach.not_mine
        enemy_occupied = self.beach.enemy_occupied

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
        if self.typ in (4, 12):  # shi, king
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
        if self.typ in (7, 12):  # bingo, king
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
            p += 1
            while not_occupied(p):
                p += 1
            if enemy_occupied(p):
                ma.append(p)
            p = self.p + 10
            while not_occupied(p):
                ma.append(p)
                p += 10
            p += 10
            while not_occupied(p):
                p += 10
            if enemy_occupied(p):
                ma.append(p)
            p = self.p - 1
            while not_occupied(p):
                ma.append(p)
                p += -1
            p += -1
            while not_occupied(p):
                p += -1
            if enemy_occupied(p):
                ma.append(p)
            p = self.p - 10
            while not_occupied(p):
                ma.append(p)
                p += -10
            p += -10
            while not_occupied(p):
                p += -10
            if enemy_occupied(p):
                ma.append(p)
        self.ma = ma


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
