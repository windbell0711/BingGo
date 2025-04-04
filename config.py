"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Github  : windbell0711/BingGo
@License : Apache 2.0
@File    : config.py
"""
from __future__ import annotations
from typing import Any, List, Tuple
import csv

VERSION = "v1.2.0"

# screen_scale = 1
active_qizi_delta_scale = 5  # 原大小：65

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

ALL_PIECE_TYPES = "jcmxspwbRNBQKP"

PREFERENCE_BY_DEFAULT = """\
img_style,intl
quick_cmd_status,on
save_when_quit,on
init_lineup,|RNBK QNBR|PPPP PPPP|         |         |         |b bbbbb b| p     p |         |cmxswsxmc|
ai_depth,6
promotion_dis,2
screen_scale,1
"""


def reset_preference() -> None:
    """初始化重置preference.csv"""
    with open(file="preference.csv", mode='w', newline='', encoding='utf-8') as f:
        f.write(PREFERENCE_BY_DEFAULT)

def read_preference(key: str) -> str:
    """从preference.csv中读入"""
    try:
        with open(file="preference.csv", mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == key:
                    return row[1].strip()
    except FileNotFoundError:
        reset_preference()
        print("!preference.csv文件缺失，已重置。")
        return read_preference(key)

def write_preference(key, value) -> None:
    """在preference.csv中添加或覆盖"""
    # 先读取现有内容
    lines = []
    key_found = False
    try:
        with open("preference.csv", mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2 and row[0].strip() == key:
                    lines.append([key, value])
                    key_found = True
                else:
                    lines.append(row)
    # 如果文件不存在，直接创建并写入
    except FileNotFoundError:
        print("!preference.csv不存在或已被移动，将新建preference.csv")
    # 如果键不存在，追加新键值对
    if not key_found:
        lines.append([key, value])
    # 写回文件
    with open("preference.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

def is_int(s: str) -> bool:
    for c in s:
        if not (c.isdigit() or c == "-"):
            return False
    return True

def is_float(s: str) -> bool:
    for c in s:
        if not (c.isdigit() or c == "." or c == "-"):
            return False
    return True

def check_int(key: str, min_num: int, max_num: int, value_if_invalid: int) -> int:
    r = read_preference(key).strip()
    if is_int(r) and min_num <= int(r) <= max_num:
        return int(r)
    else:
        print("!Invalid " + key + ": " + r)
        return value_if_invalid

def check_float(key: str, min_num: float, max_num: float, value_if_invalid: float) -> float:
    r = read_preference(key).strip()
    if is_float(r) and min_num <= float(r) <= max_num:
        return float(r)
    else:
        print("!Invalid " + key + ": " + r)
        return value_if_invalid


init_lineup = read_preference("init_lineup")[1:]  # 去掉起始的“|”

IMG_STYLE_INTL   = {"intl": True, "chn": False}[read_preference("img_style").lower()]
QUICK_CMD_STATUS = {"on": 1, "off": 0}[read_preference("quick_cmd_status").lower()]
SAVE_WHEN_QUIT   = {"on": True, "off": False}[read_preference("save_when_quit").lower()]

AI_DEPTH      = check_int  ("ai_depth", 2, 12, 5)
PROMOTION_DIS = check_int  ("promotion_dis", 1, 3, 2)
SCREEN_SCALE  = check_float("screen_scale", 0.25, 10, 1)
