"""
-*- coding: utf-8 -*-
@Time    : 2025-03-31
@Github  : windbell0711/BingGo
@Author  : mimi
@License : Apache 2.0
@File    : FSF.py
"""
from __future__ import annotations
import json
import os
import sys
import warnings
import random
from typing import Any

import pyffish

import chess.uci
from chess.uci import GoCommand

def pos(s: str) -> int:  # len(s)=2
    return ord(s[0])-97 + (9-int(s[1]))*10

ALP = "abcdefghi"
def posl(intp: int) -> str:
    return ALP[intp % 10] + str(9 - intp // 10)

def s2l(l: str) -> str:
    """binggo中logs转化为pgn"""
    aaaaa = '['+l.replace("(", "[").replace(")", "]")+']'
    a = json.loads(aaaaa)
    r = ""
    for i in a:
        pf = -1
        pro = ''
        for ii in i:
            if ii[0] == 0:
                pf, pt = ii[1], ii[2]
            elif ii[0] == 1:
                pro = 'm' if ii[1]==0 else 'q'
        if pf == -1:  raise ValueError(str(ii)+"无移动操作")
        r += posl(pf)+posl(pt)+pro
    return r

def l2s(b: list[bool], s: str) -> list:
    beach = b
    ret = []
    li = s.split(' ')
    for i in li:
        a = []
        pf, pt = pos(i[0:2]), pos(i[2:4])
        if beach[pt] == True:
            a.append([2, pt, pt])  #sha
        a.append([0, pf, pt])  #yi
        if i[-1] == 'm' or i[-1]=='q':
            a.append([2, pt, pt])  #sheng
            a.append([1, 11 if i[-1]=='q' else 0, pt])  #sheng
        beach[pf] = False
        beach[pt] = True
        ret.append(a)
    return ret

class GoPerftCommand(GoCommand):
    def __init__(self, perft,
             searchmoves: Any = None,
             ponder: bool = False,
             wtime: Any = None,
             btime: Any = None,
             winc: Any = None,
             binc: Any = None,
             movestogo = None,
             depth: Any = None,
             nodes: Any = None,
             mate: Any = None,
             movetime: Any = None,
             infinite: bool = False):
        super().__init__(searchmoves, ponder, wtime, btime, winc, binc, movestogo, depth, nodes, mate, movetime, infinite)

        # 重新构建命令行参数，包含perft参数
        builder = []
        builder.append("go")

        # 处理父类的参数
        if searchmoves:
            builder.append("searchmoves")
            for move in searchmoves:
                builder.append(move.uci())
        if ponder:
            builder.append("ponder")
        if wtime is not None:
            builder.append(f"wtime {int(wtime)}")
        if btime is not None:
            builder.append(f"btime {int(btime)}")
        if winc is not None:
            builder.append(f"winc {int(winc)}")
        if binc is not None:
            builder.append(f"binc {int(binc)}")
        if movestogo is not None and movestogo > 0:
            builder.append(f"movestogo {int(movestogo)}")
        if depth is not None:
            builder.append(f"depth {int(depth)}")
        if nodes is not None:
            builder.append(f"nodes {int(nodes)}")
        if mate is not None:
            builder.append(f"mate {int(mate)}")
        if movetime is not None:
            builder.append(f"movetime {int(movetime)}")
        if infinite:
            builder.append("infinite")

        # 添加perft参数
        if perft is not None:
            builder.append(f"perft {perft}")

        self.buf = " ".join(builder)

    def uci_info(self, info):
        """处理引擎返回的info消息，收集节点统计信息"""
        pass

    def execute(self, engine):
        for info_handler in engine.info_handlers:
            info_handler.on_go()

        engine.bestmove = None
        engine.ponder = None
        engine.Mmove_received.clear()
        engine.Mmoves.clear()

        engine.send_line(self.buf)
        engine.Mmove_received.wait()
        self.set_result(engine.Mmoves)


class EngineIO:
    def __init__(self):
        self.start_pos = None
        self.moves = None
        self.variant = None
        self.engine = None  # 改为单个引擎实例
        self.info_handler = None  # 对应的单个信息处理器

    def init_engine(self, engine_path, engine_options: dict, config, variant, book_path=""):  # 参数改为单个路径和配置
        """初始化单个引擎和信息处理器"""
        self.engine = None
        self.info_handler: chess.uci.InfoHandler = None

        if not os.path.exists(engine_path):
            sys.exit(f"{engine_path} does not exist.")
        self.engine = chess.uci.popen_engine(engine_path)

        self.engine.uci()
        if config:
            self.engine.setoption({"VariantPath": config})
        self.engine.setoption({"UCI_Variant": variant})
        self.variant = variant
        self.engine.setoption(engine_options)

        ih = chess.uci.InfoHandler()
        self.info_handler = ih
        self.engine.info_handlers.append(ih)

        self.book = book_path
        if self.book:
            self.init_book()
        else:
            self.fens = []

        for o in engine_options:
            pyffish.set_option(o, engine_options[o])
        pyffish.set_option("VariantPath", config)
        pyffish.set_option("UCI_Variant", variant)

    def reset_engine(self):
        """重置引擎状态"""
        if self.engine:
            self.engine.ucinewgame()
            self.engine.setoption({"clear hash": True, "UCI_Variant": self.variant})


    def go(self, **kwargs):
        e:chess.uci.Engine = self.engine
        self.send_moves()
        bestmove = e.go(**kwargs)
        # self.moves.append(bestmove.bestmove)
        return bestmove


    def init_book(self):
        assert self.book
        if self.book is True:
            bookfile = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "books", f"{self.variant}.epd")
            )
        elif self.book:
            bookfile = os.path.abspath(self.book)

        if os.path.exists(bookfile):
            with open(bookfile) as f:
                self.fens = [line.rstrip(';\n') for line in f]
        else:
            warnings.warn(f"{bookfile} does not exist. Using starting position.")

    def init_game(self):
        self.moves = []
        self.reset_engine()  # 补充参数
        self.start_pos = random.choice(self.fens) if self.fens else "startpos"

    def get_possible_moves(self, perft=1):
        print(self.moves)
        if self.moves:
            temp = self.moves.pop()
            self.send_moves()
            self.moves.append(temp)
        # 发送带perft参数的命令
        command = GoPerftCommand(perft=perft)
        moves = self.engine._queue_command(command, async_callback=True)
        return moves

    def send_moves(self):
        self.engine.send_line("position " + self.start_pos + " moves " + " ".join(self.moves))