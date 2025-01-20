from kivy.config import Config
Config.set('graphics', 'width', '800')  # 必须在导入其他任何Kivy模块之前设置
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)  # 禁止调整窗口大小
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.metrics import Metrics
from kivy.animation import Animation
from kivy.clock import Clock
import time

from beach import *


M = Metrics.density / 2

def fx(p):
    return (p % 10 + 0.5) / 12

def fy(p):
    return (8.5 - p // 10) / 9


class BingGo(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.beach = Beach()
        self.beach.quick_set(qizis=config.init_lineup)  # 初始化布局
        self.active_qizi = None  # 当前棋子
        self.mycamp = False  # 我的阵营  False: 中象; True: 国象
        self.imgs = []
        
        self.sound = None
        self.layout = None

    def build(self):
        # bgm设置
        self.sound = SoundLoader.load('./music/main.wav')
        if self.sound:
            self.sound.volume = 1.0
            self.sound.loop = True
            self.sound.play()
        else:
            print("!声音播放出错", self.sound)

        # 窗口及背景图设置
        Window.size = (800, 600)
        self.layout = FloatLayout()
        image = Image(source='./img/beach.png', size=("800dp", "600dp"), size_hint=(None, None),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(image)

        # 按键绑定
        Window.bind(on_touch_down=self.handle_button_press)

        # 棋子贴图  TODO: 统一化未完成，应将quick_set()从Beach搬至BingGo
        self.imgs = []
        for qizi in self.beach.pieces:
            self.imgs.append(Image(
                source=f'./img/{qizi.typ}.png', size_hint=(None, None), size=("65dp", "65dp"),
                pos_hint={'center_x': fx(qizi.p), 'center_y': fy(qizi.p)}
            ))
            self.layout.add_widget(self.imgs[-1])

        # 已弃用写法：
        # for i in range(0, 89):
        #     self.imgs = []
        #     if not self.beach[i] is None:
        #         p = self.beach[i].p
        #         imagen = f'image_{i}'
        #         self.imgs.append(imagen)
        #         globals()[imagen] = Image(source=f'./img/{self.beach[i].typ}.png', size_hint=(None, None),
        #                                   size=("65dp", "65dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)})
        #         self.layout.add_widget(globals()[imagen])

        return self.layout

    def place_piece(self, qizi: Qizi, p: int):
        idt = self.beach.set_son(qizi, p)
        self.imgs.append(Image(source='./img/%d.png' % qizi.typ, size_hint=(None, None),
                               size=("65dp", "65dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
        self.layout.add_widget(self.imgs[idt])

    def kill_piece(self, qizi: Qizi):
        self.beach.set_son(None, qizi.p)
        qizi.alive = False
        self.layout.remove_widget(self.imgs[qizi.idt])

    def _move_force(self, pfrom: int, pto: int):
        # 判断是否吃子
        yummy, cuisine = self.beach.occupied(pto), None
        if yummy:
            cuisine = self.beach[pto].idt
        # 更新数据并获取棋子id
        idt = self.beach.move_son(pfrom, pto)
        # 确保图片置于顶层
        self.layout.remove_widget(self.imgs[idt])
        self.layout.add_widget(self.imgs[idt])
        # 走子平移动画
        animation = Animation(pos_hint={'center_x': fx(pto), 'center_y': fy(pto)}, duration=0.25)
        animation.start(self.imgs[idt])
        # 吃子消失动画
        if yummy:
            Clock.schedule_once(lambda dt: self.layout.remove_widget(self.imgs[cuisine]), 0.25)

    def board(self, x, y):
        """点按棋盘"""
        px = round((x - 66) / 133.3, 0)
        py = 8 - round((y - 66) / 133.3, 0)
        p = int(px + 10 * py)  # 点选的位置
        if not self.beach.valid(p):
            print("!位置不合法  p:", p)
            return
        if self.beach.occupied(p) and self.beach[p].camp_intl == self.mycamp:  # 点选棋子为己方阵营
            self.active_qizi = self.beach[p]
            print(self.active_qizi.typ, self.active_qizi.get_ma())
        elif self.active_qizi is not None and p in self.active_qizi.get_ma():  # 点选位置self.active_qizi能走到
            self._move_force(pfrom=self.active_qizi.p, pto=p)
            print("已移动")
        else:
            print("无法抵达或无法选中")
        return

    def handle_button_press(self, window, touch):
        if touch.button == 'left':
            x, y = touch.pos
            x, y = x / M, y / M
            if x < 1250:
                self.board(x, y)
            elif 1316 < x < 1484:
                if 680 < y < 768:
                    print("regret")
                elif 483 < y < 568:
                    print("new")
                elif 263 < y < 356:
                    print("story")


if __name__ == '__main__':
    BingGo().run()
