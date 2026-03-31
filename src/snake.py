from collections import deque
from element import Element
from direction import Direction
from constants import HEIGHT, WIDTH

class Snake:
    """
    Класс контролирует элементы тела и направление движения змейки.
    """

    def __init__(self, head: Element):
        """
        :param head: Элемент игрового поля - голова змейки
        """
        self.snake = deque()
        self.snake.appendleft(head)
        self.direction = Direction.RIGHT

    def is_contains(self, element: Element) -> bool:
        """
        :param element: элемент поля, содержание которого в змейке нужно проверить
        :return: True или False
        """
        try:
            self.snake.index(element)
            return True
        except ValueError:
            return False

    def get_new_head(self) -> Element:
        """
        Вычисляет новую голову змейки в зависимости от направления движения с учётом перехода сквозь стены.
        :return:
        """
        head = self.snake[0]
        if self.direction == Direction.UP:
            new_y = (head.y + 1) % HEIGHT
            return Element(head.x, new_y)

        if self.direction == Direction.RIGHT:
            new_x = (head.x + 1) % WIDTH
            return Element(new_x, head.y)

        if self.direction == Direction.DOWN:
            new_y = (head.y - 1) % HEIGHT
            return Element(head.x, new_y)

        if self.direction == Direction.LEFT:
            new_x = (head.x - 1) % WIDTH
            return Element(new_x, head.y)
        raise ValueError("Неопознанное направление")

    def set_direction(self, new_direction):
        """
        Метод используется для изменения направления движения змейки
        :param new_direction: направление, которое нужно установить
        :return:
        """
        if len(self.snake) == 1 or new_direction.value % 2 != self.direction.value % 2:
            self.direction = new_direction

    def enqueue(self, new_head: Element):
        """
        Добавляет новую голову в начало змейки, используется когда змейка съедает яблоко
        :param new_head: Новый элемент головы змейки
        :return:
        """
        self.snake.appendleft(new_head)

    def dequeue(self):
        """
        Удаляет хвост змейки
        :return:
        """
        self.snake.pop()