"""
-*- coding: utf-8 -*-
@Time    : 2025-01-22
@Github  : windbell0711/BingGo
@Author  : Lilold333
@License : Apache 2.0
@File    : intelligence.py
"""

class Intelligence:
    def __init__(self, beach, war):
        self.beach = beach
        self.war = war  # 尽量别用self.war哦
        self.mycamp = war.mycamp

        self.Chn = []
        self.Intl = []
        self.king_p = 90
        self.shuai_p = 90

    def get_attack_pose(self):
        self.reset_attack_pose()
        for i in self.beach.pieces:  # 找king
            if i.typ == 12:
                self.king_p = i.p
                break
        for i in (63, 64, 65, 73, 74, 75, 83, 84, 85):  # 找shuai
            if not self.beach[i] is None:
                if self.beach[i].typ == 6:
                    self.shuai_p = i
                    break
        for i in self.beach.pieces:
            if i.alive:
                if i.camp_intl:  # 遍历国际象棋棋子
                    self.Intl += i.get_ma()
                else:
                    self.Chn += i.get_ma()

    def reset_attack_pose(self):
        self.Chn = []
        self.Intl = []
        self.king_p = 90
        self.shuai_p = 90

    def end(self, i, j, k):
        self.beach.virtual_move(i, i.p)
        self.beach.virtual_move(k, j)

    def bgn(self, i, j):
        self.beach.virtual_move(i, j)
        self.beach.virtual_move(None, i.p)
        self.get_attack_pose()

    def king_is_checkmate(self):
        for i in self.beach:
            if i is not None:
                if i.camp_intl:
                    for j in i.get_ma():
                        if j is not None:
                            k = self.beach[j]
                        else:
                            k = None
                        self.bgn(i, j)
                        if self.mycamp == False:
                            if not self.king_p in self.Chn:
                                print(i.p, j)
                                self.end(i, j, k)
                                return False
                        self.end(i, j, k)
        return True

    def shuai_is_checkmate(self):
        for i in self.beach:
            if i is not None:
                if not i.camp_intl:
                    for j in i.get_ma():
                        if j is not None:
                            k = self.beach[j]
                        else:
                            k = None
                        self.bgn(i, j)
                        if self.mycamp == True:
                            if not self.shuai_p in self.Intl:
                                print(i.p, j)
                                self.end(i, j, k)
                                return False
                        self.end(i, j, k)
        return True
