"""
-*- coding: utf-8 -*-
@Time    : 2025-01-24
@Github  : windbell0711/BingGo
@Author  : windbell0711
@Coauthor: Lilold333
@License : Apache 2.0
@File    : war.py
"""
from beach import *
from intelligence import target, Intelligence

class War:
    def __init__(self):
        self.beach = Beach()
        self.active_qizi = None
        self.mycamp_intl = False
        self.ai = Intelligence(self.beach, self.mycamp_intl)

        self.moves = []
        self.label = ""
        self.你的回合 = False

    def solve_board_press(self, p: int):
        """用户点按棋盘上一点"""
        self.moves = []
        self.label = ""
        self.你的回合 = False
        # 点选棋子为己方阵营
        if self.beach.occupied(p) and self.beach[p].camp_intl == self.mycamp_intl:
            # 可能是要王车易位
            if (self.active_qizi is not None and self.beach[3] is not None and self.mycamp_intl and
                    self.castle_move(p)):
                pass
            # 也可能是重选棋子
            else:
                self.active_qizi = self.beach[p]
        # 点选位置self.active_qizi能走到
        elif self.active_qizi is not None and p in self.active_qizi.get_ma():
            self.simple_move(p)
            # self.ラウンドを終える()
        else:
            print("无法抵达或无法选中", p)

    def simple_move(self, p):
        """将当前棋子移往指定位置"""
        self.moves.append((0, self.active_qizi.p, p))
        self._promotion(self.active_qizi.p, p)
        self.ラウンドを終える()

    def castle_move(self, p):
        """王车易位"""
        if self.ai.king_is_checkmate():
            return
        if (p == 0 and self.active_qizi.typ == 12 and self.beach[3].typ == 12 and
                self.beach[1] == self.beach[2] is None and self.beach[p].typ == 8):
            self.moves.append((0, 0, 2))
            self.moves.append((0, 3, 1))
            self.ラウンドを終える()
            return True
        elif (p == 8 and self.active_qizi.typ == 12 and self.beach[3].typ == 12 and
              self.beach[4] == self.beach[5] == self.beach[6] == self.beach[7] is None and self.beach[p].typ == 8):
            self.moves.append((0, 8, 4))
            self.moves.append((0, 3, 5))
            self.ラウンドを終える()
            return True
        return None

    def _promotion(self, pf, p):  # 是否升变
        if self.beach[pf].typ == 13 and 79 < p < 89:  # ♟->♛
            self.moves.append((2, self.beach[pf].typ, p))  # self.kill_piece(self.beach[p])
            self.moves.append((1, 11, p))  # self.place_piece(Qizi(p=p, typ=11, beach=self.beach), p=p)
            return True
        if self.beach[pf].typ == 7 and 0 <= p < 9:  # 兵 -> 将
            self.moves.append((2, self.beach[pf].typ, p))  # self.kill_piece(self.beach[p])
            self.moves.append((1, 0, p))  # self.place_piece(Qizi(p=p, typ=11, beach=self.beach), p=p)
            return True
        return False

    def _check(self):  # 是否将军
        self.ai.get_attack_pose()
        if self.mycamp_intl:
            if self.ai.shuai_p in self.ai.Intl:
                self.label = "check"
                self.moves.extend([reversed(self.moves)])
            elif self.ai.king_p in self.ai.Chn:
                if self.ai.king_is_checkmate():
                    self.label = "red_wins"
                    return
                self.label = "check"
        else:
            if self.ai.king_p in self.ai.Chn:
                self.label = "wangbeijj"
                self.moves.extend([reversed(self.moves)])
            elif self.ai.shuai_p in self.ai.Intl:
                if self.ai.shuai_is_checkmate():
                    self.label = "black_wins"
                    return
                self.label = "jiangjun"

    def ラウンドを終える(self):
        self.你的回合 = True
        self.mycamp_intl = not self.mycamp_intl
        self.active_qizi = None

    @staticmethod
    def reverse_operation(oper: Tuple[int, int, int]) -> Tuple[int, int, int]:
        if oper[0] == 0:
            return (oper[0], oper[2], oper[1])
        elif oper[0] == 1:
            return (2, oper[1], oper[2])
        elif oper[0] == 2:
            return (1, oper[1], oper[2])
        else:
            raise ValueError("!Cannot reverse oper: " + str(oper))


if __name__ == '__main__':
    pass
