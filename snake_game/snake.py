"""
贪吃蛇类定义
"""
from typing import List, Tuple
import pygame
from enum import Enum


class Direction(Enum):
    """移动方向枚举"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    """贪吃蛇类"""

    def __init__(self, start_pos: Tuple[int, int], cell_size: int):
        """
        初始化蛇

        Args:
            start_pos: 初始位置 (x, y)
            cell_size: 每个格子的大小
        """
        self.cell_size = cell_size
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT

        # 蛇身 - 列表存储每个格子的坐标
        # 头部在索引 0，尾部在最后
        self.body: List[Tuple[int, int]] = [
            start_pos,
            (start_pos[0] - 1, start_pos[1]),
            (start_pos[0] - 2, start_pos[1])
        ]

        self.grow_pending = 0  # 待增长的格子数
        self.alive = True

    def change_direction(self, new_direction: Direction) -> None:
        """
        改变蛇的移动方向

        Args:
            new_direction: 新方向
        """
        # 防止 180 度转向
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }

        if opposite.get(new_direction) != self.direction:
            self.next_direction = new_direction

    def move(self) -> Tuple[int, int]:
        """
        移动蛇

        Returns:
            新的头部位置
        """
        self.direction = self.next_direction

        # 计算新头部位置
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        # 将新头部插入到列表开头
        self.body.insert(0, new_head)

        # 如果没有待增长的格子，移除尾部
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

        return new_head

    def grow(self, amount: int = 1) -> None:
        """
        增加蛇的长度

        Args:
            amount: 增长的格子数
        """
        self.grow_pending += amount

    def check_self_collision(self) -> bool:
        """
        检查是否撞到自己

        Returns:
            是否发生碰撞
        """
        return self.body[0] in self.body[1:]

    def check_wall_collision(self, width: int, height: int) -> bool:
        """
        检查是否撞到墙壁

        Args:
            width: 游戏区域宽度（格子数）
            height: 游戏区域高度（格子数）

        Returns:
            是否发生碰撞
        """
        head_x, head_y = self.body[0]
        return head_x < 0 or head_x >= width or head_y < 0 or head_y >= height

    def get_head_position(self) -> Tuple[int, int]:
        """
        获取蛇头位置

        Returns:
            头部坐标
        """
        return self.body[0]

    def draw(self, screen: pygame.Surface, colors: List[Tuple[int, int, int]]) -> None:
        """
        绘制蛇

        Args:
            screen: Pygame 屏幕对象
            colors: 颜色列表用于渐变效果
        """
        for i, segment in enumerate(self.body):
            # 计算颜色 - 从头部到尾部渐变
            color_index = min(i, len(colors) - 1)
            color = colors[color_index]

            # 绘制圆角矩形
            rect = pygame.Rect(
                segment[0] * self.cell_size + 1,
                segment[1] * self.cell_size + 1,
                self.cell_size - 2,
                self.cell_size - 2
            )
            pygame.draw.rect(screen, color, rect, border_radius=self.cell_size // 4)

            # 头部添加眼睛
            if i == 0:
                self._draw_eyes(screen, segment)

    def _draw_eyes(self, screen: pygame.Surface, head_pos: Tuple[int, int]) -> None:
        """
        在蛇头上绘制眼睛

        Args:
            screen: Pygame 屏幕对象
            head_pos: 头部位置
        """
        eye_color = (255, 255, 255)
        pupil_color = (0, 0, 0)
        eye_size = self.cell_size // 5
        pupil_size = eye_size // 2

        base_x = head_pos[0] * self.cell_size
        base_y = head_pos[1] * self.cell_size

        # 根据方向确定眼睛位置
        if self.direction == Direction.RIGHT:
            eye1_pos = (base_x + self.cell_size * 3 // 4, base_y + self.cell_size // 3)
            eye2_pos = (base_x + self.cell_size * 3 // 4, base_y + self.cell_size * 2 // 3)
        elif self.direction == Direction.LEFT:
            eye1_pos = (base_x + self.cell_size // 4, base_y + self.cell_size // 3)
            eye2_pos = (base_x + self.cell_size // 4, base_y + self.cell_size * 2 // 3)
        elif self.direction == Direction.UP:
            eye1_pos = (base_x + self.cell_size // 3, base_y + self.cell_size // 4)
            eye2_pos = (base_x + self.cell_size * 2 // 3, base_y + self.cell_size // 4)
        else:  # DOWN
            eye1_pos = (base_x + self.cell_size // 3, base_y + self.cell_size * 3 // 4)
            eye2_pos = (base_x + self.cell_size * 2 // 3, base_y + self.cell_size * 3 // 4)

        # 绘制眼睛
        pygame.draw.circle(screen, eye_color, eye1_pos, eye_size)
        pygame.draw.circle(screen, eye_color, eye2_pos, eye_size)
        pygame.draw.circle(screen, pupil_color, eye1_pos, pupil_size)
        pygame.draw.circle(screen, pupil_color, eye2_pos, pupil_size)

    def reset(self, start_pos: Tuple[int, int]) -> None:
        """
        重置蛇的状态

        Args:
            start_pos: 新的起始位置
        """
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.body = [
            start_pos,
            (start_pos[0] - 1, start_pos[1]),
            (start_pos[0] - 2, start_pos[1])
        ]
        self.grow_pending = 0
        self.alive = True
