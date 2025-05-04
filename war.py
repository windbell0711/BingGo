"""
-*- coding: utf-8 -*-
@Time    : 2025-01-24
@Github  : windbell0711/BingGo
@Author  : windbell07
@Coauthor: Lilold
@Coauthor: mimi
@License : Apache 2.0
@File    : war.py
"""
import logging
import time

import requests
from typing import Tuple

from kivy.clock import Clock

import Utils
import gists
import history
from FSF import FSF
from Utils import pos2uci
from beach import *
import config


class War:
    def __init__(self, display, args: Tuple):
        self.mycamp_intl = {'chn': False, 'intl': True}[config.ACTIVE_CAMP.lower()]
        self.display = display
        self.beach = Beach()
        for p in range(90):  # 初始化，注意此处只是和self.display按照一样的规则设置了棋盘，其beach和qizi的地址都不一样，所以无法通过idt或地址交流
            name = config.INIT_LINEUP[1:][p]
            if name == " " or name == "|":
                continue
            self.beach.set_son(Qizi(p=p, typ=config.typ_dict[name], beach=self.beach), p)
        self.ai = FSF()
        self.active_qizi = None
        self.logs: List[List[Tuple[int, int, int]]] = []  # 走子日志
        '''
        0 移动+pf+pt
        1 生成+p+你是谁(见config.py的类型typ)
        2 干掉+typ(没用)+p
        就是不管合不合法 所有操作都能做
        '''
        self.turn = 0

        self.move_allowed = True  # 初始化时允许用户操作

        self.auto_intl = False
        self.auto_chn = False

        self.SCREEN_POS_x = args[0]
        self.SCREEN_POS_y = args[1]

        self.is_checkmate = False
        # self.SCREEN_POS_a = args[2]
        # self.SCREEN_POS_b = args[3]
        self.last_cp = None

    def main(self, p: int, castle=False):
        """将当前棋子移向位置p"""
        # if not self.move_allowed:
        #     raise ValueError("!Move not allowed.")
        moves = []
        if castle:
            if p == 0:
                moves.append((4, 0, 2))  # 4: castle
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
            elif self.active_qizi.typ == 7 and p // 10 == config.PROMOTION_DIS:  # 兵 -> 将
                moves.append((2, self.active_qizi.typ, p))
                moves.append((1, 0, p))

        def is_palindrome_list(lst):
            n = len(lst)
            if n < 2:
                return False
            mid = n // 2
            a = lst[mid - 1]
            b = lst[mid]
            return a[1] == b[2] and a[2] == b[1]

        self.ai.io.moves.append(pos2uci(str(moves)))
        self.display.remove_path()
        # self.display.show_path()
        self.conduct_operations(opers=moves)
        label = self.ai.get_checked(self.beach, self.mycamp_intl)
        self.display.remove_label()
        if label > 0:
            # self.display.add_label("将军！" if label in (2, 4) else "将杀！")
            self.display.add_label(("", "black_wins", "check", "red_wins", "jiangjun")[label])
        if self.turn != len(self.logs):
            self.logs = self.logs[:self.turn]
        self.logs.append(moves)
        self.turn += 1
        self.display.turn_label.text = str(self.turn)
        self.mycamp_intl = not self.mycamp_intl
        self.active_qizi = None

        self.display.generate_animation(moves)

        Clock.schedule_once(lambda dt: self.ai_continue(), timeout=0.25)
        Clock.schedule_once(lambda dt: self.gists_continue(), timeout=0.1)
        return moves

    def king_win(self):
        return self.ai.is_checkmate() and not self.mycamp_intl

    def shuai_win(self):
        return self.ai.is_checkmate() and self.mycamp_intl

    def generate_ai_move(self):
        # self.ai.get_attack_pose()
        # if  (self.ai.king_p in self.ai.Chn and self.mycamp_intl == False) or (self.ai.shuai_p in self.ai.Intl and self.mycamp_intl==True):
        #     print("!游戏已结束")
        #     return
        if self.ai.is_checkmate():
            self.is_checkmate = True
        else:
            self.is_checkmate = False
        if self.is_checkmate:
            logging.warning("!游戏已结束")
            return
        if self.mycamp_intl:
            pf, pt = self.ai.get_best_move_Intl()
            # pf, pt = AI.get_ai_move(chessboard=self.beach)
        else:
            pf, pt = self.ai.get_best_move_Chn()
        if pf is None and pt is None:
            logging.warning("!游戏已结束")
            return
        cp = self.ai.get_cp()
        if self.last_cp == cp == 0:  # 和棋
            logging.warning("!游戏已结束")
            return
        self.last_cp = cp
        logging.debug(f"{pf}, {pt}")
        # print(pf, pt, self.beach)
        # for l in self.beach:
        #     print(l)
        self.active_qizi = self.beach[pf]  # TODO:随机的None值，需要修复
        return pt
        # self.main(p=pt)

    def regret(self):
        self.is_checkmate = False
        self.turn -= 1  # 先上一回合再操作
        ms = [self.reverse_operation(m) for m in reversed(self.logs[self.turn])]
        self.conduct_operations(ms)
        # for i in range(len(self.logs[self.turn])-1, -1, -1):  # 倒序重现
        #     self.display_operation(self.reverse_operation(self.logs[self.turn][i]))
        self.mycamp_intl = not self.mycamp_intl
        self.display.turn_label.text = str(self.turn)
        self.display.generate_animation(ms)
        self.ai.get_status()
        self.ai.regret()

    def gret(self):
        ms = self.logs[self.turn]
        self.conduct_operations(ms)
        self.turn += 1  # 先操作再下一回合
        self.mycamp_intl = not self.mycamp_intl
        self.display.turn_label.text = str(self.turn)
        self.display.generate_animation(ms)
        self.ai.get_status()
        self.ai.gret()

    def solve_board_press(self, p: int):
        """用户点按棋盘上一点"""
        moves = []
        # label = ""
        # next_turn = False  # 弃用
        # 点选棋子为己方阵营
        # print((self.beach.occupied(p), self.beach[p].camp_intl, self.mycamp_intl) if self.beach.occupied(p) else self.beach.occupied(p))
        if self.beach.occupied(p) and self.beach[p].camp_intl == self.mycamp_intl:
            # 王车易位
            if (self.mycamp_intl and
                    self.active_qizi is not None and
                    self.active_qizi.typ == 12 and
                    self.active_qizi.p == 3 and
                    self.beach[p].typ == 8 and
                    not self.ai.is_checkmate() and
                    ((p == 0 and self.beach[1] == self.beach[2] is None) or
                     (p == 8 and self.beach[4] == self.beach[5] == self.beach[6] == self.beach[7] is None))):
                moves = self.main(p=p, castle=True)
            # 重选棋子
            else:
                self.active_qizi = self.beach[p]
        # 点选位置self.active_qizi能走到
        elif self.active_qizi is not None and p in Utils.ucis_to_poses(self.beach, self.ai.get_possible_moves_piece(
                Utils.posl(self.active_qizi.p))):
            moves = self.main(p=p)
        else:
            logging.info("无法抵达或无法选中\t" + str(p))
        if moves:
            logging.debug(self.ai.io.moves)
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
        self.ai.get_status()
        if self.ai.io.info_handler.info["score"][1].mate == 1:
            return "red_wins" if self.mycamp_intl else "black_wins"
        else:
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
            if self.move_allowed:
                self.display.ai_move_thread()
                return True
        return False

    def gists_continue(self):
        """如果设置了网络对战，则自动完成下一步"""
        if not config.BATTLE_ONLINE == "off":
            if (config.BATTLE_ONLINE == "chn" and self.mycamp_intl) or \
                    (config.BATTLE_ONLINE == "intl" and not self.mycamp_intl):
                self.display.gists_move_thread()
                return True
        return False

    def get_gists_move(self, username: str):
        gists.send(username, history.format_to_str(self.logs))  # 发送走子过程
        time.sleep(5)
        message = gists.receive(username)
        if message[message.find(':')+2:message.rstrip('|').rfind('|')+1] == history.format_to_str(self.logs):
            # self.logs = history.restore_to_list(message[message.find(':')+2:])
            pass
        else:
            logging.critical(f"警告！接收到的远程消息与本地状态不匹配，程序可能出错，已拒绝对方的走棋！\t{message[message.find(':')+2:message.rstrip('|').rfind('|')+1]} != {history.format_to_str(self.logs)}")
        opers = history.restore_to_list(message[message.find(':')+2:-1])[-1]
        for o in opers:
            if o[0] == 0:
                oper = o
                break
        self.active_qizi = self.beach[oper[1]]
        return oper[2]

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
