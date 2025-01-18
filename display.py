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
sa=[]

def fx(p):
    return (p%10+0.5)/12
def fy(p):
    return (8.5-p//10)/9


class war(App):
    def build(self):

        Window.size = (800, 600)
        self.layout = FloatLayout()
        image = Image(source='./img/beach.png',size=(1100, 1100), size_hint=(None, None),
                      pos_hint={'center_x': 0.375, 'center_y': 0.5})
        self.layout.add_widget(image)

        Window.bind(on_touch_down=self.get_p)

        for i in range(0,88):
            if not beach[i]== None:
                p=beach[i].p
                imagen = f'image_{i}'
                globals()[imagen] = Image(source=f'./img/{beach[i].typ}.png', size_hint=(None, None),
                                          size=(133, 133), pos_hint={'center_x': fx(p), 'center_y': fy(p)})
                self.layout.add_widget(globals()[imagen])

        return self.layout

    def get_p(self, window, touch):
        if touch.button == 'left':
            self.x, self.y = touch.pos
            if not self.x > 1250:
                x = round((self.x - 66) / 133.3, 0)
                y = 8 - round((self.y - 66) / 133.3, 0)
                p = int(x+10*y)
            if not beach[p]==None:
                sa=beach[p].get_ma()
                print(beach[p].ma)


if __name__ == '__main__':
    war().run()
