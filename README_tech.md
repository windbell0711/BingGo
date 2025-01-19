# 技术文档



## Objects and Functions
```
config.py
├── typ_dict: {"车": 1, "马": 2, ...}
└── ...

move.py
├── Beach
│  *├── beach: list[Qizi|None] (len=90)
│   │
│  *├── __getitem__(item) (get) -> Qizi|None
│  *├── set(qizi, p: int) (set)
│  *├── continuously_set(qizis: dict{p(int): typ(str|int)}) (set)
│   └┬─ valid(x: int) -> bool (judge)
│    ├─ occupied(x: int) -> bool (judge)
│    ├─ not_occupied(x: int) -> bool (judge)
│    ├─ ch_occupied(x: int) -> bool (judge)
│    └─ in_occupied(x: int) -> bool (judge)
└── Qizi
    ├── idt (!ready-to-be-expired)
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

display.py
├── War
│   ├── beach
│  *└── move_son(pfrom: int, pto: int)
└── BingGo(App)
    ├── (build)
    └┬─ get_p(window, touch)
     ├─ regret(window, touch)
     ├─ new(window, touch)
     └─ story(window, touch)
```





```sh
git clone https://github.com/windbell0711/BingGo.git
```

## Developing History
```
2025.1.15 立项。
1.16 确定实现路径和基本方向。
1.17 环境配置，基础学习；GitHub代码库配置；走子逻辑实现(Qizi类)；游戏名称及贴图。
1.18 修复bug；战场实现(Beach类)；修改mycamp判断方式；用kivy实现可视化，检测光标所在格。
1.19 修复bug；撰写README；更新display.py。
```

<br/>

*summarized by [@windbell0711](https://github.com/windbell0711/windbell0711)*
