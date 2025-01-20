# BingGo
<p align="right">
  <a href="https://github.com/windbelljianjie0711/BingGo/README_en.md">EN</a> · 
  <a href="https://github.com/windbelljianjie0711/BingGo/README_tech.md">技术文档</a>
</p>
挺兵！将中国象棋和国际象棋的玩法结合，9*9的棋局中，中象与国象两军对垒。一同见证这场世界交融的战斗、文化交融的盛宴！


[![](https://img.shields.io/badge/issues-0-blue)](https://github.com/windbell0711/BingGo/issues)
![](https://img.shields.io/badge/contributors-2-green)
![](https://img.shields.io/badge/stars-1-orange)
[![](https://img.shields.io/badge/LICENSE-Apache2.0-yellow)](https://github.com/windbell0711/BingGo?tab=Apache-2.0-1-ov-file#readme)

<p align="center">
  <a href="https://github.com/windbelljianjie0711/BingGo">
    <img src="./img_readme/mahoupao.png" alt="Logo" width="160" height="160">
  </a>
</p>
<h3 align="center">BingGo</h3>
<p align="center">the magical integration with Chinese chess and International chess</p>

[<p align="center">**探索本项目的文档 »**</p>](#目录)
<p align="center">
  <a href="https://github.com/windbell0711/BingGo">查看Demo</a>  ·
  <a href="https://github.com/windbell0711/BingGo/issues">报告Bug</a>  ·
  <a href="https://github.com/windbell0711/BingGo/issues">提出新特性</a>
</p>

 
## 目录
- [规则介绍](#规则介绍)
  - [主要修改](#主要修改)
  - [完整规则](#完整规则)
- [游戏安装](#游戏安装)
- [作者](#作者)
- [技术信息](#技术信息)
- [版权说明](#版权说明)


## 规则介绍
### 主要修改
本游戏基本沿用中象或国象的走子和获胜规则，主要修改如下：
1. 棋盘初始状态如下图所示，大小为9*9，两方分别摆放中国象棋棋子和国际象棋棋子。
![游戏开局](./img_readme/war1.png)
2. 由于战场扩大，国际象棋增一兵。
3. 中国象棋增一中炮。
4. 取消中象中，相、士的走子范围限制。
5. 中象中，兵向前一步即可向前方、左侧或右侧移动一步。

### 完整规则

游戏由中国象棋方开始，安装以下方法轮流行走一次。

#### 国象方：
**帅**
沿直线移动一格，不能离开九宫格。
若直接面对王，并处于自己的回合开始，胜。

**士**
沿斜线移动一格

**相**
沿斜线移动两格，不能越子

**马**
沿直线移动一格，然后沿此方向斜向前移动一格，沿途有子则不能通过

**车**
沿直线移动任意格，不能越子

**炮**
沿直线移动任意格，不能越子，不能以此方式吃子
若直线上与敌方子间有且仅有一个子，可以将敌方子吃掉

**兵**
向前，左或右走一格，若到达底线，则可以立即变成车



#### 国象方：

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


## 游戏安装

## 作者
<img src="./img_readme/Lilold.png" alt="Logo" width="60" height="60"><a href="https://github.com/windbell0711/Lilold333">@Lilold</a>
<br/>
<img src="./img_readme/windbell0711.png" alt="Logo" width="60" height="60"><a href="https://github.com/windbell0711/windbell0711">@windbell0711</a>

## 技术信息
无论您是开发者还是用户，非常欢迎您来查看我们的[技术文档](README_tech.md)！

## 版权说明
本项目采用[Apache 2.0](LICENSE)协议。
