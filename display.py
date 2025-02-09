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
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.core.clipboard import Clipboard
from kivy.metrics import Metrics
from kivy.animation import Animation
from kivy.clock import Clock

from war import *
import config
import wx

class BieGuanWoException(Exception):
    pass

try:
    S = config.screen_scale
except AttributeError as e:
    print("! " + str(e))
    S = 1
M = Metrics.density * S / 2

def fx(p):
    return (p % 10 + 0.5) / 12

def fy(p):
    return (8.5 - p // 10) / 9

class WarScreen(FloatLayout):
    def __init__(self, args, **kwargs):
        super(WarScreen, self).__init__(**kwargs)
        self.war = War(self, args)
        self.beach = Beach()

        self.click_time = time.time()
        self.quick_cmd_status = config.QUICK_CMD_STATUS

        self.img_source = 'img2' if config.IMG_STYLE_INTL else "img"

        # self.auto_intl = False
        # self.auto_chn = False
        self.auto_intl_img = Image(source=f'./{self.img_source}/gou.png', size=("%ddp" % (25 * S), "%ddp" % (25 * S)), size_hint=(None, None),
                                   pos_hint={'center_x': 0.803, 'center_y': 0.270})
        self.auto_chn_img = Image(source=f'./{self.img_source}/gou.png', size=("%ddp" % (25 * S), "%ddp" % (25 * S)), size_hint=(None, None),
                                  pos_hint={'center_x': 0.803, 'center_y': 0.328})

        # 窗口及背景图设置
        Window.size = (800 * S, 600 * S)
        self.bg_image = Image(source=f'./{self.img_source}/beach.png', size=("%ddp" % (800 * S), "%ddp" % (600 * S)), size_hint=(None, None),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.bg_image)
        self.turn_label = Label(text="0", size_hint=(None, None), size=("%ddp" % (200 * S), "%ddp" % (100 * S)), bold=True,
                                pos_hint={'center_x': 0.875, 'center_y': 0.68}, font_size='20dp', color=[0, 0, 0, 1])
        self.add_widget(self.turn_label)

        self.hints = []
        self.dots = []
        # self.add_widget(self.auto_intl_img)
        # self.add_widget(self.auto_chn_img)
        self.picture_image = []

        # 按键绑定
        Window.bind(on_touch_down=self.handle_button_press)
        Window.bind(on_keyboard=self.handle_keyboard)

        # 棋盘初始化
        self.pieces = []
        self.imgs = []
        for p in range(90):
            name = config.init_lineup[p]
            if name == " " or name == "|":
                continue
            typ = config.typ_dict[name]
            qizi = Qizi(p=p, typ=typ, beach=self.beach, idt=len(self.pieces))
            self.beach.set_son(qizi, p)
            self.pieces.append(qizi)
            self.imgs.append(Image(
                source=f'./{self.img_source}/{typ}.png', size_hint=(None, None), size=("%ddp" % (65 * S), "%ddp" % (65 * S)),
                pos_hint={'center_x': fx(p), 'center_y': fy(p)}
            ))
            self.add_widget(self.imgs[-1])

    def add_label_sound(self, text, sound):
        self.hints.append(Image(source=f'./{self.img_source}/{text}.png', size_hint=(None, None),
                                size=("%ddp" % (65 * S), "%ddp" % (65 * S)), pos_hint={'center_x': 0.375, 'center_y': 0.5}))
        self.add_widget(self.hints[-1])
        Clock.schedule_once(lambda dt: self.remove_label(), 1)
        self.sound = SoundLoader.load(f'./music/{sound}.wav')
        if self.sound:
            self.sound.volume = 1.0
            self.sound.loop = True
            self.sound.play()

    def add_label(self, text):
        self.hints.append(Image(source=f'./{self.img_source}/{text}.png', size_hint=(None, None),
                                size=("%ddp" % (200 * S), "%ddp" % (200 * S)), pos_hint={'center_x': 0.87, 'center_y': 0.515}))
        self.add_widget(self.hints[-1])

    def remove_label(self):
        for i in self.hints:
            self.remove_widget(i)

    def show_path(self):
        for p in self.war.active_qizi.get_ma():
            if self.beach.occupied(p):
                self.dots.append(Image(source=f'./{self.img_source}/big_dot.png', size_hint=(None, None),
                                       size=("%ddp" % (65 * S), "%ddp" % (65 * S)), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
                self.dots[-1].opacity = 0.5
                self.add_widget(self.dots[-1])
            else:
                self.dots.append(Image(source=f'./{self.img_source}/small_dot.png', size_hint=(None, None),
                                 size=("%ddp" % (120 * S), "%ddp" % (120 * S)), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
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
    #                            size=("%ddp" % (65 * S), "%ddp" % (65 * S)), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
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
        self.war.solve_board_press(p)

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

    def new(self):  # bug 多按了会卡，然而失去全部力气和手段
        self.__init__((-1, -1))
        print("已新局")

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
                self.imgs.append(Image(source=f'./{self.img_source}/%d.png' % oper[1], size_hint=(None, None),
                                       size=("%ddp" % (65 * S), "%ddp" % (65 * S)), pos_hint={'center_x': fx(oper[2]), 'center_y': fy(oper[2])}))
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
                if i == 2:  # 非法王车易位回退动画延迟1
                    k40 = a[:]
                    Clock.schedule_once(lambda dt: self._move_animation(idt=k40[1], p=k40[2]), 0.175)
                elif i == 3:  # 非法王车易位回退动画延迟2
                    k41 = a[:]
                    Clock.schedule_once(lambda dt: self._move_animation(idt=k41[1], p=k41[2]), 0.175)
                else:
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

    def regret(self):
        if self.war.turn == 0:
            print("!无法回退")
            self.turn_label_twinkle()
            return
        self.war.regret()
        print("已回退一步")

    def gret(self):
        if self.war.turn == len(self.war.logs):
            print("!无法前进")
            self.turn_label_twinkle()
            return
        self.war.gret()
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
            if len(self.picture_image):
                self.remove_widget(self.picture_image[-1])
                self.picture_image = []
                return
            if time.time() - self.click_time < 0.15:  # 点按频率限制
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
            elif 705 * 2 < x < 770 * 2 and 230 * 2 < y < 270 * 2:
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
            elif 147 * 2 < y < 207 * 2:
                # 国象自动
                if y < 177 * 2:
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
            # 切换贴图风格
            elif 1288 < x < 1382 and 88 < y < 122:
                if self.img_source == 'img':
                    self.img_source = 'img2'
                    config.write_preference("img_style", "intl")
                else:
                    self.img_source = 'img'
                    config.write_preference("img_style", "chn")
                print("重置成功，请重启。")
                raise BieGuanWoException
                # self.remove_widget(self.bg_image)
                # self.bg_image = Image(source=f'./{self.img_source}/beach.png', size=("%ddp" % (800 * S), "%ddp" % (600 * S)),
                #                       size_hint=(None, None),
                #                       pos_hint={'center_x': 0.5, 'center_y': 0.5})
                # self.add_widget(self.bg_image)
                # self.new()
        elif touch.button == 'right':
            if len(self.picture_image):
                self.remove_widget(self.picture_image[-1])
                self.picture_image = []
            if time.time() - self.click_time < 0.15:  # 点按频率限制
                print("!请按慢一点")
                return
            self.click_time = time.time()

            x, y = touch.pos
            print("touch.pos: ", x, y)
            x, y = x / M, y / M
            if x < 1250:
                px = round((x - 66) / 133.3, 0)
                py = 8 - round((y - 66) / 133.3, 0)
                p = int(px + 10 * py)  # 点选的位置
                if not self.beach.valid(p):
                    print("!位置不合法  p:", p)
                    return
                if not self.beach[p] is None:
                    self.show_picture(self.beach[p].typ)

    def handle_keyboard(self, window, key, scancode, codepoint, modifier):
        if self.quick_cmd_status == 0:  # 键盘监听关闭
            return
        if key == 305:  # 点到ctrl了
            return
        if time.time() - self.click_time < 0.15:  # 点按频率限制
            return
        self.click_time = time.time()
        print(key, modifier)
        # <-
        if key == 276:
            self.regret()
        # ->
        elif key == 275:
            self.gret()
        # Ctrl + C
        elif 'ctrl' in modifier and key == 99:
            print("load " + json.dumps(self.war.logs))
            Clipboard.copy("load " + json.dumps(self.war.logs))
        # Ctrl + V
        elif 'ctrl' in modifier and key == 118:
            p = Clipboard.paste().strip().replace("\n", "")
            print("Running " + p)
            if p.find(" ") == -1:  # 不需要参数
                cmd = p
                pass
            else:
                cmd, argu = p[:p.find(" ")].lower(), p[p.find(" ")+1:]  # 需要参数
                if cmd == "load":
                    try:
                        l = json.loads(argu)
                        self.new()
                        self.war.logs = l
                    except json.decoder.JSONDecodeError:
                        print("!Invalid log: " + argu)
                elif cmd == "quick_cmd":
                    if argu == "on":
                        self.quick_cmd_status = 1
                        config.write_preference(key="quick_cmd_status", value="on")
                    elif argu == "off":
                        self.quick_cmd_status = 0
                        config.write_preference(key="quick_cmd_status", value="off")
                    else:
                        print("!Invalid argu: " + argu)
                elif cmd == "init_lineup":
                    if len(argu) == 91 and argu[0] == "|":
                        config.write_preference(key="init_lineup", value=argu)
                    else:
                        print("!Invalid argu: " + argu)

    def show_picture(self, typ):
        self.picture_image.append(
            Image(source=f'./{self.img_source}/{typ}_p.png', size=("%ddp" % (700 * S), "%ddp" % (500 * S)), size_hint=(None, None),
                  pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.add_widget(self.picture_image[-1])


class BingGo(App):
    def __init__(self, args=(-1, -1)):
        super().__init__()
        self.args = args
        self.icon = './img_readme/mahoupao.ico'
        self.war_screen = None

    def build(self):
        # bgm设置
        # self.sound = SoundLoader.load('./music/main.wav')
        # if self.sound:
        #     self.sound.volume = 1.0
        #     self.sound.loop = True
        #     self.sound.play()
        # else:
        #     print("!声音播放出错", self.sound)
        self.war_screen = WarScreen(self.args)
        return self.war_screen


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
    if config.friend_fight:
        print("请调整窗口位置，保证能同时看到象棋界面和微信聊天框，接下来将录入鼠标位置...")
        print("录入聊天输入框位置...")
        SCREEN_POS_x, SCREEN_POS_y = wx.set_wx()
        print(SCREEN_POS_x, SCREEN_POS_y)
        reset()
        BingGo(args=(SCREEN_POS_x, SCREEN_POS_y)).run()
    else:
        reset()
        BingGo().run()
