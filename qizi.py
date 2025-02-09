"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Github  : windbell0711/BingGo
@Author  : Lilold333
@Coauthor: TheWindbell07
@License : Apache 2.0
@File    : qizi.py
"""
from typing import List, Dict, Tuple
import config


class Qizi:
    def __init__(self, p: int, typ: int, beach, idt=None):
        self.idt = idt  # 由Beach在set后任命
        self.alive = True  # 是否存活
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

    def value(self):
        c=2
        if self.typ == 1:
            return 18*c
        if self.typ in (9,10):
            return -12*c
        if self.typ== 5:
            return 12*c
        if self.typ == 2:
            return 9*c
        if self.typ ==4:
            return 1*c
        if self.typ ==3:
            return 5*c
        if self.typ == 7:
            if self.p // 10 <= 1:
                return 20*c
            else:
                return 4*c
        if self.typ == 8:
            return -18*c
        if self.typ == 11:
            return -100*c
        if self.typ == 13:
            if self.p//10>=7:
                return -20*c
            else:
                return -3*c
        if self.typ == 0:
            return 40*c
        if self.typ == 6:
            return 0
        if self.typ == 12:
            return 0


    def get_ma(self):
        test2 = self.beach.valid
        test = self.beach.not_occupied
        eat = self._not_mine
        special_eat = self._enemy_occupied
        ma = []  # moveable positions

        if self.typ in (1, 8, 11, 0):  # 直走
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
        if self.typ in (0, 2):  # 有马腿马
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
        if self.typ in (0, 3):  # xiang
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
        if self.typ in (0, 4, 12,3):  # shi king
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

            p = self.p - 10
            while test(p):
                p += -10
                if special_eat(p) and not self.beach[p]==None:
                    if self.beach[p].typ==12:
                        ma.append(p)
        if self.typ == 7:  # bingo
            p = self.p
            if not p % 10 == 0 and eat(p - 1) :
                ma.append(p - 1)
            if not p % 10 == 8 and eat(p + 1) :
                ma.append(p + 1)
            if not p // 10 == 0 and eat(p - 10):
                ma.append(p - 10)
        if self.typ in (12,4):  # king
            p = self.p
            if not p // 10 == 8 and eat(p + 10):
                ma.append(p + 10)
            if not p % 10 == 0 and eat(p - 1):
                ma.append(p - 1)
            if not p % 10 == 8 and eat(p + 1):
                ma.append(p + 1)
            if not p // 10 == 0 and eat(p - 10):
                ma.append(p - 10)
        if self.typ == 13:  # pawn
            p = self.p
            if test(p + 10):
                ma.append(p + 10)
            if special_eat(p + 11):
                ma.append(p + 11)
            if special_eat(p + 9):
                ma.append(p + 9)
            if p // 10 == 1 and test(p + 10) and test(p + 20):  # 兵的第一步
                ma.append(p + 20)
        if self.typ in (0, 5):  # pao
            p = self.p + 1
            while test(p):
                ma.append(p)
                p += 1
            if test2(p):
                p += 1
                while test(p):
                    p += 1
                if special_eat(p):
                    ma.append(p)
            p = self.p + 10
            while test(p):
                ma.append(p)
                p += 10
            if test2(p):
                p += 10
                while test(p):
                    p += 10
                if special_eat(p):
                    ma.append(p)
            p = self.p - 1
            while test(p):
                ma.append(p)
                p += -1
            if test2(p):
                p += -1
                while test(p):
                    p += -1
                if special_eat(p):
                    ma.append(p)
            p = self.p - 10
            while test(p):
                ma.append(p)
                p += -10
            if test2(p):
                p += -10
                while test(p):
                    p += -10
                if special_eat(p):
                    ma.append(p)
        self.ma = ma
        return ma
    
    
    
    def get_protect(self):
        test2 = self.beach.valid
        test = self.beach.not_occupied
        eat = self._not_mine
        special_eat = self._enemy_occupied
        protect = []  # protected positions

        if self.typ in (1, 8, 11, 0):  # 直走
            p = self.p + 1
            while test(p):
                protect.append(p)
                p += 1
            if test2(p):
                protect.append(p)
            p = self.p - 1
            while test(p):
                protect.append(p)
                p += -1
            if test2(p):
                protect.append(p)
            p = self.p + 10
            while test(p):
                protect.append(p)
                p += 10
            if test2(p):
                protect.append(p)
            p = self.p - 10
            while test(p):
                protect.append(p)
                p += -10
            if test2(p):
                protect.append(p)
        if self.typ in (10, 11):  # 斜走的走子
            p = self.p + 11
            while test(p):
                protect.append(p)
                p += 11
            if test2(p):
                protect.append(p)
            p = self.p - 11
            while test(p):
                protect.append(p)
                p += -11
            if test2(p):
                protect.append(p)
            p = self.p + 9
            while test(p):
                protect.append(p)
                p += 9
            if test2(p):
                protect.append(p)
            p = self.p - 9
            while test(p):
                protect.append(p)
                p += -9
            if test2(p):
                protect.append(p)
        if self.typ in (0, 2):  # 有马腿马
            p = self.p
            if test(p + 1):  # 马腿处子的判断
                if test2(p + 12):  # 落点吃子判断
                    protect.append(p + 12)
                if test2(p - 8):
                    protect.append(p - 8)
            if test(p - 1):
                if test2(p - 12):
                    protect.append(p - 12)
                if test2(p + 8):
                    protect.append(p + 8)
            if test(p + 10):
                if test2(p + 21):
                    protect.append(p + 21)
                if test2(p + 19):
                    protect.append(p + 19)
            if test(p - 10):
                if test2(p - 21):
                    protect.append(p - 21)
                if test2(p - 19):
                    protect.append(p - 19)
        if self.typ == 9:  # 无马腿马
            p = self.p
            if test2(p + 1):  # 马腿处子的判断
                if test2(p + 12):  # 落点吃子判断
                    protect.append(p + 12)
                if test2(p - 8):
                    protect.append(p - 8)
            if test2(p - 1):
                if test2(p - 12):
                    protect.append(p - 12)
                if test2(p + 8):
                    protect.append(p + 8)
            if test2(p + 10):
                if test2(p + 21):
                    protect.append(p + 21)
                if test2(p + 19):
                    protect.append(p + 19)
            if test2(p - 10):
                if test2(p - 21):
                    protect.append(p - 21)
                if test2(p - 19):
                    protect.append(p - 19)
        if self.typ in (0, 3):  # xiang
            p = self.p
            if test(p + 11):  # xiang腿处子的判断
                if test2(p + 22):  # 落点吃子判断
                    protect.append(p + 22)
            if test(p - 11):
                if test2(p - 22):
                    protect.append(p - 22)
            if test(p + 9):
                if test2(p + 18):
                    protect.append(p + 18)
            if test(p - 9):
                if test2(p - 18):
                    protect.append(p - 18)
        if self.typ in (0, 4, 12,3):  # shi king
            p = self.p
            if test2(p - 11):
                protect.append(p - 11)
            if test2(p + 11):
                protect.append(p + 11)
            if test2(p - 9):
                protect.append(p - 9)
            if test2(p + 9):
                protect.append(p + 9)
        if self.typ == 6:  # shuai
            p = self.p
            if not p % 10 == 3 and test2(p - 1):
                protect.append(p - 1)
            if not p % 10 == 5 and test2(p + 1):
                protect.append(p + 1)
            if not p // 10 == 6 and test2(p - 10):
                protect.append(p - 10)
            if not p // 10 == 8 and test2(p + 10):
                protect.append(p + 10)

            p = self.p - 10
            while test(p):
                p += -10
                if test2(p) and not self.beach[p]==None:
                    if self.beach[p].typ==12:
                        protect.append(p)
        if self.typ == 7:  # bingo
            p = self.p
            if not p % 10 == 0 and test2(p - 1) :
                protect.append(p - 1)
            if not p % 10 == 8 and test2(p + 1) :
                protect.append(p + 1)
            if not p // 10 == 0 and test2(p - 10):
                protect.append(p - 10)
        if self.typ == 12:  # king
            p = self.p
            if not p // 10 == 8 and test2(p + 10):
                protect.append(p + 10)
            if not p % 10 == 0 and test2(p - 1):
                protect.append(p - 1)
            if not p % 10 == 8 and test2(p + 1):
                protect.append(p + 1)
            if not p // 10 == 0 and test2(p - 10):
                protect.append(p - 10)
        if self.typ == 13:  # pawn
            p = self.p
            if test2(p + 11):
                protect.append(p + 11)
            if test2(p + 9):
                protect.append(p + 9)
        if self.typ in (0, 5):  # pao
            p = self.p + 1
            while test(p):
                p += 1
            if test2(p):
                p += 1
                while test(p):
                    protect.append(p)
                    p += 1
                if test2(p):
                    protect.append(p)
            p = self.p + 10
            while test(p):
                p += 10
            if test2(p):
                p += 10
                while test(p):
                    protect.append(p)
                    p += 10
                if test2(p):
                    protect.append(p)
            p = self.p - 1
            while test(p):
                p += -1
            if test2(p):
                p += -1
                while test(p):
                    protect.append(p)
                    p += -1
                if test2(p):
                    protect.append(p)
            p = self.p - 10
            while test(p):
                p += -10
            if test2(p):
                p += -10
                while test(p):
                    protect.append(p)
                    p += -10
                if test2(p):
                    protect.append(p)
        self.protect = protect
        return protect
    
    

    def move(self, p):
        """对该子在beach中实施移动，包括吃子，不校验能否走到"""
        if self.beach[p] is not None:  # 吃子
            self.beach[p].alive = False  # 你死
            self.beach.set_son(None, p)  # 你走
        self.beach.set_son(None, self.p)  # 我走
        self.beach.set_son(self, p)  # 我来
        self.p = p  # 我动
