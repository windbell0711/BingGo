import os
import time

import Utils
from beach import Beach

import pyffish

class FSF:

    def __init__(self):
        self.io = Utils.EngineIO()
        cores = os.cpu_count()
        self.io.init_engine("fairy-stockfish-largeboards_x86-64-bmi2-latest.exe", {"Threads": cores, "Hash": cores*8}, config="zvgv3.ini", variant="zhongxiang_vs_guoxiang")
        self.io.init_game()
        self.io.engine.go(depth=1) #快速获取当前状态
        self.lasts = []

    def get_best_move_Intl(self):
        bm = self.io.go(movetime=100).bestmove
        return Utils.pos(bm[0:2]), Utils.pos(bm[2:])

    def get_best_move_Chn(self):
        bm = self.io.go(movetime=100).bestmove
        return Utils.pos(bm[0:2]), Utils.pos(bm[2:])

    def is_checkmate(self):
        h = self.io.info_handler
        self.get_status()
        if h.info["score"][1].mate == 1:
            return True
        return False

    def regret(self):
        self.lasts += [self.io.moves[-1]]
        self.io.moves.pop()

    def gret(self):
        self.io.moves.append(self.lasts[-1])
        self.lasts.pop()

    def get_status(self, move_now = ""):
        e = self.io.engine
        e.send_line("position " + self.io.start_pos + " moves " + " ".join(self.io.moves + [move_now] if move_now else []))
        e.go(depth=6)
    def get_checked(self, board: Beach, intl: bool):
        # pms = self.io.get_possible_moves().result()
        # intl = not intl
        # for m in pms:
        #     move = Utils.pos(m[2:])
        #     p = board[move]
        #     print(m, move, p)
        #     if p and p.typ == 6:
        #         if not intl:
        #             return 1 # 需要回退一步，因为红方自己走入将杀
        #         return 2 # 黑方将军
        #     if p and p.typ == 12:
        #         if intl:
        #             return 3 # 黑方自己走入将杀
        #         return 4 # 红方将军
        # return 0
        pms = self.io.get_possible_moves().result()
        print(self.io.moves[-1] if self.io.moves else "", pms)
        if self.io.moves and self.io.moves[-1] not in pms:
            if intl:
                return 3 # 黑方自己走入将杀
            return 1 # 红方自己走入将杀

        check = pyffish.gives_check("zhongxiang_vs_guoxiang", self.io.start_pos, self.io.moves)
        if check:
            if intl:
                return 4 # 红方将军
            return 2 # 黑方将军

        return 0