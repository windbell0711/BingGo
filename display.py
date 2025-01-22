"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Github  : windbell0711/BingGo
@Author  : Lilold333
@Coauthor: TheWindbell07
@License : Apache 2.0
@File    : diaplay.py
"""

from kivy.config import Config
Config.set('graphics', 'width', '800')  # 必须在导入其他任何Kivy模块之前设置
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)  # 禁止调整窗口大小
from kivy.app import App
# from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.metrics import Metrics
from kivy.animation import Animation
from kivy.clock import Clock

from beach import *

M = Metrics.density / 2

def fx(p):
    return (p % 10 + 0.5) / 12

def fy(p):
    return (8.5 - p // 10) / 9


class War(FloatLayout):
    def __init__(self, **kwargs):
        super(War, self).__init__(**kwargs)
        self.beach = Beach()
        self.beach.quick_set(qizis=config.init_lineup)  # 初始化布局
        self.active_qizi = None  # 当前棋子
        self.mycamp = False  # 我的阵营  False: 中象; True: 国象
        self.log: List[Tuple[int, int, int]] = [(7, 0, 0)]  # 走子日志  0: move; 1: place; 2: kill; 7: 分割符
        self.regret_mode = False
        self.regret_pointer = 0
        self.imgs = []

        # bgm设置
        # self.sound = SoundLoader.load('./music/main.wav')
        # if self.sound:
        #     self.sound.volume = 1.0
        #     self.sound.loop = True
        #     self.sound.play()
        # else:
        #     print("!声音播放出错", self.sound)

        # 窗口及背景图设置
        Window.size = (800, 600)
        image = Image(source='./img/beach.png', size=("800dp", "600dp"), size_hint=(None, None),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(image)

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

    hints=[]

    def add_label_sound(self,text,sound):
        self.hints.append(Image(source=f'./img/{text}.png', size_hint=(None, None),
                               size=("65dp", "65dp"), pos_hint={'center_x': 0.375, 'center_y': 0.5}))
        self.add_widget(self.hints[-1])
        Clock.schedule_once(lambda dt: self.remove_label(), 1)
        self.sound = SoundLoader.load(f'./music/{sound}.wav')
        if self.sound:
            self.sound.volume = 1.0
            self.sound.loop = True
            self.sound.play()


    def add_label(self,text):
        self.hints.append(Image(source=f'./img/{text}.png', size_hint=(None, None),
                               size=("200dp", "200dp"), pos_hint={'center_x': 0.87, 'center_y': 0.4}))
        self.add_widget(self.hints[-1])

    def remove_label(self):
        for i in self.hints:
            self.remove_widget(i)

    dots=[]

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

    def place_piece(self, qizi: Qizi, p: int, log=True):  # TODO: 可以占死人位
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

    def _promotion(self, p):  # 升变
        if self.beach[p].typ == 13 and 79 < p < 89:
            Clock.schedule_once(lambda dt: self.kill_piece(self.beach[p]),0.1)
            Clock.schedule_once(lambda dt: self.place_piece(Qizi(p=p, typ=11, beach=self.beach), p=p),0.1)
            return True
        if self.beach[p].typ == 7 and 0 <= p < 9:
            Clock.schedule_once(lambda dt: self.kill_piece(self.beach[p]),0.1)
            Clock.schedule_once(lambda dt: self.place_piece(Qizi(p=p, typ=0, beach=self.beach), p=p),0.1)
            return True
        return False

    Chn = []
    Intl = []
    king_p=90
    shuai_p=90

    def get_attack_pose(self):
        self.reset_attack_pose()
        print(self.beach[3])
        for i in range(0,89):
            if not self.beach[i] == None:
                print(self.beach[i].typ)
                if self.beach[i].typ == 12:
                    self.king_p = i
                    print(i,self.beach[i].p,self.king_p,self.beach[i])
                    break
        for i in (63, 64, 65, 73, 74, 74, 83, 84, 85):
            if not self.beach[i] == None:
                if self.beach[i].typ == 6:
                    self.shuai_p = i
                    print(self.beach[i].p)
                    break
        for i in self.beach:
            if not i == None:
                if i.camp_intl==True:#遍历国际象棋棋子
                    self.Intl += i.get_ma()
                else:
                    self.Chn += i.get_ma()

    def reset_attack_pose(self):
        self.Chn = []
        self.Intl = []
        self.king_p = 90
        self.shuai_p = 90

    def end(self):
        self.beach.virtual_move(self.i, self.i.p)
        self.beach.virtual_move(self.k, self.j)

    def bgn(self):
        self.beach.virtual_move(self.i, self.j)
        self.beach.virtual_move(None, self.i.p)
        print(self.beach[3])
        self.get_attack_pose()

    def king_is_checkmate(self):
        for self.i in self.beach:
            if not self.i == None:
                if self.i.camp_intl==True:
                    for self.j in self.i.get_ma():
                        if not self.j == None:
                            self.k=self.beach[self.j]
                        else:
                            self.k=None
                        self.bgn()
                        if self.mycamp==True:
                            if not self.king_p in self.Chn:
                                print(self.i.p,self.j)
                                self.end()
                                return False
                        self.end()
        return True

    def shuai_is_checkmate(self):
        for self.i in self.beach:
            if not self.i == None:
                if self.i.camp_intl==False:
                    for self.j in self.i.get_ma():
                        if not self.j == None:
                            self.k=self.beach[self.j]
                        else:
                            self.k=None
                        self.bgn()
                        if self.mycamp==False:
                            if not self.shuai_p in self.Intl:
                                print(self.i.p, self.j)
                                self.end()
                                return False
                        self.end()
        return True


    def check(self):
        self.get_attack_pose()
        if self.mycamp == True:
            if self.shuai_p in self.Intl:
                self.add_label(text="check")
                Clock.schedule_once(lambda dt: self.change_regret_mode(), 0.2)
                Clock.schedule_once(lambda dt: self.regret(), 0.2)
                Clock.schedule_once(lambda dt: self.change_regret_mode(), 0.2)
            elif self.king_p in self.Chn:
                if self.king_is_checkmate():
                    self.add_label(text="red_wins")
                    return
                self.add_label(text="check")
        else:
            if self.king_p in self.Chn:
                self.add_label(text="wangbeijj")
                Clock.schedule_once(lambda dt: self.change_regret_mode(), 0.2)
                Clock.schedule_once(lambda dt: self.regret(), 0.2)
                Clock.schedule_once(lambda dt: self.change_regret_mode(), 0.2)
            elif self.shuai_p in self.Intl:
                if self.shuai_is_checkmate():
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
        self.mycamp = not self.mycamp
        self.active_qizi = None
        self.log.append((7, 0, 0))  # 回合结束
        print(self.log)
        self.remove_label()
        self.check()


    def save(self):
        pass

    def load(self):
        pass

    def change_regret_mode(self):
        """打开或关闭悔棋模式"""
        if not self.regret_mode:  # 打开悔棋模式
            if self.log[-1][0] != 7:  # log最后一项必是(7, 0, 0)
                print("!log损坏")
                return
            self.regret_pointer = len(self.log) - 1  # 指向最后一项
            self.regret_mode = True
        else:  # 关闭悔棋模式
            self.log = self.log[:self.regret_pointer + 1]
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
        if self.regret_pointer == 0:
            print("!无法回退")
            return
        self.regret_pointer -= 1
        while self.log[self.regret_pointer][0] != 7:
            self.reproduce_operation(self.reverse_operation(self.log[self.regret_pointer]))
            self.regret_pointer -= 1
        self.mycamp=not self.mycamp
        self.reset_attack_pose()
        print("已回退一步")

    def gret(self):
        if self.regret_pointer == len(self.log) - 1:
            print("!无法前进")
            return
        self.regret_pointer += 1
        while self.log[self.regret_pointer][0] != 7:
            self.reproduce_operation(self.log[self.regret_pointer])
            self.regret_pointer += 1
        self.mycamp = not self.mycamp
        self.reset_attack_pose()
        print("已前进一步")

    def handle_button_press(self, window, touch):
        if touch.button == 'left':
            x, y = touch.pos
            print("touch.pos: ", x, y)
            x, y = x / M, y / M
            if x < 1250:
                if self.regret_mode:
                    self.change_regret_mode()
                self.board(x, y)
            elif 750 < y < 848 and 1268 < x < 1536:
                self.remove_path()
                self.remove_label()
                if not self.regret_mode:
                    self.change_regret_mode()
                if 1268 < x < 1332:
                    self.regret()
                elif 1342 < x < 1462:
                    pass
                elif 1476 < x < 1536:
                    self.gret()


class BingGo(App):
    def build(self):
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