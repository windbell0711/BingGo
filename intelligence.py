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
        self.war = war
        self.mycamp = war.mycamp

    Chn = []
    Intl = []
    king_p = 90
    shuai_p = 90

    def get_attack_pose(self):
        self.reset_attack_pose()
        print(self.beach[3])
        for i in range(0, 89):
            if not self.beach[i] is None:
                print(self.beach[i].typ)
                if self.beach[i].typ == 12:
                    self.king_p = i
                    print(i, self.beach[i].p, self.king_p, self.beach[i])
                    break
        for i in (63, 64, 65, 73, 74, 75, 83, 84, 85):
            if not self.beach[i] is None:
                if self.beach[i].typ == 6:
                    self.shuai_p = i
                    print(self.beach[i].p)
                    break
        for i in self.beach:
            if i is not None:
                if i.camp_intl == True:  # 遍历国际象棋棋子
                    self.Intl += i.get_ma()
                else:
                    self.Chn += i.get_ma()

    def reset_attack_pose(self):
        self.Chn = []
        self.Intl = []
        self.king_p = 90
        self.shuai_p = 90

    def end(self):
        self.beach.virtual_move(self.i, self.i.p)
        self.beach.virtual_move(self.k, self.j)

    def bgn(self):
        self.beach.virtual_move(self.i, self.j)
        self.beach.virtual_move(None, self.i.p)
        print(self.beach[3])
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
                        if self.mycamp == True:
                            if not self.king_p in self.Chn:
                                print(self.i.p, self.j)
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
                                print(self.i.p, self.j)
                                self.end()
                                return False
                        self.end()
        return True
