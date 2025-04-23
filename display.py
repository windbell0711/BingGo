"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Github  : windbell0711/BingGo
@Author  : Lilold
@Coauthor: windbell07
@License : Apache 2.0
@File    : display.py
"""
import asyncio
import json
import os
import threading
import time
import webbrowser

import config

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
from kivy.graphics import Rotate
from kivy.uix.textinput import TextInput

from war import *
import Utils


try:
    S: float = config.SCREEN_SCALE
except AttributeError as e:
    logging.error(str(e))
    S = 1
M = Metrics.density * S / 2


class WarScreen(FloatLayout):
    def __init__(self, args, **kwargs):
        super(WarScreen, self).__init__(**kwargs)
        self.restart_expected = False
        self.war = War(self, args)
        self.beach = Beach()

        self.click_time = time.time()
        self.quick_cmd_status = config.QUICK_CMD_ON

        # self.img_source = 'imgs/img2' if config.IMG_STYLE else "imgs/img"

        # self.auto_intl = False
        # self.auto_chn = False
        self.auto_intl_img = Image(source=self.get_img("gou"), size=('%ddp' % (25 * S), '%ddp' % (25 * S)),
                                   size_hint=(None, None),
                                   pos_hint={'center_x': 0.803, 'center_y': 0.270})
        self.auto_chn_img = Image(source=self.get_img("gou"), size=('%ddp' % (25 * S), '%ddp' % (25 * S)),
                                  size_hint=(None, None),
                                  pos_hint={'center_x': 0.803, 'center_y': 0.328})

        # 窗口及背景图设置
        Window.size = (800 * S, 600 * S)
        self.bg_img = Image(source=self.get_img("bg"), size=('%ddp' % (800 * S), '%ddp' % (600 * S)),
                            size_hint=(None, None),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.bg_img)
        self.board_img = Image(source=self.get_img("board"), size=('%ddp' % (800 * S), '%ddp' % (600 * S)),
                               size_hint=(None, None),
                               pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.board_img)
        self.turn_label = Label(
            text="0",
            size_hint=(None, None),
            size=('%ddp' % (200 * S), '%ddp' % (200 * S)),
            pos_hint={'center_x': 0.875, 'center_y': 0.68},
            font_size=f'{20 * S}dp',
            bold=True,
            color=[0, 0, 0, 1])
        self.add_widget(self.turn_label)
        # 添加 TextInput 实例
        self.text_input = TextInput(
            text="",
            font_size=f'{20 * S}dp',
            multiline=False,
            size_hint=(None, None),
            size=('150dp', '40dp'),
            pos_hint={'center_x': 0.878, 'center_y': 0.5},
            font_name='./fonts/simli.ttf'  # 设置支持中文的字体  TODO: 无法正常输入中文
        )
        # self.text_input.bind(on_text_validate=self.on_enter_pressed)  # 绑定 on_text_validate 事件
        self.add_widget(self.text_input)

        # TODO: msg_output
        # self.msg_current = ""
        # self.msg_label = Label(
        #     text=f"BingGo {config.VERSION}",
        #     size_hint=(None, None),
        #     size=('%ddp' % (200 * S), '%ddp' % (100 * S)),
        #     pos_hint={'center_x': 0.88, 'center_y': 0.515},
        #     font_size=f'{20 * S}dp',
        #     color=[0, 0, 0, 1],
        #     halign='center',  # 水平居中
        #     valign='middle',  # 垂直居中
        #     font_name='./fonts/simli.ttf'  # 隶书
        # )
        # self.add_widget(self.msg_label)

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
            name = config.INIT_LINEUP[1:][p]
            if name == " " or name == "|":
                continue
            typ = config.typ_dict[name]
            qizi = Qizi(p=p, typ=typ, beach=self.beach, idt=len(self.pieces))
            self.beach.set_son(qizi, p)
            self.pieces.append(qizi)
            self.imgs.append(Image(
                source=self.get_img(str(typ)), size_hint=(None, None),
                size=('%ddp' % (65 * S), '%ddp' % (65 * S)),
                pos_hint={'center_x': self.fx(p), 'center_y': self.fy(p)}
            ))
            self.add_widget(self.imgs[-1])

        self._init_async_event_loop()  # 新增异步事件循环线程

    def fx(self, p):
        if not self.flipped:
            return (p % 10 + 0.5) / 12
        else:
            return 0.75 - (p % 10 + 0.5) / 12

    def fy(self, p):
        if not self.flipped:
            return (8.5 - p // 10) / 9
        else:
            return 1 - (8.5 - p // 10) / 9

    def get_img(self, name: str) -> str:
        if os.path.exists(f'./imgs/{config.IMG_STYLE}/{name}.png'):  # 检查指定图片在当前包内是否存在
            return f'./imgs/{config.IMG_STYLE}/{name}.png'
        else:
            logging.warning(f"{name}.png not found, using default")
            return f'./imgs/{config.IMG_STYLE_DEFAULT}/{name}.png'

    def _init_async_event_loop(self):
        """初始化异步事件循环线程"""
        self.loop = asyncio.new_event_loop()
        self.async_thread = threading.Thread(
            target=self._run_async_loop,
            daemon=True
        )
        self.async_thread.start()

    def _run_async_loop(self):
        """运行异步事件循环"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def add_label_sound(self, text: str, sound):
        self.hints.append(Image(source=self.get_img(text), size_hint=(None, None),
                                size=('%ddp' % (65 * S), '%ddp' % (65 * S)),
                                pos_hint={'center_x': 0.375, 'center_y': 0.5}))
        self.add_widget(self.hints[-1])
        Clock.schedule_once(lambda dt: self.remove_label(), 1)
        self.sound = SoundLoader.load(f'./music/{sound}.wav')
        if self.sound:
            self.sound.volume = 1.0
            self.sound.loop = True
            self.sound.play()

    def add_label(self, text):
        if text is None or text == "":
            logging.info("label text is empty")
            return
        self.remove_label()
        self.hints.append(Image(source=self.get_img(text), size_hint=(None, None),
                                size=('%ddp' % (200 * S), '%ddp' % (200 * S)),
                                pos_hint={'center_x': 0.88, 'center_y': 0.58}))
        self.add_widget(self.hints[-1])

    def remove_label(self):
        for i in self.hints:
            self.remove_widget(i)

    # def add_gif(self, text):
    #     self.gif=(Image(source=f'./{self.img_source}/{text}.gif', size_hint=(None, None),
    #                             size=('%ddp' % (300 * S), '%ddp' % (300 * S)),
    #                             pos_hint={'center_x': 0.87, 'center_y': 0.515}))
    #     self.add_widget(self.gif)
    #
    # def remove_gif(self):
    #     self.remove_widget(self.gif)

    idt_light = []
    bigidt = 0

    def show_path(self):
        self.bigidt = self.beach[self.war.active_qizi.p].idt
        self.imgs[self.bigidt].size = (
            '%ddp' % ((65 + config.ACTIVE_QIZI_DELTA_SCALE) * S), '%ddp' % ((65 + config.ACTIVE_QIZI_DELTA_SCALE) * S))
        from_pos = Utils.posl(self.war.active_qizi.p)
        for p in [Utils.pos(m[2:]) for m in self.war.ai.get_possible_moves_piece(from_pos)]:
            if self.beach.occupied(p):
                if config.IMG_STYLE == 'intl':
                    idt = self.beach[p].idt
                    # logging.debug(f"idt\t {idt}")
                    self.idt_light.append(idt)
                    self.imgs[idt].opacity = 0.5
                elif config.IMG_STYLE == 'chn':
                    self.dots.append(Image(source=self.get_img("big_dot"), size_hint=(None, None),
                                           size=('%ddp' % (65 * S), '%ddp' % (65 * S)),
                                           pos_hint={'center_x': self.fx(p), 'center_y': self.fy(p)}))
                    self.dots[-1].opacity = 0.5
                    self.add_widget(self.dots[-1])
            else:
                self.dots.append(Image(source=self.get_img("small_dot"), size_hint=(None, None),
                                       size=('%ddp' % (120 * S), '%ddp' % (120 * S)),
                                       pos_hint={'center_x': self.fx(p), 'center_y': self.fy(p)}))
                self.dots[-1].opacity = 0.5
                self.add_widget(self.dots[-1])

    def remove_path(self):
        if self.bigidt <= len(self.imgs):
            self.imgs[self.bigidt].size = ('%ddp' % (65 * S), '%ddp' % (65 * S))
        for i in self.idt_light:
            self.remove_widget(self.imgs[i])
            self.imgs[i].opacity = 1
            self.add_widget(self.imgs[i])
        self.idt_light = []
        for i in self.dots:
            self.remove_widget(i)

    def click_board(self, x, y):
        """点按棋盘"""
        px = round((x - 66) / 133.3, 0)
        py = 8 - round((y - 66) / 133.3, 0)
        if self.flipped:
            px = 8 - px
            py = 8 - py
        p = int(px + 10 * py)  # 点选的位置
        if not self.beach.valid(p):
            logging.error(f"位置不合法  p\t {p}")
            return

        # moves, label, next_turn = self.war.solve_board_press(p)
        self.war.solve_board_press(p)

        self.remove_path()
        if self.war.active_qizi:
            self.show_path()

    def save(self, file_name="save.json"):
        with open(file=os.getcwd() + "\\" + file_name, mode='w', encoding='utf-8') as f:
            json.dump(self.war.logs, f)
        logging.info("已保存")

    def load(self, file_name="save.json"):
        if self.war.turn != 0:
            self.save("autosave%d.json" % int(time.time()))
            self.safe_restart()
        with open(file=os.getcwd() + "\\" + file_name, mode='r', encoding='utf-8') as f:
            ret = json.load(f)
        self.war.logs = ret
        logging.info("已载入")

    def _move_animation(self, idt, p):
        # 确保图片置于顶层
        self.remove_widget(self.imgs[idt])
        self.add_widget(self.imgs[idt])
        # 走子平移动画
        animation = Animation(pos_hint={'center_x': self.fx(p), 'center_y': self.fy(p)}, duration=0.1)
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
                self.imgs.append(Image(source=self.get_img("%d") % oper[1], size_hint=(None, None),
                                       size=('%ddp' % (65 * S), '%ddp' % (65 * S)),
                                       pos_hint={'center_x': self.fx(oper[2]), 'center_y': self.fy(oper[2])}))
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
            logging.warning("无法回退")
            self.turn_label_twinkle()
            return
        self.war.regret()
        logging.debug("已回退一步")

    def gret(self):
        if self.war.turn == len(self.war.logs):
            logging.warning("无法前进")
            self.turn_label_twinkle()
            return
        self.war.gret()
        logging.debug("已前进一步")

    def turn_label_twinkle(self):
        """显示当前回合的label闪红"""
        self._change_color_turn_label((0.9, 0, 0, 1))
        Clock.schedule_once(lambda dt: self._change_color_turn_label((0, 0, 0, 1)), timeout=0.08)
        Clock.schedule_once(lambda dt: self._change_color_turn_label((0.9, 0, 0, 1)), timeout=0.16)
        Clock.schedule_once(lambda dt: self._change_color_turn_label((0, 0, 0, 1)), timeout=0.24)

    def _change_color_turn_label(self, color):
        self.turn_label.color = color

    def ai_move_thread_start(self):
        """完全异步化改造  reference: https://blog.csdn.net/xinzhengLUCK/article/details/138504766"""
        if self.war.is_checkmate:
            logging.warning("游戏已结束，无法AI走子")
            return
        self.war.move_allowed = False

        async def _async_task():
            # try:
            #     # 耗时操作（AI计算）
            #     result = self.war.generate_ai_move()
            #     return result
            # except Exception as e:
            #     logging.error("!AI任务异常: " + str(e))
            #     return None
            result = self.war.generate_ai_move()
            return result

        def _on_complete(task):
            def _ui_operation(dt):
                result = task.result()
                if result is not None and not self.war.is_checkmate:  # 新增有效性检查
                    self.war.main(result)
                self.remove_widget(self.jiazai)
            self.war.move_allowed = True
            Clock.schedule_once(_ui_operation)
            logging.info("AI任务完成，走子放开")

        # ui显示加载中
        self.remove_label()
        self.remove_path()
        self.jiazai = Image(
            source=self.get_img('jiazai'),
            size_hint=(None, None),
            size=('%ddp' % (70 * S), '%ddp' % (70 * S)),
            pos_hint={'center_x': 0.875, 'center_y': 0.515
                      },
        )
        self.add_widget(self.jiazai)
        with self.jiazai.canvas.before:
            rot = Rotate(angle=0, origin=(1400 * M, 618 * M))  # 固定旋转中心坐标
        Animation(angle=-18000, duration=300).start(rot)  # 创造并开始旋转动画
        # 通过已初始化的异步事件循环提交任务
        asyncio.run_coroutine_threadsafe(
            _async_task(),
            self.loop
        ).add_done_callback(_on_complete)
        logging.info("已通过异步事件循环提交任务，限制走子")

    creative_mode = False
    c_typ = 0

    def handle_button_press(self, window, touch):
        if self.creative_mode:
            x, y = touch.pos
            # logging.debug(f"touch.pos\t {x}, {y}")
            x, y = x / M, y / M
            # logging.debug(touch.button)  # debug
            if touch.button == 'scrollup':
                self.create_p[self.c_typ].size = ('%ddp' % (55 * S), '%ddp' % (55 * S))
                self.create_p[self.c_typ].opacity = 1
                if self.c_typ > 12:
                    self.c_typ = 0
                else:
                    self.c_typ += 1
                self.create_p[self.c_typ].size = ('%ddp' % (65 * S), '%ddp' % (65 * S))
                self.create_p[self.c_typ].opacity = 0.7
            elif touch.button == 'scrolldown':
                self.create_p[self.c_typ].size = ('%ddp' % (55 * S), '%ddp' % (55 * S))
                self.create_p[self.c_typ].opacity = 1
                if self.c_typ < 1:
                    self.c_typ = 13
                else:
                    self.c_typ -= 1
                self.create_p[self.c_typ].size = ('%ddp' % (65 * S), '%ddp' % (65 * S))
                self.create_p[self.c_typ].opacity = 0.7

            elif touch.button == 'middle':
                if x < 1220:
                    px = round((x - 66) / 133.3, 0)
                    py = 8 - round((y - 66) / 133.3, 0)
                    if self.flipped:
                        px = 8 - px
                        py = 8 - py
                    p = int(px + 10 * py)  # 点选的位置
                    if not self.beach.valid(p):
                        logging.error(f"位置不合法  p\t {p}")
                        return

                    if self.beach[p] is not None:
                        self.create_p[self.c_typ].size = ('%ddp' % (55 * S), '%ddp' % (55 * S))
                        self.create_p[self.c_typ].opacity = 1
                        self.c_typ = self.beach[p].typ
                        self.create_p[self.c_typ].size = ('%ddp' % (65 * S), '%ddp' % (65 * S))
                        self.create_p[self.c_typ].opacity = 0.7

            elif touch.button == 'left':
                if 1220 < x < 1576 and 62 < y < 220:
                    shuai = 0
                    king = 0
                    for i in self.beach:
                        if i != None and i.typ == 6:
                            shuai += 1
                        elif i != None and i.typ == 12:
                            king += 1
                    if king != 1 or shuai != 1:
                        logging.error('不正确的王或帅数量')
                        return
                    self.war.ai.get_status()  # 快速获取当前状态
                    self.creative_mode = False

                    self.remove_widget(self.cr_image)
                    for i in self.create_p:
                        self.remove_widget(i)

                elif 1220 < x < 1576 and 228 < y < 1108:
                    self.create_p[self.c_typ].size = ('%ddp' % (55 * S), '%ddp' % (55 * S))
                    self.create_p[self.c_typ].opacity = 1
                    typx = (x - 1200) // 180
                    typy = (y - 228) // 125
                    self.c_typ = int(typx + 2 * typy)
                    self.create_p[self.c_typ].size = ('%ddp' % (65 * S), '%ddp' % (65 * S))
                    self.create_p[self.c_typ].opacity = 0.7
                    logging.debug(self.c_typ)

                elif x < 1220:
                    px = round((x - 66) / 133.3, 0)
                    py = 8 - round((y - 66) / 133.3, 0)
                    if self.flipped:
                        px = 8 - px
                        py = 8 - py
                    p = int(px + 10 * py)  # 点选的位置
                    if not self.beach.valid(p):
                        logging.error(f"位置不合法  p\t {p}")
                        return
                    if self.beach[p] is not None:
                        self.generate_animation([(2, self.beach[p].typ, p)])
                        self.war.beach.set_son(None, p=p)
                    else:
                        if self.c_typ == 6 and p not in (63, 64, 65, 73, 74, 75, 83, 84, 85):
                            logging.error('帅不能摆在这里')
                            return
                        self.generate_animation([(1, self.c_typ, p)])
                        self.war.beach.set_son(Qizi(p=p, typ=self.c_typ, beach=self.war.beach), p=p)
        else:
            if touch.button == 'left':
                if len(self.picture_image):
                    self.remove_widget(self.picture_image[-1])
                    self.picture_image = []
                    return
                if time.time() - self.click_time < 0.15:  # 点按频率限制
                    logging.warning("!请按慢一点")
                    return
                self.click_time = time.time()

                x, y = touch.pos
                # logging.debug(f"touch.pos\t {x}, {y}")
                x, y = x / M, y / M

                # 摆子
                if 1272 < x < 1384 and 456 < y < 534:
                    if not self.war.move_allowed:
                        logging.warning("请等待走子完成")
                        return
                    self.creative_mode = True
                    self.remove_path()
                    self.remove_label()
                    self.war.mycamp_intl = False
                    self.war.logs = []  # 走子日志
                    self.war.turn = 0
                    self.turn_label.text = '0'
                    self.cr_image = Image(source=self.get_img("create"),
                                          size=('%ddp' % (800 * S), '%ddp' % (600 * S)), size_hint=(None, None),
                                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
                    self.add_widget(self.cr_image)
                    self.create_p = []
                    for i in range(0, 14):
                        self.create_p.append(Image(
                            source=self.get_img(str(i)), size_hint=(None, None),
                            size=('%ddp' % (55 * S), '%ddp' % (55 * S)),
                            pos_hint={'center_x': i % 2 / 10 + 0.825, 'center_y': i // 2 / 10 + 0.25}
                        ))
                        self.add_widget(self.create_p[-1])
                    self.create_p[self.c_typ].size = ('%ddp' % (65 * S), '%ddp' % (65 * S))
                    self.create_p[self.c_typ].opacity = 0.7
                # 下棋
                if x < 1250:
                    if not self.war.move_allowed:
                        logging.warning("请等待走子完成")
                        return
                    self.war.ai.get_status()  # 快速获取当前状态
                    logging.debug(f">>> {self.war.ai.get_checked(self.war.beach, self.war.mycamp_intl)}")
                    if self.war.is_checkmate and self.war.mycamp_intl == False:
                        self.add_label('red_wins')
                        logging.info('游戏结束')
                        return
                    elif self.war.is_checkmate and self.war.mycamp_intl == True:
                        self.add_label('black_wins')
                        logging.info('游戏结束')
                        return
                    self.click_board(x, y)
                # 右上三个
                elif 750 < y < 848 and 1268 < x < 1536:
                    if not self.war.move_allowed:
                        logging.warning("请等待走子完成")
                        return
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
                    if self.war.move_allowed:
                        if not self.war.is_checkmate:
                            self.ai_move_thread_start()
                        else:
                            logging.warning('游戏已结束')
                    else:
                        logging.warning("请等待走子完成")
                    
                # 新局
                elif 1458 < x < 1542 and 70 < y < 152:
                    if not self.war.move_allowed:
                        logging.warning("请等待走子完成")
                        return
                    self.safe_restart()
                # 保存、载入
                elif 174 < y < 262:
                    if not self.war.move_allowed:
                        logging.warning("请等待走子完成")
                        return
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
                    if self.war.move_allowed:
                        self.war.ai_continue()
                # 切换贴图风格
                elif 641 * 2 < x < 690 * 2 and 100 < y < 146:
                    if config.IMG_STYLE == 'chn':
                        config.edit_setting("img_style", 'intl')
                    else:
                        config.edit_setting("img_style", 'chn')
                    logging.info("重置成功，准备重启...")
                    # 延迟执行重启保证界面操作完成
                    Clock.schedule_once(lambda dt: self.safe_restart(), 0.5)
            elif touch.button == 'right':
                if len(self.picture_image):
                    self.remove_widget(self.picture_image[-1])
                    self.picture_image = []
                if time.time() - self.click_time < 0.15:  # 点按频率限制
                    logging.warning("!请按慢一点")
                    return
                self.click_time = time.time()

                x, y = touch.pos
                # logging.debug(f"touch.pos\t {x}, {y}")
                x, y = x / M, y / M
                if x < 1250:
                    px = round((x - 66) / 133.3, 0)
                    py = 8 - round((y - 66) / 133.3, 0)
                    if self.flipped:
                        px = 8 - px
                        py = 8 - py
                    p = int(px + 10 * py)  # 点选的位置
                    if not self.beach.valid(p):
                        logging.warning(f"位置不合法  p: {p}")
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

    def safe_restart(self):
        """安全重启"""
        if self.parent and self.parent.parent:  # 检查widget树状态
            self.restart_expected = True
            App.get_running_app().stop()

    flipped = False

    def flip(self):
        # 更新翻转状态
        self.flipped = not self.flipped
        # 将self.board_img上下翻转
        self.board_img.texture.flip_vertical()
        # 棋子全部更新位置
        cnt = 0
        for i in self.imgs:
            p = self.pieces[cnt].p
            i.pos_hint = {'center_x': self.fx(p), 'center_y': self.fy(p)}
            cnt += 1
        logging.info('已翻转棋盘')

    def skip(self):
        self.war.mycamp_intl = not self.war.mycamp_intl
        logging.info('已切换当前执棋方')

    def handle_keyboard(self, window, key, scancode, codepoint, modifier):
        if self.quick_cmd_status == 0:  # 键盘监听关闭
            return
        if key == 305:  # 点到ctrl了
            return
        if time.time() - self.click_time < 0.15:  # 点按频率限制
            return
        self.click_time = time.time()
        # logging.debug(f"{key}, {modifier}")  # debug
        # <-
        if key == 276 and not self.text_input.focus:
            self.regret()
        # ->
        elif key == 275 and not self.text_input.focus:
            self.gret()
        # Ctrl + E
        elif 'ctrl' in modifier and key == 101:
            self.skip()
        # Ctrl + F
        elif 'ctrl' in modifier and key == 102:
            self.flip()
        # Ctrl + C
        elif 'ctrl' in modifier and key == 99:
            logging.info("load " + json.dumps(self.war.logs))
            Clipboard.copy("load " + json.dumps(self.war.logs))
        # # Ctrl + V
        # elif 'ctrl' in modifier and key == 118:
        #     p = Clipboard.paste().strip().replace("\n", "")
        #     print("Running: " + p)
        #     r = self.handle_quick_cmd(user_input=p)
        #     print("Return: " + r)
        # Enter
        elif key == 13 or ('numlock' in modifier and key == 271):
            # Enter按下后，执行输入框中的内容
            if not self.text_input.focus:  self.text_input.focus = True
            if not self.text_input.text == "":
                ret = self.handle_quick_cmd(user_input=self.text_input.text)
                self.text_input.text = ret if ret.find(':') == -1 else ret[:ret.find(':')]

    def handle_quick_cmd(self, user_input: str) -> str:
        """
        处理用户输入的快速指令。
        输入：指令内容。输出：如有一条则显示返回提示，如有多条则显示完成几条指令，如中途错误则为显示错误信息。
        """
        if ";" in user_input or "；" in user_input:
            user_input_li = user_input.replace("；", ";").split(";")
            for inp in user_input_li:
                ret = self.handle_single_quick_cmd(inp)
                if ret[0] == '!':
                    return ret
            return "已完成 " + str(len(user_input_li)) + " 条指令"
        else:
            return self.handle_single_quick_cmd(user_input)

    def handle_single_quick_cmd(self, user_input: str) -> str:
        """
        处理用户输入的单行快速指令。
        输入：指令内容。输出：返回信息，第一个字符为“!”表示出错中断。
        """
        # 预处理输入
        infp = user_input.strip().replace("：", ":").replace("，", ",")
        inp = infp.rstrip(":").lstrip('/').lstrip('\\')
        if inp.strip() == "":  return "!输入为空"

        # 分割指令和参数
        if inp.find(":") == -1:  # 不需要参数
            cmd = inp.lower()
            args = []
        else:  # 需要参数
            cmd  = inp[:inp.find(":")].strip().lower()
            args = [argu.strip() for argu in inp[inp.find(":")+1:].split(",")]

        # 处理和执行指令
        # 载入
        if cmd in ("load_log", "load", "载入", "导入"):
            if len(args) != 1:  return f"!参数个数错误({len(args)}/{1})"  # 控制参数个数
            try:
                l = json.loads(args[0])
                self.restart()
                self.war.logs = l
                return "已载入布局"
            except json.decoder.JSONDecodeError:
                return "!Invalid log: " + args[0]
        # 翻转
        elif cmd in ("flip", "twist", "翻转", "反转"):
            self.flip()
            return "已翻转棋盘"
        # 跳过
        elif cmd in ("skip", "跳过", "交换"):
            self.skip()
            return "已更改执棋阵营"
        # 装死（会导致未响应）
        elif cmd in ("sleep", "装死", "假死", "未响应"):
            if len(args) != 1:  return f"!参数个数错误({len(args)}/{1})"  # 控制参数个数
            if not (args[0].strip().isdigit() and 0 < int(args[0]) < 10001):  return "!参数无效哦: " + str(args[0])  # 1ms<参数<=10001ms
            time.sleep(int(args[0]) / 1000)
            return f"已装死{args[0]}ms"
        # 显示设置项
        elif cmd in ("say", "显示设置", "提取", "当前项"):
            if len(args) != 1:  return f"!参数个数错误({len(args)}/{1})"  # 控制参数个数
            return str(getattr(config, args[0].strip().upper().replace(' ', '_')))
        # 更改设置
        elif cmd in ("set", "更改设置", "设置"):
            if len(args) != 2:  return f"!参数个数错误({len(args)}/{2})"  # 控制参数个数
            config.edit_setting(key=args[0].lower().replace(' ', '_'), value=args[1])
            return "更改重启后生效: " + args[0] + " 更改为 " + args[1]
        # 重置设置
        elif cmd in ("reset", "重置设置"):
            config.reset_setting()
            return "已重置设置"
        # 更改zvgv3设置
        elif cmd in ("set_zvgv3", "更改zvgv3设置", "棋类设置"):
            if len(args) != 2:  return f"!参数个数错误({len(args)}/{2})"  # 控制参数个数
            config.edit_zvgv3(key=args[0], value=args[1])
        # 重置zvgv3设置
        elif cmd in ("reset_zvgv3", "重置zvgv3设置", "重置棋类设置"):
            config.reset_zvgv3()
            return "已重置zvgv3设置"
        # 显示帮助
        elif cmd in ("help", "帮助", "芝士什么"):
            webbrowser.open("https://gitee.com/thewindbell07/BingGo/blob/master/README.md")
            return "已打开帮助文档"
        elif cmd in ("hello", "hi", "version", "你好", "版本"):
            return "BingGo " + config.VERSION
        return "!无效的指令: " + cmd

    def show_picture(self, typ):
        self.picture_image.append(
            Image(source=self.get_img(f'{typ}_p'), size=('%ddp' % (700 * S), '%ddp' % (500 * S)),
                  size_hint=(None, None),
                  pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.add_widget(self.picture_image[-1])


class BingGo(App):
    def __init__(self, args=(-1, -1)):
        super().__init__()
        self.args = args
        self.title = f"BingGo {config.VERSION}"  # Title
        self.icon = './imgs/mahoupao.ico'
        self.war_screen = None
        self._is_running = True

    def build(self):
        # bgm设置
        # self.sound = SoundLoader.load('./music/main.wav')
        # if self.sound:
        #     self.sound.volume = 1.0
        #     self.sound.loop = True
        #     self.sound.play()
        # else:
        #     logging.error("!声音播放出错", self.sound)
        self.war_screen = WarScreen(self.args)
        return self.war_screen

    def on_start(self):
        if os.path.exists("lastsave.json"):
            self.war_screen.load("lastsave.json")
            os.remove("./lastsave.json")
            logging.info("已回复进度并删除lastsave.json")

    def on_stop(self):
        """应用退出时保存数据并清理资源"""
        # 保存棋局数据
        if config.SAVE_WHEN_QUIT:
            if self.war_screen.war.turn != 0:
                self.war_screen.save("lastsave.json")
        # 关闭异步事件循环
        if hasattr(self.war_screen, 'loop'):
            self.war_screen.loop.call_soon_threadsafe(self.war_screen.loop.stop)
        # 更新运行状态
        self._is_running = False
        logging.info("正在退出")


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
