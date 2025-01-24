"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Github  : windbell0711/BingGo
@Author  : Lilold333
@Coauthor: TheWindbell07
@License : Apache 2.0
@File    : diaplay.py
"""
import json
import os

from kivy.config import Config
Config.set('graphics', 'width', '800')  # 必须在导入其他任何Kivy模块之前设置
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)  # 禁止调整窗口大小
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
# from kivy.core.text import LabelBase
# LabelBase.register(name="Roboto", fn_regular=r"D:\Documents\Jetbrains\PycharmProjects\BingGo\dist\BingGo 0.1\_internal\kivy_install\data\fonts\Roboto-Regular.ttf")
from kivy.metrics import Metrics
from kivy.animation import Animation
from kivy.clock import Clock

from beach import *
from intelligence import Intelligence

M = Metrics.density / 2

def fx(p):
    return (p % 10 + 0.5) / 12

def fy(p):
    return (8.5 - p // 10) / 9

def target(x,y):
    return y


class War(FloatLayout):
    def __init__(self, **kwargs):
        super(War, self).__init__(**kwargs)
        self.beach = Beach()
        self.beach.quick_set(qizis=config.init_lineup)  # 初始化布局
        self.active_qizi = None  # 当前棋子
        self.mycamp = False  # 我的阵营  False: 中象; True: 国象
        self.log:       List[Tuple[int, int, int]]  = []  # 该回合走子日志  0: move; 1: place; 2: kill
        self.logs: List[List[Tuple[int, int, int]]] = []  # 走子日志
        self.turn = 0  # 所在回合
        self.regret_mode = False
        self.imgs = []

        self.auto_intl = False
        self.auto_chn = False
        self.auto_intl_img = Image(source='./img/gou.png', size=("25dp", "25dp"), size_hint=(None, None),
                                   pos_hint={'center_x': 0.803, 'center_y': 0.270})
        self.auto_chn_img = Image(source='./img/gou.png', size=("25dp", "25dp"), size_hint=(None, None),
                                  pos_hint={'center_x': 0.803, 'center_y': 0.328})

        self.ai = Intelligence(self.beach, self)

        # 窗口及背景图设置
        Window.size = (800, 600)
        image = Image(source='./img/beach.png', size=("800dp", "600dp"), size_hint=(None, None),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(image)
        self.turn_label = Label(text="0", size_hint=(None, None), size=("200dp", "100dp"), bold=True,
                                pos_hint={'center_x': 0.875, 'center_y': 0.68}, font_size='20', color=[0, 0, 0, 1])
        self.add_widget(self.turn_label)

        # self.add_widget(self.auto_intl_img)
        # self.add_widget(self.auto_chn_img)

        # 按键绑定
        Window.bind(on_touch_down=self.handle_button_press)

        # 棋子贴图  TODO: 统一化未完成，应将quick_set()从Beach搬至War
        self.imgs = []
        for qizi in self.beach.pieces:
            self.imgs.append(Image(
                source=f'./img/{qizi.typ}.png', size_hint=(None, None), size=("65dp", "65dp"),
                pos_hint={'center_x': fx(qizi.p), 'center_y': fy(qizi.p)}
            ))
            self.add_widget(self.imgs[-1])

    hints = []

    def add_label_sound(self, text, sound):
        self.hints.append(Image(source=f'./img/{text}.png', size_hint=(None, None),
                                size=("65dp", "65dp"), pos_hint={'center_x': 0.375, 'center_y': 0.5}))
        self.add_widget(self.hints[-1])
        Clock.schedule_once(lambda dt: self.remove_label(), 1)
        self.sound = SoundLoader.load(f'./music/{sound}.wav')  # TODO: 多次使用self.sound存在潜在风险
        if self.sound:
            self.sound.volume = 1.0
            self.sound.loop = True
            self.sound.play()

    def add_label(self, text):
        self.hints.append(Image(source=f'./img/{text}.png', size_hint=(None, None),
                                size=("200dp", "200dp"), pos_hint={'center_x': 0.87, 'center_y': 0.4}))
        self.add_widget(self.hints[-1])

    def remove_label(self):
        for i in self.hints:
            self.remove_widget(i)

    dots = []

    def show_path(self):
        for p in self.active_qizi.get_ma():
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

    def place_piece(self, qizi: Qizi, p: int, log=True):  # TODO: 优化：可以占死人位
        idt = self.beach.set_son(qizi, p)
        self.imgs.append(Image(source='./img/%d.png' % qizi.typ, size_hint=(None, None),
                               size=("65dp", "65dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
        self.add_widget(self.imgs[idt])
        if log:
            self.log.append((1, qizi.typ, p))

    def kill_piece(self, qizi: Qizi, log=True):
        self.beach.set_son(None, qizi.p)
        qizi.alive = False
        self.remove_widget(self.imgs[qizi.idt])
        if log:
            self.log.append((2, qizi.typ, qizi.p))

    def _move_force(self, pfrom: int, pto: int, log=True):
        # 判断是否吃子，顺便写个日志
        yummy = self.beach.occupied(pto)
        if yummy:
            cuisine = self.beach[pto].idt
            if log:
                self.log.append((2, self.beach.pieces[cuisine].typ, pto))
            self.beach.pieces[cuisine].alive = False
            Clock.schedule_once(lambda dt: self.remove_widget(self.imgs[cuisine]), 0.1)  # 吃子消失动画
        # 更新数据并获取棋子id，顺便写个日志
        idt = self.beach.move_son(pfrom, pto)
        if log:
            self.log.append((0, pfrom, pto))
        # 确保图片置于顶层
        self.remove_widget(self.imgs[idt])
        self.add_widget(self.imgs[idt])
        # 走子平移动画
        animation = Animation(pos_hint={'center_x': fx(pto), 'center_y': fy(pto)}, duration=0.1)
        animation.start(self.imgs[idt])

    def _castling(self, p):  # 王车易位
        if self.ai.king_is_checkmate():
            return
        if (self.active_qizi.typ == 12 and self.beach[3].typ == 12 and
                self.beach[1] == self.beach[2] is None and p == 0 and self.beach[p].typ == 8):
            self._move_force(pfrom=0, pto=2)
            self._move_force(pfrom=3, pto=1)
            return True
        elif (self.active_qizi.typ == 12 and self.beach[3].typ == 12 and
              self.beach[4] == self.beach[5] == self.beach[6] == self.beach[7] is None and p == 8 and self.beach[p].typ == 8):
            self._move_force(pfrom=8, pto=4)
            self._move_force(pfrom=3, pto=5)
            return True
        return False

    def _promotion(self, p):  # 升变 ♟->♛
        if self.beach[p].typ == 13 and 79 < p < 89:
            Clock.schedule_once(lambda dt: self.kill_piece(self.beach[p]),0.1)
            Clock.schedule_once(lambda dt: self.place_piece(Qizi(p=p, typ=11, beach=self.beach), p=p),0.1)
            return True
        if self.beach[p].typ == 7 and 0 <= p < 9:
            Clock.schedule_once(lambda dt: self.kill_piece(self.beach[p]),0.1)
            Clock.schedule_once(lambda dt: self.place_piece(Qizi(p=p, typ=0, beach=self.beach), p=p),0.1)
            return True
        return False

    def check(self):
        self.ai.get_attack_pose()
        if self.mycamp == True:
            if self.ai.shuai_p in self.ai.Intl:
                self.add_label(text="check")
                Clock.schedule_once(lambda dt: self.change_regret_mode(), 0.2)
                Clock.schedule_once(lambda dt: self.regret(), 0.2)
                Clock.schedule_once(lambda dt: self.change_regret_mode(), 0.2)
            elif self.ai.king_p in self.ai.Chn:
                if self.ai.king_is_checkmate():
                    self.add_label(text="red_wins")
                    return
                self.add_label(text="check")
        else:
            if self.ai.king_p in self.ai.Chn:
                self.add_label(text="wangbeijj")
                Clock.schedule_once(lambda dt: self.change_regret_mode(), 0.2)
                Clock.schedule_once(lambda dt: self.regret(), 0.2)
                Clock.schedule_once(lambda dt: self.change_regret_mode(), 0.2)
            elif self.ai.shuai_p in self.ai.Intl:
                if self.ai.shuai_is_checkmate():
                    self.add_label(text="black_wins")
                    return
                self.add_label(text="jiangjun")

    def board(self, x, y):
        """点按棋盘"""
        px = round((x - 66) / 133.3, 0)
        py = 8 - round((y - 66) / 133.3, 0)
        p = int(px + 10 * py)  # 点选的位置
        if not self.beach.valid(p):
            print("!位置不合法  p:", p)
            return
        if self.beach.occupied(p) and self.beach[p].camp_intl == self.mycamp:  # 点选棋子为己方阵营
            # 王车易位检查
            if self.active_qizi is not None and self.beach[3] is not None and self.mycamp and self._castling(p):
                self.remove_path()
                self.ラウンドを終える()
            else:
                self.active_qizi = self.beach[p]
                self.remove_path()
                self.show_path()
        elif self.active_qizi is not None and p in self.active_qizi.get_ma():  # 点选位置self.active_qizi能走到
            self._move_force(pfrom=self.active_qizi.p, pto=p)
            print("已移动")
            self._promotion(p)
            self.remove_path()
            Clock.schedule_once(lambda dt: self.ラウンドを終える(), 0.15)
        else:
            print("无法抵达或无法选中")
        return

    def ラウンドを終える(self):
        self.turn += 1
        print("self.turn:", self.turn)
        # print(self.beach)
        self.mycamp = not self.mycamp
        self.active_qizi = None
        self.logs.append(self.log)  # 回合结束
        self.log = []
        print(self.logs)
        self.remove_label()
        self.check()
        self.turn_label.text = str(self.turn)
        # 如果设置了人机对弈，则自动完成下一步
        if self.mycamp:
            if self.auto_intl:
                self.ai.get_possible_moves_Intl()
                self._move_force(*self.ai.best_move)
                self._promotion(target(*self.ai.best_move))
                Clock.schedule_once(lambda dt: self.ラウンドを終える(), 0.1)
        else:
            if self.auto_chn:
                self.ai.get_possible_moves_Chn()
                self._move_force(*self.ai.best_move)
                self._promotion(target(*self.ai.best_move))
                Clock.schedule_once(lambda dt: self.ラウンドを終える(), 0.1)

    def save(self):
        with open(file=os.getcwd() + r"\save.json", mode='w', encoding='utf-8') as f:
            json.dump(self.logs, f)

    def load(self):
        with open(file=os.getcwd() + r"\save.json", mode='r', encoding='utf-8') as f:
            ret = json.load(f)
        self.logs = ret

    def change_regret_mode(self):
        """打开或关闭悔棋模式"""
        if not self.regret_mode:  # 打开悔棋模式
            self.regret_mode = True
        else:  # 关闭悔棋模式
            self.logs = self.logs[:self.turn]
            self.active_qizi = None
            self.regret_mode = False

    def reproduce_operation(self, oper: Tuple[int, int, int]) -> None:
        if oper[0] == 0:
            self._move_force(pfrom=oper[1], pto=oper[2], log=False)
        elif oper[0] == 1:
            self.place_piece(qizi=Qizi(p=oper[2], typ=oper[1], beach=self.beach), p=oper[2], log=False)
        elif oper[0] == 2:
            self.kill_piece(self.beach[oper[2]], log=False)

    def reverse_operation(self, oper: Tuple[int, int, int]) -> Tuple[int, int, int]:
        if oper[0] == 0:
            return (oper[0], oper[2], oper[1])
        elif oper[0] == 1:
            return (2, oper[1], oper[2])
        elif oper[0] == 2:
            return (1, oper[1], oper[2])
        print("!无法逆向操作")
        return oper

    def regret(self):
        if self.turn == 0:
            print("!无法回退")
            self.turn_label_twinkle()
            return
        self.turn -= 1  # 先下一回合再操作
        self.turn_label.text = str(self.turn)
        for i in range(len(self.logs[self.turn])-1, -1, -1):  # 倒序重现
            self.reproduce_operation(self.reverse_operation(self.logs[self.turn][i]))
        self.mycamp = not self.mycamp
        self.ai.reset_attack_pose()
        print("已回退一步")

    def gret(self):
        if self.turn == len(self.logs):
            print("!无法前进")
            self.turn_label_twinkle()
            return
        for i in range(0, len(self.logs[self.turn]), 1):  # 正序重现
            self.reproduce_operation(self.logs[self.turn][i])
        self.turn += 1  # 先操作再下一回合
        self.turn_label.text = str(self.turn)
        self.mycamp = not self.mycamp
        self.ai.reset_attack_pose()
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
            x, y = touch.pos
            print("touch.pos: ", x, y)
            x, y = x / M, y / M
            # 下棋
            if x < 1250:
                if self.regret_mode:
                    self.change_regret_mode()
                self.board(x, y)
            # 右上三个
            elif 750 < y < 848 and 1268 < x < 1536:
                self.remove_path()
                self.remove_label()
                if not self.regret_mode:
                    self.change_regret_mode()
                # 撤回
                if 1268 < x < 1332:
                    self.regret()
                # 自动提示
                elif 1342 < x < 1462:
                        if self.mycamp==False:
                            self.ai.get_possible_moves_Chn()
                        else:
                            self.ai.get_possible_moves_Intl()
                        self._move_force(*self.ai.best_move)
                        self._promotion(target(*self.ai.best_move))
                        self.ラウンドを終える()
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",self.ai.value)
                # 重做
                elif 1476 < x < 1536:
                    self.gret()
            # 新局
            elif 1458 < x < 1542 and 70 < y < 152:
                self.__init__()
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
                    if self.auto_intl:
                        self.auto_intl = False
                        self.remove_widget(self.auto_intl_img)
                    else:
                        self.auto_intl = True
                        self.add_widget(self.auto_intl_img)
                # 中象自动
                else:
                    if self.auto_chn:
                        self.auto_chn = False
                        self.remove_widget(self.auto_chn_img)
                    else:
                        self.auto_chn = True
                        self.add_widget(self.auto_chn_img)


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
        return War()


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
