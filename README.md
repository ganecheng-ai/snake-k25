# 贪吃蛇游戏 (Snake Game)

一款使用 Python 和 Pygame 开发的精美贪吃蛇游戏，支持简体中文界面。

## 功能特性

### 游戏玩法
- 经典贪吃蛇游戏体验
- 方向键或 WASD 键控制移动
- 吃到食物增长并得分
- 难度随分数增加而提升

### 界面特色
- 精美渐变蛇身效果
- 网格背景设计
- 食物脉动动画
- 蛇头动态眼睛
- 简体中文界面

### 系统功能
- 最高分记录保存
- 暂停功能（P键）
- 完整的日志系统
- 跨平台支持

## 系统要求

- Python 3.9+
- Pygame 2.5+
- Windows / Linux / macOS

## 安装与运行

### 方法 1：直接运行源代码

1. 克隆仓库
```bash
git clone git@github.com:ganecheng-ai/snake-k25.git
cd snake-k25
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行游戏
```bash
python main.py
```

### 方法 2：下载预编译版本

从 [Releases](https://github.com/ganecheng-ai/snake-k25/releases) 页面下载对应系统的预编译版本：

- **Windows**: `snake-game-windows-x64.exe`
- **Linux**: `snake-game-linux-x64.tar.gz`
- **macOS**: `snake-game-macos-x64.dmg`

## 操作说明

| 按键 | 功能 |
|------|------|
| ↑ / W | 向上移动 |
| ↓ / S | 向下移动 |
| ← / A | 向左移动 |
| → / D | 向右移动 |
| P | 暂停/继续 |
| ESC | 退出游戏 |
| Space / Enter | 游戏结束后重新开始 |

## 开发计划

详见 [plan.md](plan.md)

## 项目结构

```
.
├── snake_game/          # 游戏核心代码
│   ├── __init__.py
│   ├── game.py         # 游戏主逻辑
│   ├── snake.py        # 蛇类
│   ├── food.py         # 食物类
│   └── logger.py       # 日志系统
├── main.py             # 程序入口
├── requirements.txt    # 依赖列表
├── plan.md            # 开发计划
├── README.md          # 项目说明
└── .github/
    └── workflows/
        └── release.yml # GitHub Actions 发布流程
```

## 版本历史

### v1.0.4
- 更新 softprops/action-gh-release 从 v1 到 v2
- 修复 GitHub Actions Node.js 20 弃用警告

### v1.0.3
- 统一数据文件保存位置，highscore.txt 现在与日志文件保存在同一根目录下
- 代码质量优化：数据文件路径管理更加清晰

### v1.0.2
- 修复 GitHub Actions Node.js 20 弃用警告
- 添加 FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 环境变量配置

### v1.0.1
- 修复 GitHub Actions workflow 的 YAML 语法错误
- 优化 CI/CD 构建流程

### v1.0.0
- 首次发布
- 基础贪吃蛇游戏功能
- 简体中文界面支持
- 跨平台构建支持

## 许可证

[MIT License](LICENSE)

## 日志文件

游戏运行日志保存在 `logs/` 目录下，文件名为 `snake_game_YYYYMMDD.log`。

## 数据文件

游戏数据（最高分记录）保存在 `snake_game_data/` 目录下。
