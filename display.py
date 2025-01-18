from move import *
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

if __name__ == '__main__':
    beach = Beach()
    pao = Qizi(idt=10086, p=60, typ=5, beach=beach)  # 炮
    bingo = Qizi(idt=8000, p=50, typ=7, beach=beach)  # 兵
    pawn = Qizi(idt=12345, p=10, typ=13, beach=beach)  # Pawn
    beach.set(qizi=pao, p=60)
    beach.set(qizi=bingo, p=50)
    beach.set(qizi=pawn, p=10)
    pao.get_ma()
    print(pao.ma)


class war(App):
    def build(self):

        Window.size = (800, 600)
        self.layout = FloatLayout()
        image = Image(source='beach.png', size_hint=(0.8, 1), pos_hint={'x': 0, 'y': 0})
        self.layout.add_widget(image)
        Window.bind(on_touch_down=self.get_p)
        Window.set_title("Kivy Mouse Tracker")
        return self.layout

    def get_p(self, window, touch):
        if touch.button == 'left':
            self.x, self.y = touch.pos
            if not self.x > 1250:
                x = round((self.x - 66) / 143, 0)
                y = 8 - round((self.y - 30) / 143, 0)
                p = int(x+10*y)
            if not beach[p]==None:
                beach[p].get_ma()
                print(beach[p].ma)


if __name__ == '__main__':
    war().run()