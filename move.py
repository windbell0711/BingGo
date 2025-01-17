def test(x):  # 检测当前位置合法并且没有子
    if x % 10 != 9 and 89 >= x >= 0 == beach[x]:
        return True
    else:
        return False


def test2(x):  # 检测当前位置合法
    if x % 10 != 9 and 0 <= x <= 89:
        return True
    else:
        return False


def eat(x):  # 检测当前位置合法并且不是友方
    if x % 10 != 9 and 0 <= x <= 89 and beach[x] != self_camp:
        return True
    else:
        return False


def special_eat(x):  # 检测当前位置合法并且是敌方
    if beach[x] != 0 and beach[x] != self_camp and x % 10 != 9 and 0 <= x <= 89:
        return True
    else:
        return False


self_camp = 1  # 阵营 1-中象 2-国象 0-什么都不是
beach = []  # 沙场，每行末尾无子


class Qizi:
    def __init__(self, idt: int, p: int, camp: int, typ: int):
        self.idt = idt
        self.p = p
        self.camp = camp
        self.typ = typ
        self.ma = []

    def get_ma(self):
        ma = []  # move available positions
        if self.typ in (1, 8, 11):  # 直走
            p = self.p + 1
            while test(p):
                ma.append(p)
                p += 1
            if special_eat(p):
                ma.append(p)
            p = self.p - 1
            while test(p):
                ma.append(p)
                p += -1
            if special_eat(p):
                ma.append(p)
            p = self.p + 10
            while test(p):
                ma.append(p)
                p += 10
            if special_eat(p):
                ma.append(p)
            p = self.p - 10
            while test(p):
                ma.append(p)
                p += -10
            if special_eat(p):
                ma.append(p)
        if self.typ in (10, 11):  # 斜走的走子
            p = self.p + 11
            while test(p):
                ma.append(p)
                p += 11
            if special_eat(p):
                ma.append(p)
            p = self.p - 11
            while test(p):
                ma.append(p)
                p += -11
            if special_eat(p):
                ma.append(p)
            p = self.p + 9
            while test(p):
                ma.append(p)
                p += 9
            if special_eat(p):
                ma.append(p)
            p = self.p - 9
            while test(p):
                ma.append(p)
                p += -9
            if special_eat(p):
                ma.append(p)
        if self.typ == 2:  # 有马腿马
            p = self.p
            if test(p + 1):  # 马腿处子的判断
                if eat(p + 12):  # 落点吃子判断
                    ma.append(p + 12)
                if eat(p - 8):
                    ma.append(p - 8)
            if test(p - 1):
                if eat(p - 12):
                    ma.append(p - 12)
                if eat(p + 8):
                    ma.append(p + 8)
            if test(p + 10):
                if eat(p + 21):
                    ma.append(p + 21)
                if eat(p + 19):
                    ma.append(p + 19)
            if test(p - 10):
                if eat(p - 21):
                    ma.append(p - 21)
                if eat(p - 19):
                    ma.append(p - 19)
        if self.typ == 9:  # 无马腿马
            p = self.p
            if test2(p + 1):  # 马腿处子的判断
                if eat(p + 12):  # 落点吃子判断
                    ma.append(p + 12)
                if eat(p - 8):
                    ma.append(p - 8)
            if test2(p - 1):
                if eat(p - 12):
                    ma.append(p - 12)
                if eat(p + 8):
                    ma.append(p + 8)
            if test2(p + 10):
                if eat(p + 21):
                    ma.append(p + 21)
                if eat(p + 19):
                    ma.append(p + 19)
            if test2(p - 10):
                if eat(p - 21):
                    ma.append(p - 21)
                if eat(p - 19):
                    ma.append(p - 19)
        if self.typ == 3:  # xiang
            p = self.p
            if test(p + 11):  # xiang腿处子的判断
                if eat(p + 22):  # 落点吃子判断
                    ma.append(p + 22)
            if test(p - 11):
                if eat(p - 22):
                    ma.append(p - 22)
            if test(p + 9):
                if eat(p + 18):
                    ma.append(p + 18)
            if test(p - 9):
                if eat(p - 18):
                    ma.append(p - 18)
        if self.typ in (4, 12):  # shi king
            p = self.p
            if eat(p - 11):
                ma.append(p - 11)
            if eat(p + 11):
                ma.append(p + 11)
            if eat(p - 9):
                ma.append(p - 9)
            if eat(p + 9):
                ma.append(p + 9)
        if self.typ == 6:  # shuaui
            p = self.p
            if not p % 10 == 3:
                ma.append(p - 1)
            if not p % 10 == 5:
                ma.append(p + 1)
            if not p // 10 == 6:
                ma.append(p - 10)
            if not p // 10 == 8:
                ma.append(p + 10)
        if self.typ in (7, 12):  # bingo king
            p = self.p
            if not p % 10 == 0:
                ma.append(p + 1)
            if not p % 10 == 8:
                ma.append(p - 1)
            if not p // 10 == 0:
                ma.append(p - 10)
        if self.typ == 12:  # king
            p = self.p
            if not p // 10 == 8:
                ma.append(p + 10)
        if self.typ == 13:  # pawn
            p = self.p
            if test(p + 10):
                ma.append(p + 10)
            if special_eat(p + 11):
                ma.append(p + 11)
            if special_eat(p + 9):
                ma.append(p + 9)
        if self.typ == 5:  # pao
            p = self.p + 1
            while test(p):
                ma.append(p)
                p += 1
            while test(p):
                p += 1
            if special_eat(p):
                ma.append(p)
            p = self.p + 10
            while test(p):
                ma.append(p)
                p += 10
            while test(p):
                p += 10
            if special_eat(p):
                ma.append(p)
            p = self.p - 1
            while test(p):
                ma.append(p)
                p += -1
            while test(p):
                p += -1
            if special_eat(p):
                ma.append(p)
            p = self.p - 10
            while test(p):
                ma.append(p)
                p += -10
            while test(p):
                p += -10
            if special_eat(p):
                ma.append(p)
        self.ma = ma
