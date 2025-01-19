"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Author  : Lilold333
@Coauthor: TheWindbell07
@File    : move.py
"""
import config


class Beach:
    def __init__(self):
        self.beach: list[Qizi] = [None] * 90  # 沙场，每行末尾无子

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


class Qizi:
    def __init__(self, idt: int, p: int, typ: int, beach):
        self.idt = idt  # id
        self.alive = True
        self.p = p  # 位置代码
        self.typ = typ  # 种类
        self.camp_intl = (typ > 7)  # False-中象; True-国象
        self.beach = beach  # 所在沙场地址
        self.ma = []  # 可移动位置

    def _not_mine(self, x: int) -> bool:  # 空 / 敌
        """检测当前位置合法并且不是友方"""
        if not self.beach.valid(x):
            return False
        if self.beach[x] is not None:
            if self.camp_intl == self.beach[x].camp_intl:
                return False
        return True

    def _enemy_occupied(self, x: int) -> bool:  # 敌
        """检测当前位置合法并且是敌方"""
        if self._not_mine(x) and self.beach.occupied(x):
            return True
        return False

    def get_ma(self):
        test2 = self.beach.valid
        test = self.beach.not_occupied
        eat = self._not_mine
        special_eat = self._enemy_occupied
        ma = []  # move available positions
        if self.typ in (1, 8, 11):  # 直走
            p = self.p + 1
            while test(p):
                ma.append(p)
                p += 1
            if special_eat(p):
                ma.append(p)
            p = self.p - 1
            while test(p):
                ma.append(p)
                p += -1
            if special_eat(p):
                ma.append(p)
            p = self.p + 10
            while test(p):
                ma.append(p)
                p += 10
            if special_eat(p):
                ma.append(p)
            p = self.p - 10
            while test(p):
                ma.append(p)
                p += -10
            if special_eat(p):
                ma.append(p)
        if self.typ in (10, 11):  # 斜走的走子
            p = self.p + 11
            while test(p):
                ma.append(p)
                p += 11
            if special_eat(p):
                ma.append(p)
            p = self.p - 11
            while test(p):
                ma.append(p)
                p += -11
            if special_eat(p):
                ma.append(p)
            p = self.p + 9
            while test(p):
                ma.append(p)
                p += 9
            if special_eat(p):
                ma.append(p)
            p = self.p - 9
            while test(p):
                ma.append(p)
                p += -9
            if special_eat(p):
                ma.append(p)
        if self.typ == 2:  # 有马腿马
            p = self.p
            if test(p + 1):  # 马腿处子的判断
                if eat(p + 12):  # 落点吃子判断
                    ma.append(p + 12)
                if eat(p - 8):
                    ma.append(p - 8)
            if test(p - 1):
                if eat(p - 12):
                    ma.append(p - 12)
                if eat(p + 8):
                    ma.append(p + 8)
            if test(p + 10):
                if eat(p + 21):
                    ma.append(p + 21)
                if eat(p + 19):
                    ma.append(p + 19)
            if test(p - 10):
                if eat(p - 21):
                    ma.append(p - 21)
                if eat(p - 19):
                    ma.append(p - 19)
        if self.typ == 9:  # 无马腿马
            p = self.p
            if test2(p + 1):  # 马腿处子的判断
                if eat(p + 12):  # 落点吃子判断
                    ma.append(p + 12)
                if eat(p - 8):
                    ma.append(p - 8)
            if test2(p - 1):
                if eat(p - 12):
                    ma.append(p - 12)
                if eat(p + 8):
                    ma.append(p + 8)
            if test2(p + 10):
                if eat(p + 21):
                    ma.append(p + 21)
                if eat(p + 19):
                    ma.append(p + 19)
            if test2(p - 10):
                if eat(p - 21):
                    ma.append(p - 21)
                if eat(p - 19):
                    ma.append(p - 19)
        if self.typ == 3:  # xiang
            p = self.p
            if test(p + 11):  # xiang腿处子的判断
                if eat(p + 22):  # 落点吃子判断
                    ma.append(p + 22)
            if test(p - 11):
                if eat(p - 22):
                    ma.append(p - 22)
            if test(p + 9):
                if eat(p + 18):
                    ma.append(p + 18)
            if test(p - 9):
                if eat(p - 18):
                    ma.append(p - 18)
        if self.typ in (4, 12):  # shi king
            p = self.p
            if eat(p - 11):
                ma.append(p - 11)
            if eat(p + 11):
                ma.append(p + 11)
            if eat(p - 9):
                ma.append(p - 9)
            if eat(p + 9):
                ma.append(p + 9)
        if self.typ == 6:  # shuai
            p = self.p
            if not p % 10 == 3 and eat(p - 1):
                ma.append(p - 1)
            if not p % 10 == 5 and eat(p + 1):
                ma.append(p + 1)
            if not p // 10 == 6 and eat(p - 10):
                ma.append(p - 10)
            if not p // 10 == 8 and eat(p + 10):
                ma.append(p + 10)
        if self.typ in (7, 12):  # bingo king
            p = self.p
            if not p % 10 == 0 and eat(p - 1):
                ma.append(p - 1)
            if not p % 10 == 8 and eat(p + 1):
                ma.append(p + 1)
            if not p // 10 == 0 and eat(p - 10):
                ma.append(p - 10)
        if self.typ == 12:  # king
            p = self.p
            if not p // 10 == 8 and eat(p + 10):
                ma.append(p + 10)
        if self.typ == 13:  # pawn
            p = self.p
            if test(p + 10):
                ma.append(p + 10)
            if special_eat(p + 11):
                ma.append(p + 11)
            if special_eat(p + 9):
                ma.append(p + 9)
            if p//10 == 1 and test(p+10) and test(p+20):  # 第一步
                ma.append(p+20)
        if self.typ == 5:  # pao
            p = self.p + 1
            while test(p):
                ma.append(p)
                p += 1
            p += 1
            while test(p):
                p += 1
            if special_eat(p):
                ma.append(p)
            p = self.p + 10
            while test(p):
                ma.append(p)
                p += 10
            p += 10
            while test(p):
                p += 10
            if special_eat(p):
                ma.append(p)
            p = self.p - 1
            while test(p):
                ma.append(p)
                p += -1
            p += -1
            while test(p):
                p += -1
            if special_eat(p):
                ma.append(p)
            p = self.p - 10
            while test(p):
                ma.append(p)
                p += -10
            p += -10
            while test(p):
                p += -10
            if special_eat(p):
                ma.append(p)
        self.ma = ma

    def move(self, p):
        """对该子在beach中实施移动，包括吃子，不校验能否走到。"""
        if self.beach[p] is not None:  # 吃子
            self.beach[p].alive = False  # 你死
            self.beach.set(None, p)  # 你走
        self.beach.set(None, self.p)  # 我走
        self.beach.set(self, p)  # 我来
        self.p = p  # 我动


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
