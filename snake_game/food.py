"""
食物类定义
"""
import random
from typing import Tuple, List
import pygame


class Food:
    """食物类"""

    def __init__(self, cell_size: int):
        """
        初始化食物

        Args:
            cell_size: 每个格子的大小
        """
        self.cell_size = cell_size
        self.position: Tuple[int, int] = (0, 0)
        self.animation_offset = 0.0
        self.animation_speed = 0.15

        # 食物颜色（红色系）
        self.colors = [
            (255, 50, 50),
            (255, 80, 80),
            (255, 100, 100),
            (255, 120, 120)
        ]

    def spawn(self, width: int, height: int, snake_body: List[Tuple[int, int]]) -> None:
        """
        在游戏区域生成新食物

        Args:
            width: 游戏区域宽度（格子数）
            height: 游戏区域高度（格子数）
            snake_body: 蛇身占据的位置列表
        """
        while True:
            pos = (random.randint(0, width - 1), random.randint(0, height - 1))
            if pos not in snake_body:
                self.position = pos
                break

    def update(self) -> None:
        """更新食物动画"""
        self.animation_offset += self.animation_speed
        if self.animation_offset > 3.14159 * 2:
            self.animation_offset = 0

    def draw(self, screen: pygame.Surface) -> None:
        """
        绘制食物

        Args:
            screen: Pygame 屏幕对象
        """
        import math

        # 计算脉动效果
        pulse = math.sin(self.animation_offset) * 2

        center_x = self.position[0] * self.cell_size + self.cell_size // 2
        center_y = self.position[1] * self.cell_size + self.cell_size // 2
        radius = (self.cell_size // 2 - 4) + pulse

        # 绘制外圈发光效果
        glow_color = (255, 100, 100, 100)
        pygame.draw.circle(screen, (255, 150, 150),
                          (center_x, center_y), int(radius + 3))

        # 绘制食物主体
        pygame.draw.circle(screen, self.colors[0],
                          (center_x, center_y), int(radius))

        # 绘制高光
        highlight_offset = radius // 3
        pygame.draw.circle(screen, (255, 200, 200),
                          (int(center_x - highlight_offset), int(center_y - highlight_offset)),
                          int(radius // 3))

    def get_position(self) -> Tuple[int, int]:
        """
        获取食物位置

        Returns:
            食物坐标
        """
        return self.position
