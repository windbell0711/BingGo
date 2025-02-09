"""
-*- coding: utf-8 -*-
@Github  : windbell0711/BingGo
@File    : config.py
"""
from __future__ import annotations

import csv

friend_fight = False

screen_scale = 1

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

# init_lineup = [
#     "R", "N", "B", "K", " ", "Q", "N", "B", "R", "",
#     "P", "P", "P", "P", " ", "P", "P", "P", "P", "",
#     " ", " ", " ", " ", " ", " ", " ", " ", " ", "",
#     " ", " ", " ", " ", " ", " ", " ", " ", " ", "",
#     " ", " ", " ", " ", " ", " ", " ", " ", " ", "",
#     "兵", " ", "兵", " ", "兵", " ", "兵", " ", "兵", "",
#     " ", "炮", " ", " ", " ", " ", " ", "炮", " ", "",
#     " ", " ", " ", " ", " ", " ", " ", " ", " ", "",
#     "车", "马", "相", "士", "帅", "士", "相", "马", "车", ""
# ]

def reset_preference() -> None:
    """初始化重置preference.csv"""
    with open(file="preference.csv", mode='w', newline='', encoding='utf-8') as f:
        f.write("img_style,intl\n"
                "quick_cmd_status,on\n"
                "init_lineup,|RNBK QNBR|PPPP PPPP|         |         |         |b b b b b| p     p |         |cmxswsxmc|")

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


# init_lineup = "|RNBK QNBR|PPPP PPPP|         |         |         |b b b b b| p     p |         |cmxswsxmc|"
init_lineup = read_preference("init_lineup")[1:]  # 去掉起始的“|”

IMG_STYLE_INTL = {"intl": True, "chn": False}[read_preference("img_style").lower()]
QUICK_CMD_STATUS = {"on": 1, "off": 0}[read_preference("quick_cmd_status").lower()]
