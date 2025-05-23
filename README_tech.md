# 技术文档
# 该部分长时间未维护，请注意甄别。

## Objects and Functions (need updating)
```
config.py
├── typ_dict: {"车": 1, "马": 2, ...}
├── init_lineup
└── ...

qizi.py
└── Qizi
    ├── idt
   *├── alive: bool
   *├── p: int (0-8, 10-18, ..., 80-88)
    ├── typ: int (1-13)(see typ_dict in config.py)
    ├── camp_intl: bool (chn-False;intl-True)
    ├── beach: addr of the beach located in
   *├── ma(move_avai_positions): list[p(int)]
    │
    ├── _not_mine(x: int) -> bool
    ├── _enemy_occupied(x: int) -> bool
   *├── get_ma()
   *└── move(p: int)

beach.py
└── Beach
   *├── beach: list[Qizi|None] (len=90)
   *├── pieces: list[Qizi] (corresponding with WarScreen.imgs)
    │
   *├── __getitem__(item) (get) -> Qizi|None
   *├── set_son(qizi, p: int) (set)
   *├── quick_set(qizis: dict{p(int): typ(str|int)}) (set)
   *├── move_son(pfrom: int, pto: int) -> idt: int (move)
    └┬─ valid(x: int) -> bool (judge)
     ├─ occupied(x: int) -> bool (judge)
     ├─ not_occupied(x: int) -> bool (judge)
     ├─ ch_occupied(x: int) -> bool (judge)
     └─ in_occupied(x: int) -> bool (judge)

display.py
├── fx(p)
├── fy(p)
├── WarScreen(FloatLayout)
│   ├── beach
│   ├── active_qizi
│   ├── mycamp
│   │
│   ├── log
│   ├── regret_mode
│   ├── regret_pointer
│   ├── imgs: list[Image] (corresponding with Beach.pieces)
│   │
│   ├── sound
│   ├── dots
│   │
│   ├── add_widget(image)
│   ├── remove_widget(image)
│   ├── show_path()
│   ├── remove_path()
│   ├── place_piece(qizi: Qizi, p: int, log=True)
│   ├── kill_piece(qizi: Qizi, log=True)
│   ├── _move_force(pfrom: int, pto: int, log=True)
│   ├── _castling(p)
│   ├── _promotion(p)
│   │
│   ├── handle_button_press(window, touch)
│   ├── board(x, y)
│   ├── ラウンドを終える()
│   ├── save()
│   ├── load()
│   ├── change_regret_mode()
│   ├── reproduce_operation(oper: Tuple[int, int, int]) -> None
│   ├── reverse_operation(oper: Tuple[int, int, int]) -> Tuple[int, int, int]
│   ├── regret()
│   ├── gret()
│   │
│   └── ...
├── BingGo(App)
│   ├── (build)
│   └── get_p(window, touch)
└── reset()
```




## How to contribute
```sh
git clone https://github.com/windbell0711/BingGo.git
```


## How to package

### Use a template for quick packeging
1. Check **BingGo.spec** and modify marked lines
2. Open the Terminal of the project, Run pyinstaller: ```pyinstaller BingGo.spec```

### Create *.exe via PyInstaller
1. Open the Terminal of the project  *e.g. D:/Documents/.../BingGo*
2. Run pyinstaller: ```pyinstaller [-F] [-w] [-i ....ico] [-n ...] main.py```
3. Modify the .spec file as below: ([example](BingGo.spec))
   1. Add ```from kivy_deps import sdl2, glew``` to the beginning;
   2. Add datas.  *e.g.*```[('D:/Documents/.../BingGo/img/*.png', './img'), ...]```
   3. Add hiddenimports.  *e.g.*```['packaging','packaging.version','kivy','enchant']```
   4. Add ```*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)]``` to ```COLLECT()```.
4. Run pyinstaller again: ```pyinstaller ....spec```

*Reference:*
1. [kivi document](https://kivy.org/doc/stable/guide/packaging-windows.html)
2. [question on stackoverflow](https://stackoverflow.com/questions/62500014/cant-create-a-exe-with-python-kivy-on-windows-pyinstaller/62707185#62707185)



## History

### Developing
```
2025.1.15 立项。
1.16 确定实现路径和基本方向。
1.17 环境配置，基础学习；GitHub代码库配置；走子逻辑实现(Qizi类)；游戏名称及贴图。
1.18 修复bug；战场实现(Beach类)；修改mycamp判断方式；用kivy实现可视化，检测光标所在格。
1.19 修复bug；撰写README；更新display.py；部分重构。
1.20 修复bug；实现走子、吃子等。
1.21 懒得记了。
```

### Releases
|   Time    |           Version           | Platform |                      Download                       |                                   Release                                    |
|:---------:|:---------------------------:|:--------:|:---------------------------------------------------:|:----------------------------------------------------------------------------:|
| 2025.3.7  |           v1.1.2            | Windows  | [v1.1.2](https://wwqe.lanzouo.com/iuP3Y2pwrj1c) (0) |                                      /                                       |
| 2025.2.11 |           v1.1.1            | Windows  | [v1.1.1](https://wwqe.lanzouo.com/iDu4z2nhpbwb) (3) |                                      /                                       |
| 2025.2.11 |            v1.1             | Windows  | [v1.1](https://wwqe.lanzouo.com/iibQm2nhazve) (66)  |                                      /                                       |
| 2025.1.31 |     BingGo Release v1.0     | Windows  | [v1.0](https://wwqe.lanzouo.com/iHWAY2mgk88h) (103) |       [v1.0](https://github.com/windbell0711/BingGo/releases/tag/v1.0)       |
| 2025.1.22 | BingGo Release (Trial) v0.0 | Windows  |                          /                          | [v0.0-alpha](https://github.com/windbell0711/BingGo/releases/tag/v0.0-alpha) |


### Videos

|    Time     |            Title            |  Version  |                            bv id                             | View | Like | Comment |
|:-----------:|:---------------------------:|:---------:|:------------------------------------------------------------:|:----:|:----:|:-------:|
|  2025.2.11  | 【中国象棋vs国际象棋】v1.1实机演示（附下载链接） |   v1.1    | [BV1dMNzeBExy](https://www.bilibili.com/video/BV1dMNzeBExy/) | 4005 |  96  |   30    |
|  2025.2.6   |  【中国象棋vs国际象棋】游戏规则介绍（含下载链接）  |   v1.0    | [BV1fPNEeDEBb](https://www.bilibili.com/video/BV1fPNEeDEBb/) | 4247 | 208  |   69    |





<br/>

*summarized by [@windbell0711](https://github.com/windbell0711/windbell0711), 2025.03.07*
