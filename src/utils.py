from random import randrange
from element import Element
from snake import Snake
from constants import *


def gen_random_element() -> Element:
    """
    Генерирует случайный элемент на игровом поле.
    Используется для позиционирования яблок.
    """
    return Element(randrange(0, WIDTH), randrange(0, HEIGHT))


def get_center_element() -> Element:
    """
    Вычисляет центр игрового поля.
    Используется для начальной позиции змейки.
    """
    return Element(WIDTH // 2, HEIGHT // 2)


def gen_apple(snake: Snake, game_level) -> Element:
    """Генерирует яблоко вне змейки и вне препятствий"""
    while True:
        candidate = gen_random_element()
        if not snake.is_contains(candidate) and not game_level.is_obstacle(
                candidate.x, candidate.y):
            return candidate
