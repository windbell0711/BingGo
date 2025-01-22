"""
-*- coding: utf-8 -*-
@Time    : 2025-01-21
@Github  : windbell0711/BingGo
@Author  : Lilold333
@Coauthor: TheWindbell07
@License : Apache 2.0
@File    : main.py
"""

try:
    import os
    import sys
    from kivy.resources import resource_add_path, resource_find

    import display

    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    display.BingGo().run()
except Exception as e:
    print("!!!!!!!!!!ERROR!!!!!!!!!!")
    print(e)

input()
