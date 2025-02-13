"""
-*- coding: utf-8 -*-
@Time    : 2025-01-24
@Github  : windbell0711/BingGo
@Author  : windbell0711
@Coauthor: Lilold333
@License : Apache 2.0
@File    : war.py
"""
import json

from kivy.clock import Clock

from beach import *
from intelligence import Intelligence



class War:
    def __init__(self, display, args: Tuple):
        self.mycamp_intl = False
        self.display = display
        self.beach = Beach()
        for p in range(90):  # 初始化，注意此处只是和self.display按照一样的规则设置了棋盘，其beach和qizi的地址都不一样，所以无法通过idt或地址交流
            name = config.init_lineup[p]
            if name == " " or name == "|":
                continue
            self.beach.set_son(Qizi(p=p, typ=config.typ_dict[name], beach=self.beach), p)
        self.ai = Intelligence(self.beach, self.mycamp_intl)

        self.active_qizi = None
        self.logs: List[List[Tuple[int, int, int]]] = []  # 走子日志
        self.turn = 0

        self.auto_intl = False
        self.auto_chn = False

        self.SCREEN_POS_x = args[0]
        self.SCREEN_POS_y = args[1]
        # self.SCREEN_POS_a = args[2]
        # self.SCREEN_POS_b = args[3]

    def main(self, p: int, castle=False):
        """将当前棋子移向位置p"""
        moves = []
        if castle:
            if p == 0:
                moves.append((4, 0, 2))
                moves.append((4, 3, 1))
            elif p == 8:
                moves.append((4, 8, 4))
                moves.append((4, 3, 5))
            else:
                raise ValueError("!Wrong p when castling. Received p: " + str(p))
        else:
            if self.beach[p] is not None:
                moves.append((2, self.beach[p].typ, p))
            moves.append((0, self.active_qizi.p, p))
            if self.active_qizi.typ == 13 and 79 < p < 89:  # ♟->♛
                moves.append((2, self.active_qizi.typ, p))
                moves.append((1, 11, p))
            elif self.active_qizi.typ == 7 and 0 <= p < 9:  # 兵 -> 将
                moves.append((2, self.active_qizi.typ, p))
                moves.append((1, 0, p))

        self.display.remove_path()
        # self.display.show_path()
        self.conduct_operations(opers=moves)
        label = self._check()
        self.display.remove_label()
        if not label == "":
            self.display.add_label(label)
        if label == "check" or label == "wangbeijj":
            ms = [self.reverse_operation(m) for m in reversed(moves)]
            moves.extend(ms)
            self.conduct_operations(opers=ms)
        else:
            if self.turn != len(self.logs):
                self.logs = self.logs[:self.turn]
            self.logs.append(moves)
            self.turn += 1
            self.display.turn_label.text = str(self.turn)
            self.mycamp_intl = not self.mycamp_intl
            self.active_qizi = None

        self.display.generate_animation(moves)

        Clock.schedule_once(lambda dt: self.ai_continue(), timeout=0.25)

    def king_win(self):
        if self.ai.shuai_is_checkmate():
            return True
        else:
            return False

    def shuai_win(self):
        if self.ai.king_is_checkmate():
            return True
        else:
            return False


    def ai_move(self):
        self.ai.get_attack_pose()
        if  self.ai.king_p in self.ai.Chn or self.ai.shuai_p in self.ai.Intl:
            print("!游戏已结束")
            return []
        if self.ai.shuai_is_checkmate() or self.ai.king_is_checkmate():
            print("!游戏已结束")
            return []
        if self.mycamp_intl:
            self.ai.get_possible_moves_Intl()  #TODO
            pf, pt = self.ai.best_move
            #pf, pt = AI.get_ai_move(chessboard=self.beach)
        else:
            self.ai.get_possible_moves_Chn()
            pf, pt = self.ai.best_move
        self.active_qizi = self.beach[pf]
        self.main(p=pt)

    def regret(self):
        self.turn -= 1  # 先上一回合再操作
        ms = [self.reverse_operation(m) for m in reversed(self.logs[self.turn])]
        self.conduct_operations(ms)
        # for i in range(len(self.logs[self.turn])-1, -1, -1):  # 倒序重现
        #     self.display_operation(self.reverse_operation(self.logs[self.turn][i]))
        self.mycamp_intl = not self.mycamp_intl
        self.ai.reset_attack_pose()
        self.display.turn_label.text = str(self.turn)
        self.display.generate_animation(ms)

    def gret(self):
        ms = self.logs[self.turn]
        self.conduct_operations(ms)
        self.turn += 1  # 先操作再下一回合
        self.mycamp_intl = not self.mycamp_intl
        self.ai.reset_attack_pose()
        self.display.turn_label.text = str(self.turn)
        self.display.generate_animation(ms)

    def solve_board_press(self, p: int):
        """用户点按棋盘上一点"""
        moves = []
        # label = ""
        # next_turn = False  # 弃用
        # 点选棋子为己方阵营
        if self.beach.occupied(p) and self.beach[p].camp_intl == self.mycamp_intl:
            # 王车易位
            if (self.mycamp_intl and
                self.active_qizi is not None and
                self.active_qizi.typ == 12 and
                self.active_qizi.p == 3 and
                self.beach[p].typ == 8 and
                not self.ai.king_is_checkmate() and
                ((p == 0 and self.beach[1] == self.beach[2] is None) or
                 (p == 8 and self.beach[4] == self.beach[5] == self.beach[6] == self.beach[7] is None))):
                moves = self.main(p=p, castle=True)
            # 重选棋子
            else:
                self.active_qizi = self.beach[p]
        # 点选位置self.active_qizi能走到
        elif self.active_qizi is not None and p in self.active_qizi.get_ma():
            moves = self.main(p=p)
        else:
            print("无法抵达或无法选中", p)

        return moves

    def conduct_operations(self, opers):
        for oper in opers:
            if oper[0] == 0 or oper[0] == 4:
                self.beach.move_son(pfrom=oper[1], pto=oper[2])
            elif oper[0] == 1:
                self.beach.place_son(typ=oper[1], p=oper[2])
            elif oper[0] == 2:
                self.beach.kill_son(p=oper[2])

    def _check(self):  # 是否将军
        self.ai.get_attack_pose()
        if not self.mycamp_intl:
            if self.ai.shuai_p in self.ai.Intl:
                return "check"
            elif self.ai.king_p in self.ai.Chn:
                if self.ai.king_is_checkmate():
                    return "red_wins"
                return "checked"
            return ""
        else:
            if self.ai.king_p in self.ai.Chn:
                return "wangbeijj"
            elif self.ai.shuai_p in self.ai.Intl:
                if self.ai.shuai_is_checkmate():
                    return "black_wins"
                return "jiangjun"
            return ""

    # def ラウンドを終える(self):
    #     self._check()
    #
    #     self.你的回合 = True
    #     self.mycamp_intl = not self.mycamp_intl
    #     self.active_qizi = None

    def ai_continue(self):
        """如果设置了人机对弈，则自动完成下一步"""
        if (self.mycamp_intl and self.auto_intl) or (not self.mycamp_intl and self.auto_chn):
            self.ai_move()
            return True
        return False

    @staticmethod
    def reverse_operation(oper: Tuple[int, int, int]) -> Tuple[int, int, int]:
        if oper[0] == 0 or oper[0] == 4:
            return (oper[0], oper[2], oper[1])
        elif oper[0] == 1:
            return (2, oper[1], oper[2])
        elif oper[0] == 2:
            return (1, oper[1], oper[2])
        else:
            raise ValueError("!Cannot reverse oper: " + str(oper))


if __name__ == '__main__':
    pass
