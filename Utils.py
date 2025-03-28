import os
import sys
import warnings
import random
import chess.uci

def pos(s: str) -> int:  # len(s)=2
    return ord(s[0])-97 + (9-int(s[1]))*10

class EngineIO:
    def __init__(self):
        self.variant = None
        self.engine = None  # 改为单个引擎实例
        self.info_handler = None  # 对应的单个信息处理器

    def init_engine(self, engine_path, engine_options, config, variant, book_path=""):  # 参数改为单个路径和配置
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

    def reset_engine(self):
        """重置引擎状态"""
        if self.engine:
            self.engine.ucinewgame()
            self.engine.setoption({"clear hash": True, "UCI_Variant": self.variant})


    def go(self, **kwargs):
        e = self.engine
        e.send_line("position " + self.start_pos + " moves " + " ".join(self.bestmoves))
        bestmove = e.go(**kwargs)
        self.bestmoves.append(bestmove.bestmove)
        print(" ".join(self.bestmoves))
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
        self.bestmoves = []
        self.reset_engine()  # 补充参数
        self.start_pos = random.choice(self.fens) if self.fens else "startpos"
        self.bestmoves = []