"""
-*- coding: utf-8 -*-
@Time    : 2025-01-28
@File    : wx.py
"""
import time

import pyautogui
import keyboard
import pyperclip

def set_wx():
    print("程序已启动！将鼠标移动到目标位置后:")
    print("- 按 [回车] 捕获坐标")
    print("- 按 [ESC] 退出程序")

    while True:
        # 检测回车键按下
        if keyboard.is_pressed('enter'):
            x, y = pyautogui.position()  # 获取鼠标坐标
            return x, y
        # 检测 ESC 键退出程序
        if keyboard.is_pressed('esc'):
            print("程序已退出")
            return None, None

def send_msg(x, y, msg):
    pyautogui.click(x, y)
    pyperclip.copy(str(msg))
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

def wait_msg():
    c = pyperclip.paste()
    while pyperclip.paste() == c:
        time.sleep(0.5)
    return pyperclip.paste()

def copy_msg(a, b):
    pyautogui.rightClick(a, b)
    pyautogui.click(a+5, b+3)
    return pyperclip.paste()


if __name__ == '__main__':
    time.sleep(2)
    print(copy_msg(751, 672))
