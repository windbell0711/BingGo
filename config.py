"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Github  : windbell0711/BingGo
@License : Apache 2.0
@File    : config.py
"""
from __future__ import annotations

from typing import Any, List, Tuple
import configparser

VERSION = '(pre-release) beta-1.2.0'
ACTIVE_QIZI_DELTA_SCALE = 5  # 原大小：65
IMG_STYLE_DEFAULT = 'chn'
typ_dict = {
    "将": 0,
    "车": 1,
    "马": 2,
    "相": 3,
    "士": 4,
    "炮": 5,
    "帅": 6,
    "兵": 7,

    "j": 0,
    "c": 1,
    "m": 2,
    "x": 3,
    "s": 4,
    "p": 5,
    "w": 6,
    "b": 7,

    "城": 8,
    "骑": 9,
    "教": 10,
    "后": 11,
    "王": 12,

    "R": 8,
    "N": 9,
    "B": 10,
    "Q": 11,
    "K": 12,
    "P": 13
}
typ_num2str = {
    0: "j ",
    1: "c ",
    2: "m ",
    3: "x ",
    4: "s ",
    5: "p ",
    6: "w ",
    7: "b ",
    8: "R ",
    9: "N ",
    10: "B ",
    11: "Q ",
    12: "K ",
    13: "P "
}
typ_str2fsf = {
    "R": "r",
    "N": "n",
    "B": "b",
    "Q": "q",
    "K": "k",
    "P": "p",
    "c": "R",
    "x": "X",
    "s": "S",
    "m": "M",
    "p": "L",
    "b": "O",
    "w": "W",
    "j": "J"

}
ALL_PIECE_TYPES = 'jcmxspwbRNBQKP'

def lineup_valid(lineup: str) -> bool:
    """检查布局字符串格式正确"""
    if len(lineup) != 91:  return False
    num_of_line = 9
    for c in lineup:
        if c in ALL_PIECE_TYPES or c == " ":
            num_of_line += 1
        elif c.isdigit():  # 后续版本可能可以用数字代表空格数，但此处由长度拦死，所以不行
            num_of_line += int(c)
        elif c == '|':
            if num_of_line != 9:  return False
            num_of_line = 0
        else:
            return False
    return True

def lineup_to_fen(lineup: str) -> str:
    """布局字符串转化为FEN"""
    fen = ""
    space = 0
    for i in range(1, len(lineup)):
        if lineup[i] == " ":
            space += 1
        else:
            if space != 0:
                fen += str(space)
                space = 0
            if lineup[i] in ALL_PIECE_TYPES:
                fen += typ_str2fsf[lineup[i]]
            elif lineup[i].isdigit():
                fen += lineup[i]
            elif lineup[i] == "|":
                fen += "/"
    return fen[:-1]

def boolean(s: str) -> bool:  # bool()不是期望的作用，为此重新写一个boolean()
    return {'True': True, 'true': True, 'False': False, 'false': False}[s]

# 设置相关信息     {key: [type,   default,  function_valid]}
SETTINGS = {
    "img_style":       [str,    "chn",    lambda s: s in ("intl", "chn", "windows")],
    "quick_cmd_on":    [boolean, True,    lambda x: True],
    "save_when_quit":  [boolean, False,   lambda x: True],
    "init_lineup":     [str,    "|RNBK QNBR|PPPP PPPP|         |         |         |bbb b bbb| p     p |         |cmxswsxmc|", lineup_valid],
    "active_camp":     [str,    "chn",    lambda s: s.lower() in ("intl", "chn")],
    "ai_depth":        [int,     8,       lambda i: 2 <= i <= 18],
    "promotion_dis":   [int,     2,       lambda i: 1 <= i <= 3],
    "screen_scale":    [float,   1.0,     lambda f: 0.25 <= f <= 10],
    "battle_online":   [str,    "off",    lambda s: s in ("off", "chn", "intl")],
    "b_gists_id":      [str,    "notset", lambda s: s.isalnum()],
    "b_gists_access":  [str,    "notset", lambda s: s.isalnum()],
    "username":        [str,    "notset", lambda s: (':' not in s) and s.isprintable()],
    "chess_log":       [int,     20,      lambda i: i in (0, 10, 20, 30, 40, 50)]  # 0-NOTSET; 10-DEBUG; 20-INFO; 30-WARNING; 40-ERROR; 50-CRITICAL
}

def edit_setting(key: str, value: str, file="setting.ini", section="BingGo") -> None:
    """在setting.ini中添加或覆盖"""
    cfe = configparser.RawConfigParser()  # https://blog.csdn.net/weixin_43031092/article/details/109174379
    cfe.optionxform = lambda option: option
    cfe.read(file)
    if section not in cfe:
        cfe.add_section(section)
    cfe.set(section, key, value)
    with open(file=file, mode='w', newline='', encoding='utf-8') as fe:
        cfe.write(fe)

def reset_setting() -> None:
    """恢复默认setting"""
    cfr = configparser.ConfigParser()
    cfr.add_section("BingGo")
    for k, v in SETTINGS.items():
        cfr.set("BingGo", k, str(v[1]))
    with open("setting.ini", mode='w', newline='', encoding='utf-8') as fr:
        cfr.write(fr)
    # edit_setting('startFen', ' rnbk1qnbr/pppp1pppp/9/9/9/O1OOOOO1O/1C5C1/9/RHEASAEHR w kq - 0 1', 'rule.ini', 'zhongxiang_vs_guoxiang')

def edit_rule(key: str, value: str) -> None:
    """rule.ini中添加或覆盖"""
    edit_setting(key, value, "rule.ini", "zhongxiang_vs_guoxiang")
    # cfex = configparser.ConfigParser()
    # cfex.read("rule.ini")
    # if "zhongxiang_vs_guoxiang" not in cfex:
    #     cfex.add_section("zhongxiang_vs_guoxiang")
    # cfex.set("zhongxiang_vs_guoxiang", key, value)
    # with open("rule.ini", mode='w', newline='', encoding='utf-8') as fex:
    #     cfex.write(fex)

def reset_rule() -> None:
    """恢复默认rule"""
    with open("rule.ini", mode='w', newline='', encoding='utf-8') as frx:
        frx.write("[zhongxiang_vs_guoxiang]\nmaxRank = 9\nmaxFile = 9\nstartFen = rnbk1qnbr/pppp1pppp/9/9/9/OOO1O1OOO/1L5L1/9/CMXSWSXMC w kq - 0 1\n\n"
                  "wazir = w:s\nhorse = m:h\ncustomPiece1 = j:NB2RmpRcpR\ncustomPiece2 = x:B2\ncustomPiece3 = o:fsW\ncustomPiece4 = s:K\ncustomPiece5 = l:mRimpRcpR\n\n"
                  "king = k\nqueen = q\nrook = r\nbishop = b\nknight = n\npawn= p\n\n"
                  "pawnTypes = po\npromotionPawnTypesWhite = o\npromotionPawnTypesBlack = p\npromotionPieceTypesBlack = nbrq\npromotionPieceTypesWhite = j\npromotionRegionWhite = *9 *8 *7\npromotionRegionBlack = *1\n\n"
                  "castling = true\ncastlingKingsideFile = g\ncastlingQueensideFile = c\ncastlingKingFile = e\ncastlingRookKingsideFile = i\ncastlingRookQueensideFile = a\nchecking = true\ndoubleStep = true\ndoubleStepRegionBlack = *8\ndoubleStepRegionWhite = *4\n"
                  "extinctionPieceTypes = Wk\nextinctionValue = loss\nextinctionPseudoRoyal = true\nflyingGeneral = true\n;stalemateValue = loss\n\n"
                  "mobilityRegionWhiteWazir = d1 e1 f1 d2 e2 f2 d3 e3 f3\n\npieceToCharTable = PNBRQ..Spnbrq..kAaEe..OoCc..")


def init_setting():
    # 检查setting.ini文件是否存在，不存在则创建
    try:
        with open(file="setting.ini", mode='r', newline='', encoding='utf-8'):
            pass
        cf = configparser.ConfigParser()  # 配置解析器  https://blog.csdn.net/qq_36283274/article/details/145161987
        cf.read('setting.ini')  # 读取 INI 文件
        _ = cf["BingGo"]
    except (KeyError, FileNotFoundError, configparser.ParsingError):
        reset_setting()
        cf = configparser.ConfigParser()
        cf.read('setting.ini')

    # 读取设置并设为全局变量
    for key, value in SETTINGS.items():
        const_name = key.upper()  # 对应的变量名改为全大写
        try:  # 两处可能引发ValueError
            if value[2](value[0](cf["BingGo"][key])):  # 键存在，且值合法，则设为读取的值
                globals()[const_name] = value[0](cf["BingGo"][key])  # 设置一个以const_name为变量名的，以value[0]为类型，以cf["BingGo"][key]为值的变量
            else:  raise ValueError
        except (KeyError, ValueError):  # 键不存在，或者值不是合理的类型，或者值非法，则设为默认值
            globals()[const_name] = value[1]  # 设置一个以const_name为变量名的，以value[1]为值的变量
            print(f"{key} is not valid, set to default value {value[1]}.")  # 显示错误信息
    # >>> print(AI_DEPTH)  # output: 8

    # 检查rule.ini文件是否存在，不存在则创建
    try:
        with open(file="rule.ini", mode='r', newline='', encoding='utf-8'):
            pass
        cf = configparser.ConfigParser()  # 配置解析器  https://blog.csdn.net/qq_36283274/article/details/145161987
        cf.read('rule.ini')  # 读取 INI 文件
        _ = cf["zhongxiang_vs_guoxiang"]
    except (KeyError, FileNotFoundError, configparser.ParsingError):
        reset_rule()

    # 修改rule.ini中的FEN
    edit_rule("startFen", f"{lineup_to_fen(INIT_LINEUP)} {'b' if ACTIVE_CAMP.lower() == 'intl' else 'w'} kq - 0 1")


init_setting()

# DEBUG
# AI_DEPTH = 8  # 这是用来让dep超过限制的范围的
