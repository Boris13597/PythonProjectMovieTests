"""Настройка логирования."""

import logging
import sys


def setup_logger(name: str = "movie_tests", level: int = logging.INFO):
    """
    Настройка логгера для тестов.

    Args:
        name: Имя логгера
        level: Уровень логирования

    Returns:
        logging.Logger: Настроенный логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Создаем консольный обработчик
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(handler)

    return logger