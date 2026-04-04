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


def is_field_contains(element: Element) -> bool:
    """
    Проверяет, что элемент находится внутри поля.
    Используется, чтобы зафиксировать столкновение змейки с границей экрана.
    """
    return 0 <= element.x < WIDTH and 0 <= element.y < HEIGHT


def gen_apple(snake: Snake, game_level) -> Element:
    """Генерирует яблоко вне змейки и вне препятствий"""
    while True:
        candidate = gen_random_element()
        if not snake.is_contains(candidate) and not game_level.is_obstacle(candidate.x, candidate.y):
            return candidate


def is_good_head(head: Element, snake: Snake, game_level) -> bool:
    """Проверка на столкновение с собой и с препятствиями"""
    return (not snake.is_contains(head)) and (not game_level.is_obstacle(head.x, head.y))