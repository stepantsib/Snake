import pytest
from unittest.mock import patch
from src.utils import gen_random_element, get_center_element, gen_apple
from src.element import Element
from src.snake import Snake
from src.level import GameLevel, Level


def test_get_center_element():
    center = get_center_element()
    assert center.x == 20
    assert center.y == 12


@patch('src.utils.randrange')
def test_gen_random_element(mock_randrange):
    mock_randrange.side_effect = [7, 13]
    elem = gen_random_element()
    assert elem.x == 7
    assert elem.y == 13
    mock_randrange.assert_any_call(0, 40)
    mock_randrange.assert_any_call(0, 25)


def test_gen_apple_avoid_snake_and_obstacles():
    snake = Snake(Element(10, 10))
    snake.enqueue(Element(11, 10))

    level = GameLevel(Level.TWO)

    with patch('src.utils.gen_random_element') as mock_gen:
        mock_gen.side_effect = [
            Element(10, 10),
            Element(6, 4),
            Element(15, 15),
        ]
        apple = gen_apple(snake, level)
        assert apple == Element(15, 15)