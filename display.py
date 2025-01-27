"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Github  : windbell0711/BingGo
@Author  : Lilold333
@Coauthor: windbell0711
@License : Apache 2.0
@File    : diaplay.py
"""
import json
import os
import time

from kivy.config import Config
Config.set('graphics', 'width', '800')  # 必须在导入其他任何Kivy模块之前设置
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)  # 禁止调整窗口大小
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.metrics import Metrics
from kivy.animation import Animation
from kivy.clock import Clock

from war import *
import config

M = Metrics.density / 2

def fx(p):
    return (p % 10 + 0.5) / 12

def fy(p):
    return (8.5 - p // 10) / 9

class WarScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(WarScreen, self).__init__(**kwargs)
        self.war = War(self)
        self.beach = Beach()

        # self.turn = 0  # 所在回合
        self.click_time = time.time()

        # self.auto_intl = False
        # self.auto_chn = False
        self.auto_intl_img = Image(source='./img/gou.png', size=("25dp", "25dp"), size_hint=(None, None),
                                   pos_hint={'center_x': 0.803, 'center_y': 0.270})
        self.auto_chn_img = Image(source='./img/gou.png', size=("25dp", "25dp"), size_hint=(None, None),
                                  pos_hint={'center_x': 0.803, 'center_y': 0.328})

        # 窗口及背景图设置
        Window.size = (800, 600)
        image = Image(source='./img/beach.png', size=("800dp", "600dp"), size_hint=(None, None),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(image)
        self.turn_label = Label(text="0", size_hint=(None, None), size=("200dp", "100dp"), bold=True,
                                pos_hint={'center_x': 0.875, 'center_y': 0.68}, font_size='20', color=[0, 0, 0, 1])
        self.add_widget(self.turn_label)

        self.hints = []
        self.dots = []
        # self.add_widget(self.auto_intl_img)
        # self.add_widget(self.auto_chn_img)

        # 按键绑定
        Window.bind(on_touch_down=self.handle_button_press)

        # 棋盘初始化
        self.pieces = []
        self.imgs = []
        for p in range(90):
            name = config.init_lineup[p]
            if name == " " or name == "":
                continue
            typ = config.typ_dict[name]
            qizi = Qizi(p=p, typ=typ, beach=self.beach, idt=len(self.pieces))
            self.beach.set_son(qizi, p)
            self.pieces.append(qizi)
            self.imgs.append(Image(
                source=f'./img/{typ}.png', size_hint=(None, None), size=("65dp", "65dp"),
                pos_hint={'center_x': fx(p), 'center_y': fy(p)}
            ))
            self.add_widget(self.imgs[-1])

    def add_label_sound(self, text, sound):
        self.hints.append(Image(source=f'./img/{text}.png', size_hint=(None, None),
                                size=("65dp", "65dp"), pos_hint={'center_x': 0.375, 'center_y': 0.5}))
        self.add_widget(self.hints[-1])
        Clock.schedule_once(lambda dt: self.remove_label(), 1)
        self.sound = SoundLoader.load(f'./music/{sound}.wav')
        if self.sound:
            self.sound.volume = 1.0
            self.sound.loop = True
            self.sound.play()

    def add_label(self, text):
        self.hints.append(Image(source=f'./img/{text}.png', size_hint=(None, None),
                                size=("200dp", "200dp"), pos_hint={'center_x': 0.87, 'center_y': 0.515}))
        self.add_widget(self.hints[-1])

    def remove_label(self):
        for i in self.hints:
            self.remove_widget(i)

    def show_path(self):
        for p in self.war.active_qizi.get_ma():
            if self.beach.occupied(p):
                self.dots.append(Image(source='./img/big_dot.png', size_hint=(None, None),
                                       size=("65dp", "65dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
                self.dots[-1].opacity = 0.5
                self.add_widget(self.dots[-1])
            else:
                self.dots.append(Image(source='./img/small_dot.png', size_hint=(None, None),
                                 size=("120dp", "120dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
                self.dots[-1].opacity = 0.5
                self.add_widget(self.dots[-1])

    def remove_path(self):
        for i in self.dots:
            self.remove_widget(i)

    # def move_piece(self, pfrom: int, pto: int, idt=None):
    #     # 获取子编号
    #     idt = self.beach[pfrom].idt if idt is None else idt
    #     # 确保图片置于顶层
    #     # self.remove_widget(self.imgs[idt])
    #     # self.add_widget(self.imgs[idt])
    #     # 走子平移动画
    #     # animation = Animation(pos_hint={'center_x': fx(pto), 'center_y': fy(pto)}, duration=0.1)
    #     # animation.start(self.imgs[idt])
    #
    # def place_piece(self, typ: int, p: int, idt=None):  # TODO: 优化：可以占死人位
    #     # 获取子编号
    #     idt = len(self.pieces) if idt is None else idt
    #     # 添加贴图
    #     self.pieces.append(Qizi(p=p, typ=typ, beach=self.beach, idt=idt))
    #     self.imgs.append(Image(source='./img/%d.png' % typ, size_hint=(None, None),
    #                            size=("65dp", "65dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
    #     # self.add_widget(self.imgs[idt])
    #     # return idt
    #
    # def kill_piece(self, idt: int):
    #     # self.beach[p].alive = False
    #     self.remove_widget(self.imgs[idt])

    def click_board(self, x, y):
        """点按棋盘"""
        px = round((x - 66) / 133.3, 0)
        py = 8 - round((y - 66) / 133.3, 0)
        p = int(px + 10 * py)  # 点选的位置
        if not self.beach.valid(p):
            print("!位置不合法  p:", p)
            return

        # moves, label, next_turn = self.war.solve_board_press(p)
        moves = self.war.solve_board_press(p)

        # self.display_operation(moves)

        self.remove_path()
        if not self.war.active_qizi is None:
            self.show_path()

    # def ラウンドを終える(self):
    #     self.turn += 1
    #     print("self.turn:", self.turn)
    #     print(self.beach)
    #     self.logs.append(self.log)  # 回合结束
    #     self.log = []
    #     print(self.logs)
    #     self.remove_label()
    #     self.turn_label.text = str(self.turn)
    #     self.check()
    #     如果设置了人机对弈，则自动完成下一步
    #     if self.mycamp_intl:
    #         if self.auto_intl and not self.ai.king_is_checkmate():
    #             self.ai.get_possible_moves_Intl()
    #             # self.move_piece(,
    #             self._promotion(target(*self.ai.best_move))
    #             Clock.schedule_once(lambda dt: self.ラウンドを終える(), 0.1)
    #     else:
    #         if self.auto_chn and not self.ai.shuai_is_checkmate():
    #             self.ai.get_possible_moves_Chn()
    #             # self.move_piece(,
    #             self._promotion(target(*self.ai.best_move))
    #             Clock.schedule_once(lambda dt: self.ラウンドを終える(), 0.1)

    def save(self):
        with open(file=os.getcwd() + r"\save.json", mode='w', encoding='utf-8') as f:
            json.dump(self.war.logs, f)
        print("已保存")

    def load(self):
        if self.war.turn != 0:
            print("!请先新局")
            return
        with open(file=os.getcwd() + r"\save.json", mode='r', encoding='utf-8') as f:
            ret = json.load(f)
        self.war.logs = ret
        print("已载入")

    def new(self):  # TODO: bug 多按了会卡
        self.__init__()
        print("已新局")

    # def change_regret_mode(self):
    #     """打开或关闭悔棋模式"""
    #     if not self.regret_mode:  # 打开悔棋模式
    #         self.regret_mode = True
    #     else:  # 关闭悔棋模式
    #         self.logs = self.logs[:self.turn]
    #         self.war.active_qizi = None
    #         self.regret_mode = False

    def _move_animation(self, idt, p):
        # 确保图片置于顶层
        self.remove_widget(self.imgs[idt])
        self.add_widget(self.imgs[idt])
        # 走子平移动画
        animation = Animation(pos_hint={'center_x': fx(p), 'center_y': fy(p)}, duration=0.1)
        animation.start(self.imgs[idt])

    def generate_animation(self, opers: List[Tuple[int, int, int]]):
        """
        接收一个回合内的多次操作，在WarScreen().beach上进行修改，同时运行相关动画。
        :param opers: 操作
        """
        an = []
        # prepare
        for i in range(len(opers)):
            oper = opers[i]
            if oper[0] == 0 or oper[0] == 4:
                an.append((oper[0], self.beach[oper[1]].idt, oper[2]))
                self.beach.move_son(pfrom=oper[1], pto=oper[2])
            elif oper[0] == 1:
                idt = len(self.pieces)
                an.append((1, idt))
                self.pieces.append(Qizi(p=oper[2], typ=oper[1], beach=self.beach, idt=idt))
                self.imgs.append(Image(source='./img/%d.png' % oper[1], size_hint=(None, None),
                                       size=("65dp", "65dp"), pos_hint={'center_x': fx(oper[2]), 'center_y': fy(oper[2])}))
                self.beach.place_son(typ=oper[1], p=oper[2], idt=idt)
            elif oper[0] == 2:
                an.append((2, self.beach[oper[2]].idt))
                self.beach.kill_son(p=oper[2])
        # display
        for i in range(len(an)):
            a = an[i]
            if a[0] == 0:
                if i == 1 and an[0][0] == 0:  # 非法操作回退动画延迟
                    k00 = a[:]
                    Clock.schedule_once(lambda dt: self._move_animation(idt=k00[1], p=k00[2]), 0.15)
                elif i == 2:  # 逆升变动画延迟
                    k01 = a[:]
                    Clock.schedule_once(lambda dt: self._move_animation(idt=k01[1], p=k01[2]), 0.1)
                else:
                    self._move_animation(idt=a[1], p=a[2])
            elif a[0] == 4:
                self._move_animation(idt=a[1], p=a[2])
            elif a[0] == 1:
                if i == 2 or i == 3:  # 升变动画延迟
                    k10 = self.imgs[a[1]]
                    Clock.schedule_once(lambda dt: self.add_widget(k10), 0.1)
                else:
                    self.add_widget(self.imgs[a[1]])
            elif a[0] == 2:
                if i == 0:  # 吃子动画延迟
                    k20 = self.imgs[a[1]]
                    Clock.schedule_once(lambda dt: self.remove_widget(k20), 0.1)
                elif i == 1 or i == 2:  # 升变动画延迟
                    k21 = self.imgs[a[1]]
                    Clock.schedule_once(lambda dt: self.remove_widget(k21), 0.1)
                else:
                    raise

    @staticmethod
    def reverse_operation(oper: Tuple[int, int, int]) -> Tuple[int, int, int]:
        if oper[0] == 0:
            return (oper[0], oper[2], oper[1])
        elif oper[0] == 1:
            return (2, oper[1], oper[2])
        elif oper[0] == 2:
            return (1, oper[1], oper[2])
        print("!无法逆向操作")
        return oper

    def regret(self):
        if self.war.turn == 0:
            print("!无法回退")
            self.turn_label_twinkle()
            return
        ms = self.war.regret()
        # self.display_operation(ms)

        # self.turn -= 1  # 先下一回合再操作
        # self.turn_label.text = str(self.war.turn)
        # for i in range(len(self.logs[self.turn])-1, -1, -1):  # 倒序重现
        #     self.display_operation(self.reverse_operation(self.logs[self.turn][i]))
        # self.mycamp_intl = not self.mycamp_intl
        # self.ai.reset_attack_pose()
        print("已回退一步")

    def gret(self):
        if self.war.turn == len(self.war.logs):
            print("!无法前进")
            self.turn_label_twinkle()
            return
        ms = self.war.gret()
        # self.display_operation(ms)

        # for i in range(0, len(self.logs[self.turn]), 1):  # 正序重现
        #     self.display_operation(self.logs[self.turn][i])
        # self.turn += 1  # 先操作再下一回合
        # self.turn_label.text = str(self.turn)
        # self.mycamp_intl = not self.mycamp_intl
        # self.ai.reset_attack_pose()
        print("已前进一步")

    def turn_label_twinkle(self):
        """显示当前回合的label闪红"""
        self._change_color_turn_label((0.9, 0, 0, 1))
        Clock.schedule_once(lambda dt: self._change_color_turn_label((0, 0, 0, 1)), timeout=0.08)
        Clock.schedule_once(lambda dt: self._change_color_turn_label((0.9, 0, 0, 1)), timeout=0.16)
        Clock.schedule_once(lambda dt: self._change_color_turn_label((0, 0, 0, 1)), timeout=0.24)

    def _change_color_turn_label(self, color):
        self.turn_label.color = color

    def handle_button_press(self, window, touch):
        if touch.button == 'left':
            if time.time() - self.click_time < 0.2:  # 点按频率限制
                print("!请按慢一点")
                return
            self.click_time = time.time()

            x, y = touch.pos
            print("touch.pos: ", x, y)
            x, y = x / M, y / M

            # 下棋
            if x < 1250:
                # if self.regret_mode:
                #     self.change_regret_mode()
                self.click_board(x, y)
            # 右上三个
            elif 750 < y < 848 and 1268 < x < 1536:
                self.remove_path()
                self.remove_label()
                # if not self.regret_mode:
                #     self.change_regret_mode()
                # 撤回
                if 1268 < x < 1332:
                    self.regret()
                # 重做
                elif 1476 < x < 1536:
                    self.gret()
            elif 705*2 < x < 770*2 and 230*2 < y < 270*2:
                self.war.ai_move()
            # 新局
            elif 1458 < x < 1542 and 70 < y < 152:
                self.new()
            # 保存、载入
            elif 174 < y < 262:
                if 1266 < x < 1440:
                    self.save()
                elif 1418 < x < 1548:
                    self.load()
            # 勾选自动方
            elif 147*2 < y < 207*2:
                # 国象自动
                if y < 177*2:
                    if self.war.auto_intl:
                        self.war.auto_intl = False
                        self.remove_widget(self.auto_intl_img)
                    else:
                        self.war.auto_intl = True
                        self.add_widget(self.auto_intl_img)
                # 中象自动
                else:
                    if self.war.auto_chn:
                        self.war.auto_chn = False
                        self.remove_widget(self.auto_chn_img)
                    else:
                        self.war.auto_chn = True
                        self.add_widget(self.auto_chn_img)
                self.war.ai_continue()


class BingGo(App):
    def build(self):
        # bgm设置
        # self.sound = SoundLoader.load('./music/main.wav')
        # if self.sound:
        #     self.sound.volume = 1.0
        #     self.sound.loop = True
        #     self.sound.play()
        # else:
        #     print("!声音播放出错", self.sound)
        return WarScreen()


def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}


if __name__ == '__main__':
    reset()
    BingGo().run()
