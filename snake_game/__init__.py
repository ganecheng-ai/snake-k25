"""
贪吃蛇游戏包
"""
from .game import Game, main
from .snake import Snake, Direction
from .food import Food
from .logger import setup_logger

__version__ = "1.0.6"
__all__ = ["Game", "main", "Snake", "Direction", "Food", "setup_logger"]
