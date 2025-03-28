import os

import Utils
from intelligence6 import fro

class FSF:

    def __init__(self):
        self.io = Utils.EngineIO()
        cores = os.cpu_count()
        self.io.init_engine("fairy-stockfish-largeboards_x86-64-bmi2-latest.exe", {"Threads": cores, "Hash": cores*8}, config="zvgv3.ini", variant="zhongxiang_vs_guoxiang")
        self.io.init_game()
        self.lasts = []

    def get_best_move_Intl(self):
        bm = self.io.go(movetime=100).bestmove
        print(bm)
        return Utils.pos(bm[0:2]), Utils.pos(bm[2:])

    def get_best_move_Chn(self):
        bm = self.io.go(movetime=100).bestmove
        return Utils.pos(bm[0:2]), Utils.pos(bm[2:])

    def is_checkmate(self):
        h = self.io.info_handler
        if h.info["score"][1].mate == 1:
            return True
        return False

    def regret(self):
        self.lasts += [self.io.bestmoves[-1]]
        self.io.bestmoves.pop()

    def gret(self):
        self.io.bestmoves.append(self.lasts[-1])
        self.lasts.pop()