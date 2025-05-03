"""
-*- coding: utf-8 -*-
@Time    : 2025-03-31
@Github  : windbell0711/BingGo
@Author  : mimi
@License : Apache 2.0
@File    : FSF.py
"""
import logging
import os
import time
import re
import Utils
import config
from beach import Beach

import pyffish

class FSF:
    def __init__(self):
        import chess.uci
        chess.uci.LOGGER.setLevel(config.CHESS_LOG)  # 设置chess库日志级别为WARNING

        self.io = Utils.EngineIO()
        cores = os.cpu_count()
        self.io.init_engine("fairy-stockfish-largeboards_x86-64-bmi2-latest.exe", {"Threads": cores, "Hash": cores*8}, config="latest.ini", variant="zhongxiang_vs_guoxiang")
        self.io.init_game()
        self.io.engine.go(depth=1)  # 快速获取当前状态
        self.lasts = []
        self.black_flag = False

    def get_best_move_Intl(self):
        bm = self.io.go(depth=config.AI_DEPTH).bestmove
        if self.is_checkmate():
            return None, None
        return Utils.pos(bm[0:2]), Utils.pos(bm[2:])

    def get_best_move_Chn(self):
        bm = self.io.go(depth=config.AI_DEPTH).bestmove
        if self.is_checkmate():
            return None, None
        logging.debug(bm)
        return Utils.pos(bm[0:2]), Utils.pos(bm[2:])

    def is_checkmate(self):
        h = self.io.info_handler
        self.get_status()
        logging.debug(h.info["score"])
        if h.info["score"][1].mate == 0:
            return True
        return False

    def regret(self):
        self.lasts += [self.io.moves[-1]]
        self.io.moves.pop()
        self.get_status()

    def gret(self):
        self.io.moves.append(self.lasts[-1])
        self.lasts.pop()
        self.get_status()

    def get_status(self, move_now=""):
        e = self.io.engine
        e.send_line("position " + self.io.start_pos + " moves " + " ".join(self.io.moves + ([move_now] if move_now else [])))
        e.go(depth=4)

    def get_checked(self, board: Beach, intl: bool):
        # pms = self.io.get_possible_moves().result()
        # intl = not intl
        # for m in pms:
        #     move = Utils.pos(m[2:])
        #     p = board[move]
        #     logging.debug(f"{m}, {move}, {p}")
        #     if p and p.typ == 6:
        #         if not intl:
        #             return 1  # 需要回退一步，因为红方自己走入将杀
        #         return 2  # 黑方将军
        #     if p and p.typ == 12:
        #         if intl:
        #             return 3  # 黑方自己走入将杀
        #         return 4  # 红方将军
        # return 0
        pms = self.io.get_possible_moves().result()
        logging.debug(str(self.io.moves[-1] if self.io.moves else "") + str(pms))
        if self.is_checkmate():
            if intl:
                return 1  # black_wins
            return 3  # red_wins
        check = pyffish.gives_check("zhongxiang_vs_guoxiang", self.io.start_pos, self.io.moves)
        if check:
            if intl:
                return 4  # 红方将军 jiangjun
            return 2  # 黑方将军 check
        return 0

    def get_cp(self):
        return self.io.info_handler.info["score"][1].cp

    def get_possible_moves_piece(self, piece):
        return [m for m in self.io.get_possible_moves(pop=False).result() if m.startswith(piece)]