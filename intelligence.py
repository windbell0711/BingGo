"""
-*- coding: utf-8 -*-
@Time    : 2025-01-22
@Github  : windbell0711/BingGo
@Author  : Lilold333
@License : Apache 2.0
@File    : intelligence.py
"""

def fro(x,y):
    return x
def target(x,y):
    return y
import random


class Intelligence:
    def __init__(self, beach, war):
        self.beach = beach
        self.war = war
        self.mycamp = war.mycamp

    Chn = []
    Intl = []
    king_p = 90
    shuai_p = 90

    def get_attack_pose(self):
        self.reset_attack_pose()
        for i in range(0, 89):
            if not self.beach[i] is None:
                if self.beach[i].typ == 12:
                    self.king_p = i
                    break
        for i in (63, 64, 65, 73, 74, 75, 83, 84, 85):
            if not self.beach[i] is None:
                if self.beach[i].typ == 6:
                    self.shuai_p = i
                    break
        for i in self.beach:
            if i is not None:
                if i.camp_intl == True:  # 遍历国际象棋棋子
                    self.Intl += i.get_ma()
                else:
                    self.Chn += i.get_ma()

    def get_attack_pose2(self):
        self.reset_attack_pose()
        for i in range(0, 89):
            if not self.beach[i] is None:
                if self.beach[i].typ == 12:
                    self.king_p = i
                    break
        for i in (63, 64, 65, 73, 74, 75, 83, 84, 85):
            if not self.beach[i] is None:
                if self.beach[i].typ == 6:
                    self.shuai_p = i
                    break
        for i in self.beach:
            if i is not None:
                if i.camp_intl == True:  # 遍历国际象棋棋子
                    self.Intl += i.get_ma()
                    if i.typ in (8,9,10,12):
                        self.Iattackable.append(i.p)
                else:
                    self.Chn += i.get_ma()
                    if i.typ in (1,2,5):
                        self.Cattackable.append(i.p)

    def reset_attack_pose(self):
        self.Chn = []
        self.Intl = []
        self.king_p = 90
        self.shuai_p = 90
        self.Cattackable=[]
        self.Iattackable = []

    def end(self):
        self.beach.virtual_move(self.i, self.i.p)
        self.beach.virtual_move(self.k, self.j)

    def bgn(self):
        self.beach.virtual_move(self.i, self.j)
        self.beach.virtual_move(None, self.i.p)
        self.get_attack_pose()

    def king_is_checkmate(self):
        for self.i in self.beach:
            if not self.i is None:
                if self.i.camp_intl == True:
                    for self.j in self.i.get_ma():
                        if self.j is not None:
                            self.k = self.beach[self.j]
                        else:
                            self.k = None
                        self.bgn()
                        if self.mycamp == False:
                            if not self.king_p in self.Chn:
                                self.end()
                                return False
                        self.end()
        return True

    def shuai_is_checkmate(self):
        for self.i in self.beach:
            if not self.i is None:
                if self.i.camp_intl == False:
                    for self.j in self.i.get_ma():
                        if self.j is not None:
                            self.k = self.beach[self.j]
                        else:
                            self.k = None
                        self.bgn()
                        if self.mycamp == False:
                            if not self.shuai_p in self.Intl:
                                self.end()
                                return False
                        self.end()
        return True

    ptC = []
    ptI = []
    pms=[]#possible moves
    value=[]
    Cattackable=[]
    Iattackable=[]
    value_0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    value_1 = [4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
               4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
               4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
               4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
               4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
               4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
               1, 4, 4, 4, 4, 4, 4, 4, 1, 0,
               2, 2, 2, 3, 1, 3, 2, 2, 2, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    value_2 = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
               3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
               3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
               3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
               3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
               2, 3, 3, 3, 3, 3, 3, 3, 2, 3,
               0, 0, 2, 0, 0, 0, 2, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    value_3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    value_4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 2, 0, 10, 0, 2, 0, 0, 0,
               0, 0, 0, 10, 0, 10, 0, 0, 0, 0, ]
    value_5 = [0, 0, 0, 0, 0, 0, 0, -10, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, -1, -1, 2, 0, -10, 0, 0,
               0, 0, 0, -1, -1, -1, 0, -10, 0, 0,
               0, 0, 0, -1, -1, -1, 0, 0, 0, 0, ]
    value_6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    value_7 = [9, 9, 9, 9, 9, 9, 9, 9, 9, 0,
               8, 8, 8, 8, 8, 8, 8, 8, 8, 0,
               4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
               2, 2, 3, 3, 2, 3, 3, 2, 2, 0,
               1, 0, 2, 0, 1, 0, 2, 0, 1, 0,
               0, 0, -2, 0, 0, 0, -2, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    value_8 = [-1, -1, -1, 1, -1, 1, -1, -1, -1, -1,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2, ]
    value_9 = [0, -1, 0, 0, 0, 0, 0, -1, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    value_10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 2, 0, 0, 0, 0, 0, 2, 0, 0,
               0, 0, 0, 0, 3, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    value_11 = [0, 0, 0, 0, -100, -10, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    value_12 = [-10, -10, -10, -10, 0, 0, -10, -10, -10, 0,
               1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               3, 3, 3, 4, 5, 4, 3, 3, 3, 3,
               4, 5, 6, 7, 8, 7, 6, 5, 4, 4,
               5, 6, 7, 8, 9, 8, 7, 6, 5, 5,
               6, 7, 8, 9, 10, 9, 8, 7, 6, 6,
               0, 0, 10, 20, 30, 20, 10, 0, 0, 0,
               0, 0, 10, 20, 30, 20, 10, 0, 0, 0,]
    value_13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, -3, 0, 0, 0, 0, 0,
               2, 0, 2, 0, 2, 0, 2, 0, 2, 0,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
               5, 4, 5, 5, 5, 5, 5, 5, 5, 5,
               6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
               7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
               10, 10, 10, 10, 10, 10, 10, 10, 10, 10, ]

    value_dict={
        0: value_0,
        1: value_1,
        2: value_2,
        3: value_3,
        4: value_4,
        5: value_5,
        6: value_6,
        7: value_7,
        8: value_8,
        9: value_9,
        10: value_10,
        11: value_11,
        12: value_12,
        13: value_13,
    }
    
    def get_protected_pose(self):
        self.reset_protected_pose()
        for i in self.beach:
            if i is not None:
                if i.camp_intl == False:  # 遍历国际象棋棋子
                    self.ptC += i.get_protect()
                else:
                    self.ptI += i.get_protect()
    def reset_protected_pose(self):
        self.ptC = []
        self.ptI = []
    def estimate_value(self):
        self.value= [0] * 90
        self.get_protected_pose()
        self.get_attack_pose()
        for i in self.beach:
            if not i == None:
                self.value[i.p]=i.value()
        return self.value
    def get_possible_moves_Chn(self):
        self.pms=[]
        self.best_move = None
        self.estimate_value()
        for self.i in self.beach:
            if not self.i is None:
                if self.i.camp_intl == False:
                    for self.j in self.i.get_ma():
                        if self.j is not None:
                            self.k = self.beach[self.j]
                        else:
                            self.k = None
                        self.bgn()
                        if not self.shuai_p in self.Intl:
                            self.end()
                            self.pms.append((self.i.p, self.j))
                        else:
                            self.end()
        A = -10000
        for i in self.pms:
            if not self.beach[target(*i)] == None:
                B = self.value[target(*i)]
            else:
                B = self.value[target(*i)] - 1
            B += (self.value_dict.get(self.beach[fro(*i)].typ)[target(*i)] -
                      self.value_dict.get(self.beach[fro(*i)].typ)[fro(*i)])
            if target(*i) in self.ptI:
                B-= self.value[fro(*i)]
            else:
                o = self.beach[fro(*i)]
                k = self.beach[target(*i)]
                o.p = target(*i)
                self.beach.virtual_move(o, target(*i))
                self.beach.virtual_move(None, fro(*i))
                self.get_attack_pose2()
                if self.king_p in self.Chn:
                    B += 5
                for x in self.Iattackable:
                    if x in self.Chn:
                        B+=1
                o.p = fro(*i)
                self.beach.virtual_move(o, fro(*i))
                self.beach.virtual_move(k, target(*i))
            if fro(*i) in self.Intl:
                B+= self.value[fro(*i)]
            B += random.random()*0.5
            if B>A:
                A = B
                self.best_move = i

    def get_possible_moves_Intl(self):
        self.pms = []
        self.best_move=None
        self.estimate_value()
        for self.i in self.beach:
            if not self.i is None:
                if self.i.camp_intl == True:
                    for self.j in self.i.get_ma():
                        if self.beach[self.j] is not None:
                            self.k = self.beach[self.j]
                        else:
                            self.k = None
                        self.bgn()
                        if not self.king_p in self.Chn:
                            self.end()
                            self.pms.append((self.i.p, self.j))
                        else:
                            self.end()
        A = -10000
        for i in self.pms:
            if not self.beach[target(*i)]==None:
                B = self.value[target(*i)]
            else:
                B = self.value[target(*i)] -1
            B+=(self.value_dict.get(self.beach[fro(*i)].typ)[target(*i)] -
                    self.value_dict.get(self.beach[fro(*i)].typ)[fro(*i)])
            if target(*i) in self.ptC:
                B-= self.value[fro(*i)]
            else:
                o = self.beach[fro(*i)]
                k = self.beach[target(*i)]
                o.p=target(*i)
                self.beach.virtual_move(o, target(*i))
                self.beach.virtual_move(None, fro(*i))
                self.get_attack_pose2()
                if self.shuai_p in self.Intl:
                    B += 10
                for x in self.Cattackable:
                    if x in self.Intl:
                        B+=4
                o.p = fro(*i)
                self.beach.virtual_move(o, fro(*i))
                self.beach.virtual_move(k, target(*i))
            if fro(*i) in self.Chn and fro(*i)!=1:
                B+= self.value[fro(*i)]
            B+=random.random()*0.5
            if B > A:
                A = B
                self.best_move = i
