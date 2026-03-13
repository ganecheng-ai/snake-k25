"""
贪吃蛇游戏包
"""
from .game import Game, main
from .snake import Snake, Direction
from .food import Food
from .logger import setup_logger
from .particle import ParticleSystem

__version__ = "1.0.8"
__all__ = ["Game", "main", "Snake", "Direction", "Food", "setup_logger", "ParticleSystem"]
