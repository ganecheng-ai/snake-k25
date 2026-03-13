"""
粒子效果系统 - 提供游戏中的视觉效果
"""
import pygame
from typing import List, Tuple
import random
import math


class Particle:
    """单个粒子"""

    def __init__(self, x: float, y: float, color: Tuple[int, int, int],
                 velocity: Tuple[float, float], lifetime: int, size: int):
        """
        初始化粒子

        Args:
            x: 初始X坐标
            y: 初始Y坐标
            color: 粒子颜色
            velocity: 速度向量 (vx, vy)
            lifetime: 生命周期（帧数）
            size: 粒子大小
        """
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.alive = True

    def update(self) -> None:
        """更新粒子状态"""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

        # 应用重力效果
        self.vy += 0.1

        if self.lifetime <= 0:
            self.alive = False

    def draw(self, screen: pygame.Surface) -> None:
        """
        绘制粒子

        Args:
            screen: Pygame 屏幕对象
        """
        # 根据生命周期计算透明度
        alpha = int(255 * (self.lifetime / self.max_lifetime))

        # 创建带透明度的表面
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        color_with_alpha = (*self.color, alpha)

        pygame.draw.circle(particle_surface, color_with_alpha,
                          (self.size, self.size), self.size)
        screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))


class ParticleSystem:
    """粒子系统管理器"""

    def __init__(self):
        """初始化粒子系统"""
        self.particles: List[Particle] = []

    def spawn_explosion(self, x: float, y: float, color: Tuple[int, int, int],
                        count: int = 10) -> None:
        """
        生成爆炸效果粒子

        Args:
            x: 爆炸中心X坐标
            y: 爆炸中心Y坐标
            color: 粒子颜色
            count: 粒子数量
        """
        for _ in range(count):
            # 随机速度方向
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            # 随机大小和生命周期
            size = random.randint(2, 5)
            lifetime = random.randint(20, 40)

            # 颜色变化
            color_variation = random.randint(-30, 30)
            particle_color = (
                max(0, min(255, color[0] + color_variation)),
                max(0, min(255, color[1] + color_variation)),
                max(0, min(255, color[2] + color_variation))
            )

            particle = Particle(x, y, particle_color, (vx, vy), lifetime, size)
            self.particles.append(particle)

    def spawn_sparkle(self, x: float, y: float, color: Tuple[int, int, int]) -> None:
        """
        生成闪烁效果粒子

        Args:
            x: 位置X坐标
            y: 位置Y坐标
            color: 粒子颜色
        """
        vx = random.uniform(-0.5, 0.5)
        vy = random.uniform(-1, -0.2)
        size = random.randint(1, 3)
        lifetime = random.randint(15, 30)

        particle = Particle(x, y, color, (vx, vy), lifetime, size)
        self.particles.append(particle)

    def update(self) -> None:
        """更新所有粒子"""
        for particle in self.particles[:]:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)

    def draw(self, screen: pygame.Surface) -> None:
        """
        绘制所有粒子

        Args:
            screen: Pygame 屏幕对象
        """
        for particle in self.particles:
            particle.draw(screen)

    def clear(self) -> None:
        """清除所有粒子"""
        self.particles.clear()
