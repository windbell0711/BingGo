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

from beach import *


sa = []
m = Metrics.density / 2

def fx(p):
    return (p % 10 + 0.5) / 12

def fy(p):
    return (8.5 - p // 10) / 9


class BingGo(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.beach = Beach()
        self.beach.quick_set(qizis=config.init_lineup)  # 初始化布局
        self.sound = None
        self.imgs = []
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
        Window.bind(on_touch_down=self.print_ma)
        Window.bind(on_touch_down=self.handle_button_press)

        # 棋子贴图  TODO: 统一化未完成
        #self.imgs = []
        #for qizi in self.beach.pieces:
        #    self.imgs.append(Image(
        #        source=f'./img/{qizi.typ}.png', size_hint=(None, None), size=("65dp", "65dp"),
        #        pos_hint={'center_x': fx(qizi.p), 'center_y': fy(qizi.p)}
        #    ))
        #    self.layout.add_widget(self.imgs[-1])

        for i in range(0, 89):
            self.imgs = []
            if not self.beach[i] is None:
                 p = self.beach[i].p
                 imagen = f'image_{i}'
                 self.imgs.append(imagen)
                 globals()[imagen] = Image(source=f'./img/{self.beach[i].typ}.png', size_hint=(None, None),
                                           size=("65dp", "65dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)})
                 self.layout.add_widget(globals()[imagen])


        # self.layout.remove_widget(widget=globals()[f'image_{10}'])
        return self.layout

    def set_son(self, qizi, p: int):
        idt = self.beach.set_son(qizi, p)


    def print_ma(self, window, touch):
        """打印可移动位置"""
        if touch.button == 'left':
            self.x, self.y = touch.pos
            self.x /= m
            self.y /= m
            if not self.x > 1250:
                x = round((self.x - 66) / 133.3, 0)
                y = 8 - round((self.y - 66) / 133.3, 0)
                p = int(x + 10 * y)
                global sa
                global former_p
                if p in sa:
                    imagen = f'image_{p}'
                    if not self.beach[p]==None:
                        self.layout.remove_widget(globals()[imagen])
                    print(self.beach[p])
                    self.beach[former_p].move(p)
                    imagen2 = f'image_{former_p}'
                    globals()[imagen] = Image(source=f'./img/{self.beach[p].typ}.png', size_hint=(None, None),
                                              size=("65dp", "65dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)})
                    self.layout.add_widget(globals()[imagen])
                    self.layout.remove_widget(globals()[imagen2])
                    print(p, former_p)
                    sa=[]

                elif not self.beach[p] is None:
                    self.beach[p].get_ma()
                    print(self.beach[p].ma)
                    sa=self.beach[p].ma
                    former_p=p


    def handle_button_press(self, window, touch):
        if touch.button == 'left':
            x, y = touch.pos
            if self.is_within_bounds(x, y, "regret"):
                print("regret")
            elif self.is_within_bounds(x, y, "new"):
                print("new")
            elif self.is_within_bounds(x, y, "story"):
                print("story")

    def is_within_bounds(self, x, y, button_name):
        bounds = {
            "regret": (131 * m, 1484 * m, 680 * m, 768 * m),
            "new": (1316 * m, 1484 * m, 483 * m, 568 * m),
            "story": (1316 * m, 1484 * m, 263 * m, 356 * m)
        }
        x_min, x_max, y_min, y_max = bounds[button_name]
        return x_min < x < x_max and y_min < y < y_max


if __name__ == '__main__':
    BingGo().run()