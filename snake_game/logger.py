"""
日志系统模块 - 提供游戏运行日志记录功能
"""
import logging
import os
import sys
from datetime import datetime


def setup_logger(name: str = "snake_game") -> logging.Logger:
    """
    设置并返回游戏日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 创建日志目录 - 保存在程序运行目录
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # 日志文件名包含日期
    log_file = os.path.join(log_dir, f"snake_game_{datetime.now().strftime('%Y%m%d')}.log")

    # 文件处理器 - 记录所有级别日志
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # 控制台处理器 - 只记录 INFO 及以上级别
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("日志系统初始化完成")
    return logger
