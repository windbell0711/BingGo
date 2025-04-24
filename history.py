"""
-*- coding: utf-8 -*-
@Time    : 2025-04-23
@Github  : windbell0711/BingGo
@Author  : windbell07
@License : Apache 2.0
@File    : history.py
"""

def format_to_str(l: list) -> str:
    """
    :param l: 列表
    :return: 字符串
    """
    s = ""
    for i in l:
        for ii in i:
            s += f"{ii[0]},{ii[1]},{ii[2]};"
        s += "|"
    return s

def restore_to_list(s: str) -> list:
    """
    :param s: 字符串
    :return: 列表
    """
    l = []
    for i in s.split("|"):
        l.append([])
        for ii in i.split(";"):
            if ii != "":
                l[-1].append(tuple(map(int, ii.split(","))))
    return l

if __name__ == '__main__':
    print(format_to_str([[(1, 2, 3), (4, 5, 6)], [(7, 8, 9), (10, 11, 12)]]))
    print(restore_to_list("1,2,3;4,5,6|7,8,9;10,11,12"))
    print(format_to_str([[(0, 56, 46)]]))
