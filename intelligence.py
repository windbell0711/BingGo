"""
-*- coding: utf-8 -*-
@Time    : 2025-01-22
@Github  : windbell0711/BingGo
@Author  : Lilold333
@License : Apache 2.0
@File    : intelligence.py
"""

def compare(x, y):
    return y - x

class Intelligence:
    def __init__(self, beach, war):
        self.beach = beach
        self.war = war
        self.mycamp = war.mycamp

        self.Chn = []
        self.Intl = []
        self.king_p = 90
        self.shuai_p = 90

    def get_attack_pose(self):
        self.reset_attack_pose()
        for i in range(0, 89):
            if not self.beach[i] is None:
                if self.beach[i].typ == 12:
                    self.king_p = i
                    break
        # print("self.king_p", self.king_p)
        for i in (63, 64, 65, 73, 74, 75, 83, 84, 85):  # 找shuai
            if not self.beach[i] is None:
                if self.beach[i].typ == 6:
                    self.shuai_p = i
                    break
        for i in self.beach:
            if i is not None:
                if i.camp_intl == True:
                    self.Intl += i.get_ma()
                else:
                    self.Chn += i.get_ma()
        pass

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

    ptC = []
    ptI = []
    pms = []  # possible moves

    def get_protected_pose(self):
        self.reset_protected_pose()
        for i in self.beach:
            if i is not None:
                if i.camp_intl:  # 遍历国际象棋棋子
                    self.ptC += i.get_protect()
                else:
                    self.ptI += i.get_protect()

    def reset_protected_pose(self):
        self.ptC = []
        self.ptI = []

    def estimate_value(self):
        self.value = [0] * 90
        self.get_protected_pose()
        for i in self.ptI:
            self.value[i] -= 1
        for i in self.ptC:
            self.value[i] += 1
        for i in self.beach:
            if not i is None:
                self.value[i.p] += i.value()
        print(self.value)
        return self.value

    def get_possible_moves_Chn(self):
        self.pms=[]
        self.best_move = None
        for i in self.beach:
            if not i is None:
                if not i.camp_intl:
                    for j in i.get_ma():
                        if j is not None:
                            k = self.beach[j]
                        else:
                            k = None
                        self.bgn(i, j)
                        if not self.shuai_p in self.Intl:
                            self.end(i, j, k)
                            self.pms.append((i.p, j))
                        else:
                            self.end(i, j, k)
        A = 10000
        for i in self.pms:
            B = compare(*i)
            if B < A:
                A = B
                self.best_move = i

    def get_possible_moves_Intl(self):
        self.pms = []
        self.best_move = None
        for i in self.beach:
            if not i is None:
                if i.camp_intl:
                    for j in i.get_ma():
                        if self.beach[j] is not None:
                            k = self.beach[j]
                        else:
                            k = None
                        self.bgn(i, j)
                        if not self.king_p in self.Chn:
                            self.end(i, j, k)
                            self.pms.append((i.p, j))
                        else:
                            self.end(i, j, k)
        A = -10000
        for i in self.pms:
            B = compare(*i)
            if B > A:
                A = B
                self.best_move = i

        print(self.pms)
