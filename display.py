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
        self.imgs = []

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
        image = Image(source='./img/beach.png', size=("800dp", "600dp"), size_hint=(None, None),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(image)

        # 按键绑定
        Window.bind(on_touch_down=self.handle_button_press)

        # 棋子贴图  TODO: 统一化未完成，应将quick_set()从Beach搬至BingGo
        self.imgs = []
        for qizi in self.beach.pieces:
            self.imgs.append(Image(
                source=f'./img/{qizi.typ}.png', size_hint=(None, None), size=("65dp", "65dp"),
                pos_hint={'center_x': fx(qizi.p), 'center_y': fy(qizi.p)}
            ))
            self.add_widget(self.imgs[-1])

        self.dots = []
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

    def place_piece(self, qizi: Qizi, p: int):
        idt = self.beach.set_son(qizi, p)
        self.imgs.append(Image(source='./img/%d.png' % qizi.typ, size_hint=(None, None),
                               size=("65dp", "65dp"), pos_hint={'center_x': fx(p), 'center_y': fy(p)}))
        self.add_widget(self.imgs[idt])
        self.log.append((1, qizi.typ, p))

    def kill_piece(self, qizi: Qizi):
        self.beach.set_son(None, qizi.p)
        qizi.alive = False
        self.remove_widget(self.imgs[qizi.idt])
        self.log.append((2, qizi.typ, qizi.p))

    def _move_force(self, pfrom: int, pto: int):
        # 判断是否吃子
        yummy, cuisine = self.beach.occupied(pto), None
        if yummy:
            cuisine = self.beach[pto].idt
        # 更新数据并获取棋子id，顺便写个日志
        idt = self.beach.move_son(pfrom, pto)
        self.log.append((0, pfrom, pto))
        # 确保图片置于顶层
        self.remove_widget(self.imgs[idt])
        self.add_widget(self.imgs[idt])
        # 走子平移动画
        animation = Animation(pos_hint={'center_x': fx(pto), 'center_y': fy(pto)}, duration=0.1)
        animation.start(self.imgs[idt])
        # 吃子消失动画
        if yummy:
            self.log.append((2, self.beach.pieces[cuisine].typ, pto))
            Clock.schedule_once(lambda dt: self.remove_widget(self.imgs[cuisine]), 0.1)

    def castling(self, p):  # 王车易位
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

    def promotion(self,p):  # 升变
        if self.beach[p].typ == 13 and 79 < p < 89:
            Clock.schedule_once(lambda dt: self.kill_piece(self.beach[p]),0.1)
            Clock.schedule_once(lambda dt: self.place_piece(Qizi(p=p, typ=11, beach=self.beach), p=p),0.1)
            return True
        if self.beach[p].typ == 7 and 0 <= p < 9:
            Clock.schedule_once(lambda dt: self.kill_piece(self.beach[p]),0.1)
            Clock.schedule_once(lambda dt: self.place_piece(Qizi(p=p, typ=0, beach=self.beach), p=p),0.1)
            return True
        return False

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
            if self.active_qizi is not None and self.beach[3] is not None and self.mycamp and self.castling(p):
                self.ラウンドを終える()
            else:
                self.active_qizi = self.beach[p]
                self.remove_path()
                self.show_path()
        elif self.active_qizi is not None and p in self.active_qizi.get_ma():  # 点选位置self.active_qizi能走到
            self._move_force(pfrom=self.active_qizi.p, pto=p)
            print("已移动")
            self.promotion(p)
            Clock.schedule_once(lambda dt: self.ラウンドを終える(), 0.15)
        else:
            print("无法抵达或无法选中")
        return

    def ラウンドを終える(self):
        self.mycamp = not self.mycamp
        self.active_qizi = None
        self.log.append((7, 0, 0))
        self.remove_path()
        print(self.log)


    def save(self):
        pass

    def load(self):
        pass

    def regret(self):
        pass

    def handle_button_press(self, window, touch):
        if touch.button == 'left':
            x, y = touch.pos
            print(x, y)
            x, y = x / M, y / M
            if x < 1250:
                self.board(x, y)
            elif 750 < y < 848:
                if 1268 < x < 1332:
                    print("regret")
                elif 1342 < x < 1462:
                    print("sure")
                elif 1476 < x < 1536:
                    print("gret")


class BingGo(App):
    def build(self):
        return War()


if __name__ == '__main__':
    BingGo().run()
