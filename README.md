# BingGo
# 别看了，文档几百年没修了
<p align="right">
  <a href="https://github.com/windbelljianjie0711/BingGo/README_en.md">EN</a> · 
  <a href="https://github.com/windbelljianjie0711/BingGo/README_tech.md">技术文档</a>
</p>
挺兵！将中国象棋和国际象棋的玩法结合，9×9的棋局中，中象与国象两军对垒。一同见证这场世界交融的战斗、文化交融的盛宴！

[![](https://img.shields.io/badge/python-3.7.5+-purple)](https://www.python.org)
[![](https://img.shields.io/badge/issues-0-blue)](https://github.com/windbell0711/BingGo/issues)
[![](https://img.shields.io/badge/contributors-3-green)](https://github.com/windbell0711/BingGo/graphs/contributors)
![](https://img.shields.io/badge/stars-3-orange)
[![](https://img.shields.io/badge/framework-kivy-darkred)](https://github.com/kivy/kivy)
[![](https://img.shields.io/badge/LICENSE-Apache2.0-yellow)](https://github.com/windbell0711/BingGo?tab=Apache-2.0-1-ov-file#readme)

<p align="center">
  <a href="https://github.com/windbell0711/BingGo">
    <img src="./img_readme/mahoupao.png" alt="Logo" width="150" height="150">
  </a>
</p>

<h3 align="center">BingGo</h3>
<p align="center">the magical integration with XiangQi and Chess</p>

[<p align="center">**探索代码仓库 »**</p>](https://github.com/windbell0711/BingGo)

<p align="center">
  <a href="https://github.com/windbell0711/BingGo/README_en.md">ENGLISH</a>
</p>
 
---

<p align="center">
  <img src="./img_readme/img1.png" alt="img1">
</p>

## 目录
- [规则介绍](#规则介绍)
  - [主要修改](#主要修改)
  - [完整规则](#完整规则)
- [游戏介绍](#游戏介绍)
  - [游戏安装](#游戏安装)
  - [功能介绍](#功能介绍)
- [开发者](#开发者)
- [技术信息](#技术信息)
- [版权说明](#版权说明)

---

## 规则介绍
### 主要修改
本游戏基本沿用中象或国象的走子和获胜规则，主要修改如下：
1. 棋盘初始状态如图所示，大小为**9*9**，双方分别摆放中国象棋棋子和国际象棋棋子
2. 中象中，取消**相**的走子范围限制，即可以过河，且可以斜走一格或两格，不能越子
3. 中象中，**兵**始终可以向前方、左侧或右侧移动一步，即初始即为过河兵
4. 中象中，**士**的走法改为国象中王的走法，即可以沿直线或斜线移动一格
5. 中象中，兵到底线可**升变**为新棋子：将

### 完整规则
游戏由中国象棋方开始，按照以下方法轮流行走一次。

<details>
<summary><strong>中象方：</strong></summary>

**帅**
沿直线移动一格，不能离开九宫格，
若直接面对王，并处于自己的回合开始，胜

**士**
沿直线或斜线移动一格

**相**
沿斜线移动一格或两格，不能越子

**马**
沿直线移动一格，然后沿此方向斜向前移动一格，沿途有子则不能通过

**车**
沿直线移动任意格，不能越子

**炮**
沿直线移动任意格，不能越子，不能以此方式吃子
若直线上与敌方子间有且仅有一个子，可以将敌方子吃掉

**兵**
向前，左或右走一格，若到达底线，则可以立即变成将

**将**
有以上所有棋子的走子或吃子方式
</details>

<details>
<summary><strong>国象方：</strong></summary>

**国王**
斜向或直线移动一格。若国王在与一城堡都在底线，且此城堡处于原位，国王可以向易位的城堡方向走两格，然后城堡越过国王移动至其邻格

**皇后**
沿斜线或直线移动任意格，不能越子

**城堡**
沿直线移动任意格，不能越子

**主教**
沿斜线移动任意格，不能越子

**骑士**
先向直线侧移两格，然后转向90度再移一格，可以越子

**士兵**
向前直走一格，在初始位置可以向前走一格或两格，不能以此法吃子。敌方子在斜前方一格，可以将其吃掉。若到达底线，则可以立即变成皇后
</details>

---

## 游戏介绍

### 游戏安装
当前最新版本（仅windows）：**BingGo v1.1** [https://github.com/windbell0711/BingGo/releases/tag/v1.1](https://github.com/windbell0711/BingGo/releases/tag/v1.0)

1. 点开上方最新版本Release地址（可能等待时间稍长）
2. 查看使用说明
3. 拉到最下面点开Assets（可能等待时间稍长）
4. 点击 **BingGo.v1.1.rar** 开始下载

**备用方案**：[蓝奏云下载地址]()

更多版本请查看[Releases](https://github.com/windbell0711/BingGo/releases)。

### 功能介绍

<details><summary><strong>行棋校验</strong></summary>

点击希望移动的棋子，系统会计算并显示可移动位置与可吃的棋子，点击目标位置可以进行移动。点击其他己方棋子可以重新选择。

<img src="./img_readme/img2.png">

先后点击王和车可以进行**王车易位**。

系统会自动计算游戏**将军状态**。如果玩家做出了致命的高血压操作，系统会**自动回退**并提示被将军。如果玩家下一步怎么做都难逃落败，即被将死，系统会直接提示**游戏胜利**，无法再进行下一步操作。


</details><details><summary><strong>悔棋重做</strong></summary>

点按左箭头或键盘“←”键可**悔棋**，点按右箭头或键盘“→”键可**重做**，长按可快速前进或后退。**悔棋后一旦走棋将无法再次重做**。


</details><details><summary><strong>人机</strong></summary>

点击**提示**可用内置ai算法走一步，勾选“红方人机”或“黑方人机”将**在轮到指定方时自动走棋**。

注：人机走的棋也可以由玩家回退。


</details><details><summary><strong>保存导出与载入</strong></summary>

**保存**和**载入**只会记录当前棋局历史，**不会记录悔棋和重下的部分**。
按下“保存”会在程序运行的目录下生成save.json（如已有则覆盖），并将棋局保存其中。
按下“载入”会在程序运行的目录下读取save.json（如无则无反馈），将当前棋局保存入autosaveXXXX.json，并载入save.json中的棋局。

如果嫌以上方法过于繁琐，可以在点击游戏空白处后按下Ctrl+C，即可将棋局录入进剪贴板，可以粘贴保存或发送给他人。
复制导出的游戏信息，点击游戏空白处后按下Ctrl+V，即可载入棋局，当前未保存棋局同样会自动保存进autosave.json

</details><details><summary><strong>贴图风格切换（v1.1+）</strong></summary>

点击右下角的贴图切换按钮，游戏会自动退出，重启游戏即可享受最新贴图。
注：退出游戏前会将未保存棋局录入lastsave.json，并在下次启动时载入。

</details><details><summary><strong>个性化设置（v1.2+）</strong></summary>


...

注：如果错误地编辑了preference.csv可能导致程序崩溃，此时只需删除preference.csv恢复默认设置即可。

</details><details><summary><strong>快捷指令（v1.2+）</strong></summary>

当在游戏界面（可点按任意空白处）内时，按下Ctrl+V，程序会读取最近的一条剪贴板信息，如果符合快捷指令语法将会直接执行。

也可以将快捷指令写入**输入框**，**按下Enter键**即可执行，执行结果会在输入框内显示。

快捷指令由“**指令名**”或“**指令名：参数1，参数2，参数3...**”组成，标点符号同时支持全半角。指令名前面可以加上“/”或“\”。多条快捷指令可以用“；”分隔，执行时会依次执行。

常见指令语法如下：

|     指令名     |    别名     |      参数1      |  参数2  |            说明            |
|:-----------:|:---------:|:-------------:|:-----:|:------------------------:|
|    load     |   载入、导入   |               |       |                          |
|    twist    |   翻转、反转   |       /       |   /   |          棋盘上下翻转          |
|    skip     |   跳过、交换   |       /       |   /   |        当前一步执棋方交换         |
|    sleep    | 装死、假死、未响应 | 时长(1~10000毫秒) |   /   |       使界面未响应指定时间（雾       |
|     set     |  更改设置、设置  |     目标设置项     | 目标设置值 |  修改setting.ini以进行个性化设置   |
|    reset    |   重置设置    |       /       |   /   |       将用户设置重置为默认值        |
|  set_zvgv3  |   棋类设置    |     目标设置项     | 目标设置值 | !谨慎操作，修改zvgv3.ini以改变棋局逻辑 |
| reset_zvgv3 |  重置棋类设置   |       /       |   /   |       将棋类设置重置为默认值        |
|    help     |  帮助、芝士什么  |       /       |   /   |         打开帮助文档网页         |
|    hello    |   你好、版本   |       /       |   /   |         显示当前版本信息         |


</details>

---

## 开发者
<img src="./img_readme/Lilold.png" alt="Lilold" width="60" height="60"><a href="https://github.com/Lilold333"> @Lilold</a>
<br/>
<img src="./img_readme/windbell0711.png" alt="windbell0711" width="60" height="60"><a href="https://github.com/windbell0711"> @windbell0711</a>
<br/>
<img src="./img_readme/mimi.png" alt="windbell0711" width="60" height="60"><a href="https://github.com/mimi99528"> @mimi99</a>

## 技术信息
本项目使用[kivy框架](https://github.com/kivy/kivy)开发，更多信息欢迎查看[技术文档](README_tech.md)！

## 版权说明
本项目采用[Apache 2.0](LICENSE)协议。
