from src.direction import Direction


def test_direction_values():
    assert Direction.UP.value == 1
    assert Direction.RIGHT.value == 2
    assert Direction.DOWN.value == 3
    assert Direction.LEFT.value == 4