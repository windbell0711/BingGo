"""
-*- coding: utf-8 -*-
@Time    : 2025-01-22
@Github  : windbell0711/BingGo
@Author  : Lilold333
@License : Apache 2.0
@File    : intelligence.py
"""
import random
import copy
import config

AI_DEPTH = config.AI_DEPTH

def fro(x,y):
    return x
def target(x,y):
    return y

def in_different_camp(typ1,typ2):
    if typ1<8 and typ2>7:
        return True
    elif typ2<8 and typ1>7:
        return  True
    else:
        return False
        
def valid(p):
    if 0<=p<=88 and p%10 != 9:
        return True
    return False


    


class Intelligence:
    def __init__(self, beach, mycamp):
        self.beach = beach
        self.mycamp = mycamp

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
                    if i.typ in (8,9,10,11):
                        self.Iattackable.append(i.p)
                    if i.typ == 8 or i.typ == 11:
                        self.rook.append(i.p)
                else:
                    self.Chn += i.get_ma()
                    if i.typ in (1,2,5):
                        self.Cattackable.append(i.p)
                    if i.typ==1:
                        self.che.append(i.p)

    def reset_attack_pose(self):
        self.Chn = []
        self.Intl = []
        self.king_p = 90
        self.shuai_p = 90
        self.Cattackable=[]
        self.Iattackable = []
        self.rook=[]
        self.che=[]

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
    pms = []  # possible moves
    value=[]
    Cattackable=[]
    Iattackable=[]
    rook=[]
    che=[]
    value_0 = [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
               10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
               10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
               10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
               10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
               10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
               10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4,
               10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4,
               10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4,
               ]
    value_1 = [5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6,
               5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6, 5.6,
               5.2, 5.3, 5.3, 5.3, 5.3, 5.3, 5.3, 5.3, 5.2, 5.2,
               5.2, 5.3, 5.3, 5.3, 5.3, 5.3, 5.3, 5.3, 5.2, 5.2,
               5.2, 5.3, 5.3, 5.3, 5.3, 5.3, 5.3, 5.3, 5.2, 5.2,
               5.2, 5.3, 5.3, 5.3, 5.3, 5.3, 5.3, 5.3, 5.2, 5.2,
               5.2, 5.2, 5.2, 5.2, 5.2, 5.2, 5.2, 5.2, 5.2, 5.2,
               5.2, 5.2, 5.2, 5.2, 5.2, 5.2, 5.2, 5.2, 5.2, 5.2,
               5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
               ]
    value_2 = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               2.0, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.0, 2.0,
               2.0, 2.1, 2.2, 2.2, 2.2, 2.2, 2.2, 2.1, 2.0, 2.0,
               2.0, 2.1, 2.2, 2.2, 2.2, 2.2, 2.2, 2.1, 2.0, 2.0,
               2.0, 2.1, 2.2, 2.2, 2.2, 2.2, 2.2, 2.1, 2.0, 2.0,
               2.0, 2.1, 2.2, 2.2, 2.2, 2.2, 2.2, 2.1, 2.0, 2.0,
               2.0, 2.1, 2.2, 2.2, 2.2, 2.2, 2.2, 2.1, 2.0, 2.0,
               2.0, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.0, 2.0,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               ]
    value_3 = [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2,
               1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2,
               1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2,
               1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2,
               1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2,
               1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               ]
    value_4 = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
               1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
               1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
               1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
               1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
               1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
               1.5, 1.5, 1.5, 3.0, 3.0, 3.0, 1.5, 1.5, 1.5, 3.0,
               1.5, 1.5, 1.5, 3.0, 3.0, 3.0, 1.5, 1.5, 1.5, 3.0,
               1.5, 1.5, 1.5, 3.0, 3.0, 3.0, 1.5, 1.5, 1.5, 3.0,
               ]
    value_5 = [3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6,
               3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6,
               3.2, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.2, 3.2,
               3.2, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.2, 3.2,
               3.2, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.2, 3.2,
               3.2, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.2, 3.2,
               3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2,
               3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2,
               3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
               ]
    value_6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               ]
    value_7 = [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5,
               2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5,
               2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               ]
    value_8 = [-5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0,
               -5.2, -5.2, -5.2, -5.2, -5.2, -5.2, -5.2, -5.2, -5.2, -5.2,
               -5.2, -5.2, -5.2, -5.2, -5.2, -5.2, -5.2, -5.2, -5.2, -5.2,
               -5.2, -5.3, -5.3, -5.3, -5.3, -5.3, -5.3, -5.3, -5.2, -5.2,
               -5.2, -5.3, -5.3, -5.3, -5.3, -5.3, -5.3, -5.3, -5.2, -5.2,
               -5.2, -5.3, -5.3, -5.3, -5.3, -5.3, -5.3, -5.3, -5.2, -5.2,
               -5.2, -5.3, -5.3, -5.3, -5.3, -5.3, -5.3, -5.3, -5.2, -5.2,
               -5.6, -5.6, -5.6, -5.6, -5.6, -5.6, -5.6, -5.6, -5.6, -5.6,
               -5.6, -5.6, -5.6, -5.6, -5.6, -5.6, -5.6, -5.6, -5.6, -5.6,
               ]
    value_9 =[-2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0,
             -2.0, -2.1, -2.1, -2.1, -2.1, -2.1, -2.1, -2.1, -2.0, -2.0,
             -2.0, -2.1, -2.4, -2.4, -2.4, -2.4, -2.4, -2.1, -2.0, -2.0,
             -2.0, -2.1, -2.4, -2.4, -2.4, -2.4, -2.4, -2.1, -2.0, -2.0,
             -2.0, -2.1, -2.4, -2.4, -2.4, -2.4, -2.4, -2.1, -2.0, -2.0,
             -2.0, -2.1, -2.4, -2.4, -2.4, -2.4, -2.4, -2.1, -2.0, -2.0,
             -2.0, -2.1, -2.4, -2.4, -2.4, -2.4, -2.4, -2.1, -2.0, -2.0,
             -2.0, -2.1, -2.1, -2.1, -2.1, -2.1, -2.1, -2.1, -2.0, -2.0,
             -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0,
             ]
    value_10 =[-3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0,
               -3.2, -3.2, -3.2, -3.2, -3.2, -3.2, -3.2, -3.2, -3.2, -3.2,
               -3.2, -3.2, -3.2, -3.2, -3.2, -3.2, -3.2, -3.2, -3.2, -3.2,
               -3.2, -3.3, -3.3, -3.3, -3.3, -3.3, -3.3, -3.3, -3.2, -3.2,
               -3.2, -3.3, -3.3, -3.3, -3.3, -3.3, -3.3, -3.3, -3.2, -3.2,
               -3.2, -3.3, -3.3, -3.3, -3.3, -3.3, -3.3, -3.3, -3.2, -3.2,
               -3.2, -3.3, -3.3, -3.3, -3.3, -3.3, -3.3, -3.3, -3.2, -3.2,
               -3.6, -3.6, -3.6, -3.6, -3.6, -3.6, -3.6, -3.6, -3.6, -3.6,
               -3.6, -3.6, -3.6, -3.6, -3.6, -3.6, -3.6, -3.6, -3.6, -3.6,
               ]
    value_11 = [-10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0,
               -10.2, -10.2, -10.2, -10.2, -10.2, -10.2, -10.2, -10.2, -10.2, -10.2,
               -10.2, -10.2, -10.2, -10.2, -10.2, -10.2, -10.2, -10.2, -10.2, -10.2,
               -10.2, -10.3, -10.3, -10.3, -10.3, -10.3, -10.3, -10.3, -10.2, -10.2,
               -10.2, -10.3, -10.3, -10.3, -10.3, -10.3, -10.3, -10.3, -10.2, -10.2,
               -10.2, -10.3, -10.3, -10.3, -10.3, -10.3, -10.3, -10.3, -10.2, -10.2,
               -10.2, -10.3, -10.3, -10.3, -10.3, -10.3, -10.3, -10.3, -10.2, -10.2,
               -10.6, -10.6, -10.6, -10.6, -10.6, -10.6, -10.6, -10.6, -10.6, -10.6,
               -10.6, -10.6, -10.6, -10.6, -10.6, -10.6, -10.6, -10.6, -10.6, -10.6,
               ]
    value_12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               ]
    value_13 = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
               -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
               -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2,
               -1.2, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.3, -1.2, -1.2,
               -1.4, -1.4, -1.4, -1.4, -1.4, -1.4, -1.4, -1.4, -1.4, -1.4,
               -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5,
               -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5,
               -1.6, -1.6, -1.6, -1.6, -1.6, -1.6, -1.6, -1.6, -1.6, -1.6,
               -1.6, -1.6, -1.6, -1.6, -1.6, -1.6, -1.6, -1.6, -1.6, -1.6,
               ]

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

    def get_quick_beach(self, beach):
        quick_beach = []
        for i in beach:
            if i == None:
                quick_beach.append(None)
            else:
                quick_beach.append(i.typ)
        return quick_beach

    def king_win(self, beach):
        shuai_p = beach.index(6)
        pms = self.get_possible_moves(beach, True)[:]
        for move in pms:
            new_beach = self.make_move(move, beach)[:]
            if shuai_p not in self.get_possible_moves(new_beach, False)[:]:
                return False
        return True

    def shuai_win(self, beach):
        king_p = beach.index(12)
        pms = self.get_possible_moves(beach, False)[:]
        for move in pms:
            new_beach = self.make_move(move, beach)[:]
            if king_p not in self.get_possible_moves(new_beach, True)[:]:
                return False
        return True
    

    def get_ma(self, typ, pf, beach):
        ma=[]
        if typ in (1, 8, 11, 0):# 直走
            for a in (1,-1,10,-10):
                p = pf + a
                while valid(p) and beach[p]==None:
                    ma.append(p)
                    p += a
                if valid(p) and in_different_camp(beach[p],typ):
                    ma.append(p)
            
        if typ in (10, 11):  # 斜走的走子
            for a in (9, -9, 11, -11):
                p = pf + a
                while valid(p) and beach[p]==None:
                    ma.append(p)
                    p += a
                if valid(p) and in_different_camp(beach[p], typ):
                    ma.append(p)
        if typ in (0, 2):  # 有马腿马
            p = pf
            if valid(p + 1) and beach[p+1]==None:  # 马腿处子的判断
                if valid(p+12) and ( beach[p+12] == None or in_different_camp(beach[p+12], typ)):  # 落点吃子判断
                    ma.append(p + 12)
                if valid(p-8) and ( beach[p-8] == None or in_different_camp(beach[p-8], typ)):
                    ma.append(p - 8)
            if valid(p - 1) and beach[p-1]==None:
                if valid(p-12) and ( beach[p-12] == None or in_different_camp(beach[p-12], typ)):
                    ma.append(p - 12)
                if valid(p+8) and ( beach[p+8] == None or in_different_camp(beach[p+8], typ)):
                    ma.append(p + 8)
            if valid(p + 10) and beach[p+10]==None:
                if valid(p+21) and ( beach[p+21] == None or in_different_camp(beach[p+21], typ)):
                    ma.append(p + 21)
                if valid(p+19) and ( beach[p+19] == None or in_different_camp(beach[p+19], typ)):
                    ma.append(p + 19)
            if valid(p - 10) and beach[p-10]==None:
                if valid(p-21) and ( beach[p-21] == None or in_different_camp(beach[p-21], typ)):
                    ma.append(p - 21)
                if valid(p-19) and ( beach[p-19] == None or in_different_camp(beach[p-19], typ)):
                    ma.append(p - 19)
        if typ == 9:  # 无马腿马
            p = pf
            if valid(p + 1):  # 马腿处子的判断
                if valid(p+12) and ( beach[p + 12] == None or in_different_camp(beach[p + 12], typ)):  # 落点吃子判断
                    ma.append(p + 12)
                if valid(p-8) and ( beach[p - 8] == None or in_different_camp(beach[p - 8], typ)):
                    ma.append(p - 8)
            if valid(p - 1):
                if valid(p-12) and ( beach[p - 12] == None or in_different_camp(beach[p - 12], typ)):
                    ma.append(p - 12)
                if valid(p+8) and ( beach[p + 8] == None or in_different_camp(beach[p + 8], typ)):
                    ma.append(p + 8)
            if valid(p + 10):
                if valid(p+21) and ( beach[p + 21] == None or in_different_camp(beach[p + 21], typ)):
                    ma.append(p + 21)
                if valid(p+19) and ( beach[p + 19] == None or in_different_camp(beach[p + 19], typ)):
                    ma.append(p + 19)
            if valid(p - 10):
                if valid(p-21) and ( beach[p - 21] == None or in_different_camp(beach[p - 21], typ)):
                    ma.append(p - 21)
                if valid(p-19) and ( beach[p - 19] == None or in_different_camp(beach[p - 19], typ)):
                    ma.append(p - 19)
        if typ in (0, 3):  # xiang
            for a in (9,-9,11,-11):
                p = pf
                if valid(p + a) and beach[p+a]==None:  # xiang腿处子的判断
                    if valid(p + 2*a) and (beach[p + 2*a] == None or in_different_camp(beach[p + 2*a], typ)):  # 落点吃子判断
                        ma.append(p + 2*a)
        if typ in (0, 4, 12,3):  # shi king
            for a in (9, -9, 11, -11):
                p = pf
                if valid(p + a) and (beach[p + a] == None or in_different_camp(beach[p + a], typ)):  # 落点吃子判断
                    ma.append(p + a)
        if typ == 6:  # shuai

            p = pf
            if not p % 10 == 3 and ( beach[p - 1] == None or in_different_camp(beach[p - 1], typ)):
                ma.append(p - 1)
            if not p % 10 == 5 and ( beach[p + 1] == None or in_different_camp(beach[p + 1], typ)):
                ma.append(p + 1)
            if not p // 10 == 6 and ( beach[p - 10] == None or in_different_camp(beach[p - 10], typ)):
                ma.append(p - 10)
            if not p // 10 == 8 and ( beach[p + 10] == None or in_different_camp(beach[p + 10], typ)):
                ma.append(p + 10)

            for a in (10,-10,1,-1):
                p = pf + a
                while valid(p) and beach[p]==None:
                    p += a
                if valid(p) and beach[p]==12:
                    ma.append(p)

        if typ == 7:  # bingo
            p = pf
            if not p % 10 == 0 and ( beach[p-1] == None or in_different_camp(beach[p-1], typ)) :
                ma.append(p - 1)
            if not p % 10 == 8 and ( beach[p+1] == None or in_different_camp(beach[p+1], typ)):
                ma.append(p + 1)
            if not p // 10 == 0 and ( beach[p-10] == None or in_different_camp(beach[p-10], typ)):
                ma.append(p - 10)

        if typ in (12,4):  # king
            p = pf
            if not p // 10 == 8 and ( beach[p+10] == None or in_different_camp(beach[p+10], typ)):
                ma.append(p + 10)
            if not p % 10 == 0 and ( beach[p-1] == None or in_different_camp(beach[p-1], typ)):
                ma.append(p - 1)
            if not p % 10 == 8 and ( beach[p+1] == None or in_different_camp(beach[p+1], typ)):
                ma.append(p + 1)
            if not p // 10 == 0 and ( beach[p-10] == None or in_different_camp(beach[p-10], typ)):
                ma.append(p - 10)
        if typ == 13:  # pawn
            p = pf
            if beach[p + 10]==None:
                ma.append(p + 10)
            if beach[p + 11]!=None and in_different_camp(beach[p+11], typ):
                ma.append(p + 11)
            if beach[p + 9]!=None and in_different_camp(beach[p+9], typ):
                ma.append(p + 9)
            if p // 10 == 1 and beach[p + 10]==None and beach[p + 20]==None:  # 兵的第一步
                ma.append(p + 20)

        if typ in (0, 5):  # pao
            for a in (1,-1,10,-10):
                p = pf + a
                while valid(p) and beach[p]==None:
                    ma.append(p)
                    p += a
                if valid(p):
                    p += a
                    while valid(p) and beach[p]==None:
                        p += a
                    if valid(p) and in_different_camp(beach[p], typ):
                        ma.append(p)
        ma = list(set(ma))
        return ma

    def evaluate(self, beach):
        if 6 not in beach:
            return -10000
        if 12 not in beach:
            return 10000
        value=0
        p=-1
        for i in beach:
            p+=1
            if i!=None:
                value += self.value_dict.get(i)[p]
        return value


    def make_move(self, move, beach):
        if beach[move[0]] == 7 and move[1] // 10 == config.PROMOTION_DISTANCE:  # 兵升变
            beach[move[0]] = None
            beach[move[1]] = 0
        elif beach[move[0]] == 13 and move[1] // 10 == 8:  # 另一个兵升变
            beach[move[0]] = None
            beach[move[1]] = 11
        else:
            beach[move[1]] = beach[move[0]]
            beach[move[0]] = None
        return beach

    def is_good_move(self,move,beach):
        beach2=beach[:]
        new_beach=self.make_move(move,beach2)
        mas=self.get_ma(new_beach[move[1]],move[1],new_beach)
        for ma in mas:
            if new_beach[ma] in (1,2,5,6,8,9,10,11,12):
                return True
        return False

    def get_possible_moves(self, beach, Maxplayer):
        p = -1
        pms = []
        if Maxplayer:
            for i in beach:
                p += 1
                if i != None and i < 8:
                    ma = self.get_ma(i, p, beach)[:]
                    for j in ma:
                        if beach[j]!=None or self.is_good_move((p,j),beach):
                            pms.insert(0,(p,j))
                        else:
                            pms.append((p, j))

        else:
            for i in beach:
                p += 1
                if i != None and i > 7:
                    ma = self.get_ma(i, p, beach)[:]
                    for j in ma:
                        if beach[j] != None  or self.is_good_move((p,j),beach):
                            pms.append((p, j))
                        else:
                            pms.insert(0, (p, j))
        return pms

    def get_attacked_p(self, beach, Maxplayer):
        p = -1
        pms = []
        if Maxplayer:
            for i in beach:
                p += 1
                if i != None and i < 8:
                    ma = self.get_ma(i, p, beach)[:]
                    pms+=ma
        else:
            for i in beach:
                p += 1
                if i != None and i > 7:
                    ma = self.get_ma(i, p, beach)[:]
                    pms+=ma
        return list(set(pms))




    def alpha_beta_search(self, beach, depth, alpha, beta, Maxplayer):
        self.times+=1
        beach2=beach[:]
        if 12 not in beach2:
            return 10000*depth
        if 6 not in beach2:
            return -10000*depth
        if depth == 0:
            return self.evaluate(beach2)
        else:
            beach2 = beach[:]

            if Maxplayer:
                pms = self.get_possible_moves(beach2, True)[:]
                max_value = -1000000
                for move in pms:
                    beach2 = beach[:]
                    new_beach = self.make_move(move, beach2)[:]
                    new_value = round(self.alpha_beta_search(new_beach, depth - 1, alpha, beta, False),1)
                    if new_value > max_value:
                        max_value = new_value
                        if depth == self.d_set:
                            print(move,new_value,self.times)
                            self.finest_value = new_value
                            self.best_move = move

                    alpha = max(alpha, new_value)
                    if alpha >= beta:
                        break
                return max_value
            else:
                pms = self.get_possible_moves(beach2, False)[::-1]
                min_value = 1000000
                for move in pms:
                    beach2=beach[:]
                    new_beach = self.make_move(move, beach2)[:]
                    new_value = round(self.alpha_beta_search(new_beach, depth - 1, alpha, beta, True),1)
                    if new_value < min_value:
                        min_value = new_value
                        if depth == self.d_set:
                            print(move,new_value,self.times)
                            self.best_move = move
                    beta = min(beta, new_value)
                    if beta <= alpha:
                        break
                return min_value

    def get_best_move_Chn(self):
        self.times=0
        quick_beach = self.get_quick_beach(self.beach)[:]
        d = AI_DEPTH
        self.d_set = d
        print('Chn_search started. Value now is',round(self.evaluate(quick_beach),1))
        print('move|value|times')
        self.alpha_beta_search(quick_beach, d, -100000000, 100000000, True)
        print('Done in', self.times, 'moves')

    def get_best_move_Intl(self):
        self.times=0
        quick_beach = self.get_quick_beach(self.beach)[:]
        d = AI_DEPTH
        self.d_set = d
        print('Intl_search started. Value now is',round(self.evaluate(quick_beach),1))
        print('move|value|times')
        self.alpha_beta_search(quick_beach, d, -100000000, 100000000, False)
        print('Done in',self.times,'moves')
