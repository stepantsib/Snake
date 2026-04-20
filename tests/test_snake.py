import pytest
from src.snake import Snake
from src.element import Element
from src.direction import Direction
from src.constants import WIDTH, HEIGHT


def test_snake_initial_state():
    head = Element(10, 15)
    snake = Snake(head)
    assert len(snake.snake) == 1
    assert snake.snake[0] == head
    assert snake.direction == Direction.RIGHT


def test_is_contains():
    snake = Snake(Element(5, 5))
    snake.enqueue(Element(5, 4))
    snake.enqueue(Element(5, 3))
    assert snake.is_contains(Element(5, 5))
    assert snake.is_contains(Element(5, 3))
    assert not snake.is_contains(Element(99, 99))


def test_get_new_head_all_directions():
    head = Element(10, 10)
    snake = Snake(head)

    snake.direction = Direction.RIGHT
    assert snake.get_new_head() == Element(11, 10)

    snake.direction = Direction.LEFT
    assert snake.get_new_head() == Element(9, 10)

    snake.direction = Direction.UP
    assert snake.get_new_head() == Element(10, 11)

    snake.direction = Direction.DOWN
    assert snake.get_new_head() == Element(10, 9)


def test_get_new_head_wrap_around():
    snake = Snake(Element(WIDTH - 1, 5))
    snake.direction = Direction.RIGHT
    assert snake.get_new_head() == Element(0, 5)

    snake = Snake(Element(5, HEIGHT - 1))
    snake.direction = Direction.UP
    assert snake.get_new_head() == Element(5, 0)


def test_set_direction_rules():
    snake = Snake(Element(10, 10))

    snake.set_direction(Direction.UP)
    assert snake.direction == Direction.UP

    snake.enqueue(Element(10, 9))
    snake.set_direction(Direction.DOWN)
    assert snake.direction == Direction.UP

    snake.set_direction(Direction.RIGHT)
    assert snake.direction == Direction.RIGHT


def test_enqueue_dequeue():
    snake = Snake(Element(0, 0))
    snake.enqueue(Element(1, 0))
    snake.enqueue(Element(2, 0))
    assert len(snake.snake) == 3

    snake.dequeue()
    assert len(snake.snake) == 2
    assert snake.snake[-1] == Element(1, 0)


def test_get_new_head_invalid_direction():
    snake = Snake(Element(10, 10))
    snake.direction = "INVALID_DIRECTION"

    with pytest.raises(ValueError, match="Неопознанное направление"):
        snake.get_new_head()