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
Config.set('graphics', 'multisamples', '0')  # https://stackoverflow.com/questions/34969990/kivy-does-not-detect-opengl-2-0
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

        self.img_source = 'imgs/img2' if config.IMG_STYLE_INTL else "imgs/img"

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

    idt_light = []
    bigidt = 0

    def show_path(self):
        self.bigidt = self.beach[self.war.active_qizi.p].idt
        self.imgs[self.bigidt].size = ("%ddp" % ((65 + config.active_qizi_delta_scale) * S), "%ddp" % ((65 + config.active_qizi_delta_scale) * S))
        for p in self.war.active_qizi.get_ma():
            if self.beach.occupied(p):
                if self.img_source == 'imgs/img2':
                    idt = self.beach[p].idt
                    print(idt)
                    self.idt_light.append(idt)
                    self.imgs[idt].opacity = 0.5
                elif self.img_source == 'imgs/img':
                    self.dots.append(Image(source=f'./{self.img_source}/big_dot.png', size_hint=(None, None),
                                           size=("%ddp" % (65 * S), "%ddp" % (65 * S)),
                                           pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
                    self.dots[-1].opacity = 0.5
                    self.add_widget(self.dots[-1])

            else:
                self.dots.append(Image(source=f'./{self.img_source}/small_dot.png', size_hint=(None, None),
                                 size=("%ddp" % (120 * S), "%ddp" % (120 * S)), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
                self.dots[-1].opacity = 0.5
                self.add_widget(self.dots[-1])

    def remove_path(self):
        self.imgs[self.bigidt].size = ("%ddp" % (65 * S), "%ddp" % (65 * S))
        for i in self.idt_light:
            self.remove_widget(self.imgs[i])
            self.imgs[i].opacity = 1
            self.add_widget(self.imgs[i])
        self.idt_light=[]
        for i in self.dots:
            self.remove_widget(i)

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

    def save(self, file_name="save.json"):
        with open(file=os.getcwd() + "\\" + file_name, mode='w', encoding='utf-8') as f:
            json.dump(self.war.logs, f)
        print("已保存")

    def load(self, file_name="save.json"):
        if self.war.turn != 0:
            self.save("autosave%d.json" % int(time.time()))
            self.new()
        with open(file=os.getcwd() + "\\" + file_name, mode='r', encoding='utf-8') as f:
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
            elif 641*2 < x < 690*2 and 100 < y < 146:
                if self.img_source == 'imgs/img':
                    self.img_source = 'imgs/img2'
                    config.write_preference("img_style", "intl")
                else:
                    self.img_source = 'imgs/img'
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
                    if self.beach[p].typ == 6 and self.war.king_win():
                        self.show_picture('shuai_lose')
                    elif self.beach[p].typ == 12 and self.war.king_win():
                        self.show_picture('king_win')
                    elif self.beach[p].typ == 6 and self.war.shuai_win():
                        self.show_picture('shuai_win')
                    elif self.beach[p].typ == 12 and self.war.shuai_win():
                        self.show_picture('king_lose')
                    else:
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
        self.title = "BingGo v1.1.1"
        self.icon = './imgs/mahoupao.ico'
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

        if os.path.exists("lastsave.json"):
            self.war_screen.load("lastsave.json")
            os.remove("./lastsave.json")
            print("已回复进度并删除lastsave.json")

        return self.war_screen

    def on_stop(self):
        if self.war_screen.war.turn != 0:
            self.war_screen.save("lastsave.json")
        print("正在退出")


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
