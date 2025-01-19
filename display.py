from kivy.config import Config

# 必须在导入其他任何Kivy模块之前设置
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)  # 禁止调整窗口大小

from move import *
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.metrics import Metrics

sa = []
m = Metrics.density / 2

def fx(p):
    return (p % 10 + 0.5) / 12

def fy(p):
    return (8.5 - p // 10) / 9


class War:
    def __init__(self):
        self.beach = Beach()
        self.beach.continuously_set(qizis={
            80: "车",
            81: "马",
            82: "相",
            83: "士",
            84: "帅",
            85: "士",
            86: "相",
            87: "马",
            88: "车",
            61: "炮",
            64: "炮",
            67: "炮",
            50: "兵",
            52: "兵",
            54: "兵",
            56: "兵",
            58: "兵",

            0: "rook",
            1: "knight",
            2: "bishop",
            3: "king",
            5: "queen",
            6: "bishop",
            7: "knight",
            8: "rook",
            10: "pawn",
            11: "pawn",
            12: "pawn",
            13: "pawn",
            14: "pawn",
            15: "pawn",
            16: "pawn",
            17: "pawn",
            18: "pawn"
        })

    def move_son(self, pfrom: int, pto: int):
        self.beach.set(qizi=self.beach[pfrom], p=pto)


if __name__ == '__main__':
    binggo = War()
    beach = binggo.beach


class BingGo(App):
    def build(self):
        # bgm设置
        self.sound = SoundLoader.load('./music/main.wav')
        if self.sound:
            self.sound.volume = 1.0
            self.sound.loop = True
            self.sound.play()

        # 窗口及背景图设置
        Window.size = (800, 600)
        self.layout = FloatLayout()
        image = Image(source='./img/beach.png', size=("800dp", "600dp"), size_hint=(None, None),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(image)

        # 按键绑定
        Window.bind(on_touch_down=self.get_p)
        Window.bind(on_touch_down=self.regret)
        Window.bind(on_touch_down=self.new)
        Window.bind(on_touch_down=self.story)

        # 棋子贴图
        for i in range(0, 89):
            if not beach[i] is None:
                p = beach[i].p
                imagen = f'image_{i}'
                globals()[imagen] = Image(source=f'./img/{beach[i].typ}.png', size_hint=(None, None),
                                          size=("65dp", "65dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)})
                self.layout.add_widget(globals()[imagen])

        # self.layout.remove_widget(widget=globals()[f'image_{10}'])

        return self.layout

    def get_p(self, window, touch):
        """打印可移动位置"""
        if touch.button == 'left':
            self.x, self.y = touch.pos
            self.x /= m
            self.y /= m
            if not self.x > 1250:
                x = round((self.x - 66) / 133.3, 0)
                y = 8 - round((self.y - 66) / 133.3, 0)
                p = int(x + 10 * y)
                if not beach[p] is None:
                    sa = beach[p].get_ma()
                    print(beach[p].ma)

    def regret(self, window, touch):
        if touch.button == 'left':
            self.x, self.y = touch.pos
            if 131 * m < self.x < 1484 * m and 680 * m < self.y < 768 * m:
                print("regret")

    def new(self, window, touch):
        if touch.button == 'left':
            self.x, self.y = touch.pos
            if 1316 * m < self.x < 1484 * m and 483 * m < self.y < 568 * m:
                print("new")

    def story(self, window, touch):
        if touch.button == 'left':
            self.x, self.y = touch.pos
            if 1316 * m < self.x < 1484 * m and 263 * m < self.y < 356 * m:
                print("story")


if __name__ == '__main__':
    BingGo().run()
