"""
游戏主类 - 管理游戏状态和主循环
"""
import pygame
import os
from typing import Optional

from .snake import Snake, Direction
from .food import Food
from .logger import setup_logger


class Game:
    """游戏主类"""

    # 游戏配置
    CELL_SIZE = 25  # 每个格子的大小
    GRID_WIDTH = 30  # 网格宽度
    GRID_HEIGHT = 22  # 网格高度
    FPS = 60  # 帧率

    # 颜色定义
    BACKGROUND_COLOR = (20, 30, 40)
    GRID_LINE_COLOR = (35, 50, 65)
    TEXT_COLOR = (255, 255, 255)
    SCORE_COLOR = (100, 255, 100)
    GAME_OVER_COLOR = (255, 100, 100)

    # 蛇身渐变色
    SNAKE_COLORS = [
        (100, 255, 100),   # 头部 - 亮绿色
        (80, 220, 80),     # 浅绿色
        (60, 190, 60),     # 绿色
        (50, 160, 50),     # 深绿色
        (40, 130, 40),     # 更深绿色
    ]

    def __init__(self):
        """初始化游戏"""
        self.logger = setup_logger()
        self.logger.info("初始化游戏...")

        # 初始化 Pygame
        pygame.init()
        pygame.display.set_caption("贪吃蛇 Snake Game")

        # 计算窗口大小
        self.screen_width = self.GRID_WIDTH * self.CELL_SIZE
        self.screen_height = self.GRID_HEIGHT * self.CELL_SIZE + 60  # 额外空间用于分数显示

        # 创建窗口
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        # 初始化字体
        self._init_fonts()

        # 游戏状态
        self.snake: Optional[Snake] = None
        self.food: Optional[Food] = None
        self.score = 0
        self.high_score = self._load_high_score()
        self.game_over = False
        self.paused = False

        # 游戏速度控制
        self.move_delay = 100  # 毫秒
        self.last_move_time = 0
        self.base_speed = 100

        self.logger.info("游戏初始化完成")
        self.reset_game()

    def _init_fonts(self) -> None:
        """初始化字体"""
        # 尝试使用系统中文字体
        chinese_fonts = [
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/System/Library/PingFang.ttc",  # macOS
            "C:\\Windows\\Fonts\\msyh.ttc",  # Windows
            "C:\\Windows\\Fonts\\simsun.ttc",
        ]

        self.font_large: Optional[pygame.font.Font] = None
        self.font_medium: Optional[pygame.font.Font] = None
        self.font_small: Optional[pygame.font.Font] = None

        # 尝试加载中文字体
        for font_path in chinese_fonts:
            if os.path.exists(font_path):
                try:
                    self.font_large = pygame.font.Font(font_path, 48)
                    self.font_medium = pygame.font.Font(font_path, 32)
                    self.font_small = pygame.font.Font(font_path, 24)
                    self.logger.info(f"加载字体: {font_path}")
                    break
                except Exception as e:
                    self.logger.warning(f"无法加载字体 {font_path}: {e}")

        # 如果中文字体加载失败，使用系统默认字体
        if self.font_large is None:
            self.logger.warning("未找到中文字体，使用系统默认字体")
            self.font_large = pygame.font.SysFont("simhei", 48)
            self.font_medium = pygame.font.SysFont("simhei", 32)
            self.font_small = pygame.font.SysFont("simhei", 24)

    def _get_data_dir(self) -> str:
        """获取数据文件保存目录（程序运行目录）"""
        data_dir = os.path.join(os.getcwd(), "snake_game_data")
        os.makedirs(data_dir, exist_ok=True)
        return data_dir

    def _load_high_score(self) -> int:
        """加载最高分记录"""
        score_file = os.path.join(self._get_data_dir(), "highscore.txt")
        try:
            if os.path.exists(score_file):
                with open(score_file, "r", encoding="utf-8") as f:
                    return int(f.read().strip())
        except Exception as e:
            self.logger.error(f"加载最高分失败: {e}")
        return 0

    def _save_high_score(self) -> None:
        """保存最高分记录"""
        score_file = os.path.join(self._get_data_dir(), "highscore.txt")
        try:
            with open(score_file, "w", encoding="utf-8") as f:
                f.write(str(self.high_score))
        except Exception as e:
            self.logger.error(f"保存最高分失败: {e}")

    def reset_game(self) -> None:
        """重置游戏状态"""
        self.logger.info("重置游戏")

        # 创建蛇（从屏幕中间开始）
        start_x = self.GRID_WIDTH // 2
        start_y = self.GRID_HEIGHT // 2
        self.snake = Snake((start_x, start_y), self.CELL_SIZE)

        # 创建食物
        self.food = Food(self.CELL_SIZE)
        self.food.spawn(self.GRID_WIDTH, self.GRID_HEIGHT, self.snake.body)

        self.score = 0
        self.game_over = False
        self.paused = False
        self.move_delay = self.base_speed
        self.last_move_time = pygame.time.get_ticks()

    def handle_events(self) -> bool:
        """
        处理输入事件

        Returns:
            是否继续运行游戏
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.info("用户退出游戏")
                return False

            if event.type == pygame.KEYDOWN:
                # ESC 键退出
                if event.key == pygame.K_ESCAPE:
                    self.logger.info("用户按 ESC 退出")
                    return False

                # P 键暂停
                if event.key == pygame.K_p:
                    if not self.game_over:
                        self.paused = not self.paused
                        self.logger.info(f"游戏{'暂停' if self.paused else '继续'}")

                # 游戏结束时的重新开始
                if self.game_over:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()
                    continue

                # 暂停时忽略方向键
                if self.paused:
                    continue

                # 方向控制
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake.change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake.change_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake.change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake.change_direction(Direction.RIGHT)

        return True

    def update(self) -> None:
        """更新游戏状态"""
        if self.game_over or self.paused:
            return

        current_time = pygame.time.get_ticks()

        # 按时间间隔移动蛇
        if current_time - self.last_move_time >= self.move_delay:
            self.last_move_time = current_time

            # 移动蛇
            new_head = self.snake.move()

            # 检查是否撞墙
            if self.snake.check_wall_collision(self.GRID_WIDTH, self.GRID_HEIGHT):
                self.logger.info(f"游戏结束 - 撞墙，最终得分: {self.score}")
                self.game_over = True
                self.snake.alive = False
                return

            # 检查是否撞到自己
            if self.snake.check_self_collision():
                self.logger.info(f"游戏结束 - 撞到自己，最终得分: {self.score}")
                self.game_over = True
                self.snake.alive = False
                return

            # 检查是否吃到食物
            if new_head == self.food.get_position():
                self.logger.debug(f"吃到食物，位置: {new_head}")
                self.snake.grow(1)
                self.score += 10

                # 更新最高分
                if self.score > self.high_score:
                    self.high_score = self.score
                    self._save_high_score()

                # 生成新食物
                self.food.spawn(self.GRID_WIDTH, self.GRID_HEIGHT, self.snake.body)

                # 加快速度
                self.move_delay = max(40, self.base_speed - self.score // 2)

        # 更新食物动画
        self.food.update()

    def draw(self) -> None:
        """绘制游戏画面"""
        # 清空屏幕
        self.screen.fill(self.BACKGROUND_COLOR)

        # 绘制网格背景
        self._draw_grid()

        # 绘制游戏区域边框
        game_rect = pygame.Rect(0, 0, self.screen_width, self.GRID_HEIGHT * self.CELL_SIZE)
        pygame.draw.rect(self.screen, (60, 80, 100), game_rect, 2)

        # 绘制食物
        if self.food:
            self.food.draw(self.screen)

        # 绘制蛇
        if self.snake:
            self.snake.draw(self.screen, self.SNAKE_COLORS)

        # 绘制分数
        self._draw_score()

        # 绘制暂停提示
        if self.paused:
            self._draw_pause_screen()

        # 绘制游戏结束画面
        if self.game_over:
            self._draw_game_over_screen()

        # 更新显示
        pygame.display.flip()

    def _draw_grid(self) -> None:
        """绘制网格背景"""
        for x in range(0, self.GRID_WIDTH * self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRID_LINE_COLOR,
                             (x, 0), (x, self.GRID_HEIGHT * self.CELL_SIZE))
        for y in range(0, self.GRID_HEIGHT * self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRID_LINE_COLOR,
                             (0, y), (self.GRID_WIDTH * self.CELL_SIZE, y))

    def _draw_score(self) -> None:
        """绘制分数"""
        # 分数区域背景
        score_area = pygame.Rect(0, self.GRID_HEIGHT * self.CELL_SIZE,
                                 self.screen_width, 60)
        pygame.draw.rect(self.screen, (30, 45, 60), score_area)
        pygame.draw.line(self.screen, (60, 80, 100),
                         (0, self.GRID_HEIGHT * self.CELL_SIZE),
                         (self.screen_width, self.GRID_HEIGHT * self.CELL_SIZE), 2)

        # 分数文本
        score_text = f"得分: {self.score}"
        high_score_text = f"最高分: {self.high_score}"
        controls_text = "方向键/WASD: 移动  P: 暂停  ESC: 退出"

        if self.font_small:
            score_surface = self.font_small.render(score_text, True, self.SCORE_COLOR)
            high_surface = self.font_small.render(high_score_text, True, self.TEXT_COLOR)
            controls_surface = self.font_small.render(controls_text, True, (150, 150, 150))

            self.screen.blit(score_surface, (20, self.GRID_HEIGHT * self.CELL_SIZE + 10))
            self.screen.blit(high_surface, (20, self.GRID_HEIGHT * self.CELL_SIZE + 35))
            self.screen.blit(controls_surface,
                             (self.screen_width - controls_surface.get_width() - 20,
                              self.GRID_HEIGHT * self.CELL_SIZE + 20))

    def _draw_pause_screen(self) -> None:
        """绘制暂停画面"""
        # 半透明遮罩
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        self.screen.blit(overlay, (0, 0))

        # 暂停文字
        if self.font_large:
            pause_text = "游戏暂停"
            hint_text = "按 P 键继续"

            pause_surface = self.font_large.render(pause_text, True, self.TEXT_COLOR)
            hint_surface = self.font_small.render(hint_text, True, (200, 200, 200))

            pause_x = (self.screen_width - pause_surface.get_width()) // 2
            pause_y = self.screen_height // 2 - 30

            self.screen.blit(pause_surface, (pause_x, pause_y))
            self.screen.blit(hint_surface,
                             ((self.screen_width - hint_surface.get_width()) // 2,
                              pause_y + 60))

    def _draw_game_over_screen(self) -> None:
        """绘制游戏结束画面"""
        # 半透明遮罩
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))

        if self.font_large and self.font_medium:
            # 游戏结束文字
            over_text = "游戏结束"
            score_text = f"最终得分: {self.score}"
            high_text = f"最高分: {self.high_score}"
            restart_text = "按空格键或回车键重新开始"

            over_surface = self.font_large.render(over_text, True, self.GAME_OVER_COLOR)
            score_surface = self.font_medium.render(score_text, True, self.TEXT_COLOR)
            high_surface = self.font_medium.render(high_text, True, self.SCORE_COLOR)
            restart_surface = self.font_small.render(restart_text, True, (200, 200, 200))

            # 垂直居中排列
            center_x = self.screen_width // 2
            start_y = self.screen_height // 2 - 100

            self.screen.blit(over_surface,
                             (center_x - over_surface.get_width() // 2, start_y))
            self.screen.blit(score_surface,
                             (center_x - score_surface.get_width() // 2, start_y + 70))
            self.screen.blit(high_surface,
                             (center_x - high_surface.get_width() // 2, start_y + 110))
            self.screen.blit(restart_surface,
                             (center_x - restart_surface.get_width() // 2, start_y + 170))

    def run(self) -> None:
        """运行游戏主循环"""
        self.logger.info("游戏主循环开始")
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

        self.logger.info("游戏主循环结束")
        pygame.quit()


def main():
    """程序入口"""
    game = Game()
    game.run()
