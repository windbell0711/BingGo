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
        self.mycamp_intl = False  # 我的阵营  False: 中象; True: 国象
        self.ai = Intelligence(self.beach, self.mycamp_intl)

        self.active_qizi = None

        # self.moves = []
        # self.label = ""
        # self.你的回合 = False

    def conduct_operations(self, opers):
        for oper in opers:
            if oper[0] == 0:
                self.beach.move_son(pfrom=oper[1], pto=oper[2])
            elif oper[0] == 1:
                self.beach.place_son(typ=oper[1], p=oper[2])
            elif oper[0] == 2:
                self.beach.kill_son(p=oper[2])

    def solve_board_press(self, p: int):
        """用户点按棋盘上一点"""
        moves = []
        label = ""
        next_turn = False
        # 点选棋子为己方阵营
        if self.beach.occupied(p) and self.beach[p].camp_intl == self.mycamp_intl:
            # 可能是要王车易位
            if self.active_qizi is not None and self.beach[3] is not None and self.mycamp_intl:
                ret, ms = self.castle_move(p)
                if ret:
                    moves.extend(ms)
                    next_turn = True
            # 也可能是重选棋子
            else:
                self.active_qizi = self.beach[p]
        # 点选位置self.active_qizi能走到
        elif self.active_qizi is not None and p in self.active_qizi.get_ma():
            moves.extend(self.simple_move(p))
            next_turn = True
        else:
            print("无法抵达或无法选中", p)

        self.conduct_operations(opers=moves)
        if next_turn:  # 检查一下有没有啥问题
            label = self._check()
            if label == "check" or label == "jiangjun" or label == "wangbeijj":
                self.conduct_operations(opers=reversed(moves))
                moves.extend(reversed(moves))
        return moves, label, next_turn

    def simple_move(self, p):
        """将当前棋子移往指定位置"""
        moves = []
        if self.beach[p] is not None:
            moves.append((2, self.beach[p].typ, p))
        moves.append((0, self.active_qizi.p, p))
        moves.extend(self._promotion(self.active_qizi.p, p))
        return moves

    def castle_move(self, p):
        """王车易位"""
        if self.ai.king_is_checkmate():
            return False, None
        if (p == 0 and self.active_qizi.typ == 12 and self.beach[3].typ == 12 and
                self.beach[1] == self.beach[2] is None and self.beach[p].typ == 8):
            return True, [(0, 0, 2), (0, 3, 1)]
        elif (p == 8 and self.active_qizi.typ == 12 and self.beach[3].typ == 12 and
              self.beach[4] == self.beach[5] == self.beach[6] == self.beach[7] is None and self.beach[p].typ == 8):
            return True, [(0, 8, 4), (0, 3, 5)]
        return False, None

    def _promotion(self, pf, p):  # 是否升变
        if self.beach[pf].typ == 13 and 79 < p < 89:  # ♟->♛
            # self.kill_piece(self.beach[p])
            # self.place_piece(Qizi(p=p, typ=11, beach=self.beach), p=p)
            return [(2, self.beach[pf].typ, p), (1, 11, p)]
        if self.beach[pf].typ == 7 and 0 <= p < 9:  # 兵 -> 将
            # self.kill_piece(self.beach[p])
            # self.place_piece(Qizi(p=p, typ=11, beach=self.beach), p=p)
            return [(2, self.beach[pf].typ, p), (1, 0, p)]
        return []

    def _check(self):  # 是否将军
        self.ai.get_attack_pose()
        if self.mycamp_intl:
            if self.ai.shuai_p in self.ai.Intl:
                return "check"
            elif self.ai.king_p in self.ai.Chn:
                if self.ai.king_is_checkmate():
                    return "red_wins"
                return "check"
            return ""
        else:
            if self.ai.king_p in self.ai.Chn:
                return "wangbeijj"
            elif self.ai.shuai_p in self.ai.Intl:
                if self.ai.shuai_is_checkmate():
                    return "black_wins"
                return "jiangjun"
            return ""

    def ラウンドを終える(self):
        self._check()

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
